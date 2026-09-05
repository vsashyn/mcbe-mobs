#!/usr/bin/env python3
"""Cross-checks the two packs before they ship.

Bedrock fails quietly on a bad reference, so this catches the mistakes that
otherwise show up as an invisible mob: a texture path that does not resolve, a
geometry or animation name nothing defines, an event that adds a component
group that was never declared, a UV net that runs off the texture.

Every check runs over every entity in the behavior pack, so a new mob is
covered the moment its files land.

Run: python3 tools/validate.py   (exit 1 on any error)
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP, RP = os.path.join(ROOT, "pikachu_BP"), os.path.join(ROOT, "pikachu_RP")
errs = []

paths = glob.glob(os.path.join(ROOT, "pikachu_*/**/*.json"), recursive=True)
docs = {}
for p in paths:
    try:
        docs[p] = json.load(open(p))
    except Exception as e:
        errs.append(f"{os.path.relpath(p, ROOT)}: {e}")

geos, anims, ctrls, rends = set(), set(), set(), set()
for p, d in docs.items():
    if not isinstance(d, dict):        # texts/languages.json and friends
        continue
    for g in d.get("minecraft:geometry", []):
        geos.add(g["description"]["identifier"])
    if "animations" in d and "minecraft:client_entity" not in d:
        anims |= set(d["animations"])
    ctrls |= set(d.get("animation_controllers", {}))
    rends |= set(d.get("render_controllers", {}))

bp_ids = {docs[p]["minecraft:entity"]["description"]["identifier"]
          for p in glob.glob(os.path.join(BP, "entities/*.json"))}

aliases = {}
for p in glob.glob(os.path.join(RP, "entity/*.json")):
    d = docs[p]["minecraft:client_entity"]["description"]
    rel = os.path.relpath(p, ROOT)
    aliases[d["identifier"]] = set(d.get("animations", {}))
    if d["identifier"] not in bp_ids:
        errs.append(f"{rel}: no behavior-pack entity for {d['identifier']}")
    for t in d.get("textures", {}).values():
        if not os.path.exists(os.path.join(RP, t + ".png")):
            errs.append(f"{rel}: texture '{t}.png' is missing")
    for gname in d.get("geometry", {}).values():
        if gname not in geos:
            errs.append(f"{rel}: geometry '{gname}' is not defined")
    for a in d.get("animations", {}).values():
        pool = ctrls if a.startswith("controller.") else anims
        if a not in pool:
            errs.append(f"{rel}: '{a}' is not defined")
    for n in d.get("scripts", {}).get("animate", []):
        if isinstance(n, str) and n not in d.get("animations", {}):
            errs.append(f"{rel}: scripts.animate references unmapped '{n}'")
    for rc in d.get("render_controllers", []):
        if rc not in rends:
            errs.append(f"{rel}: render controller '{rc}' is not defined")

known_aliases = set().union(*aliases.values()) if aliases else set()
for p in glob.glob(os.path.join(RP, "animation_controllers/*.json")):
    for cn, c in docs[p]["animation_controllers"].items():
        states = c["states"]
        if c["initial_state"] not in states:
            errs.append(f"{cn}: initial_state '{c['initial_state']}' is missing")
        for sn, st in states.items():
            for t in st.get("transitions", []):
                for target in t:
                    if target not in states:
                        errs.append(f"{cn}.{sn}: transition to unknown state '{target}'")
            for a in st.get("animations", []):
                if isinstance(a, str) and a not in known_aliases:
                    errs.append(f"{cn}.{sn}: '{a}' is not mapped on any client entity")

def walk(rel, groups, ev, node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("add", "remove"):
                for g in v.get("component_groups", []):
                    if g not in groups:
                        errs.append(f"{rel}: event {ev} names unknown "
                                    f"component group '{g}'")
            else:
                walk(rel, groups, ev, v)
    elif isinstance(node, list):
        for v in node:
            walk(rel, groups, ev, v)


for p in sorted(glob.glob(os.path.join(BP, "entities/*.json"))):
    ent = docs[p]["minecraft:entity"]
    rel = os.path.relpath(p, ROOT)
    groups = set(ent.get("component_groups", {}))
    events = ent.get("events", {})
    comps = ent.get("components", {})

    for ev, body in events.items():
        walk(rel, groups, ev, body)

    shooter = comps.get("minecraft:shooter")
    if shooter and shooter["def"] not in bp_ids:
        errs.append(f"{rel}: minecraft:shooter points at "
                    f"'{shooter['def']}', which does not exist")
    loot = comps.get("minecraft:loot")
    if loot and not os.path.exists(os.path.join(BP, loot["table"])):
        errs.append(f"{rel}: loot table '{loot['table']}' is missing")
    tame = comps.get("minecraft:tameable")
    if tame and tame["tame_event"]["event"] not in events:
        errs.append(f"{rel}: tame_event '{tame['tame_event']['event']}' "
                    f"is not defined")

    # transformation and interact both reach outside the file, and both turn
    # up inside component groups as often as in the base components
    for src in [comps] + list(ent.get("component_groups", {}).values()):
        into = src.get("minecraft:transformation", {}).get("into", "")
        if into and into.split("<")[0] not in bp_ids:
            errs.append(f"{rel}: transforms into '{into}', which does not exist")
        inter = src.get("minecraft:interact", {}).get("interactions", [])
        for i in ([inter] if isinstance(inter, dict) else inter):
            for key in ("add_items", "spawn_items"):
                t = i.get(key, {}).get("table")
                if t and not os.path.exists(os.path.join(BP, t)):
                    errs.append(f"{rel}: interact {key} table '{t}' is missing")
            ev = i.get("on_interact", {}).get("event")
            if ev and ev not in events:
                errs.append(f"{rel}: on_interact fires '{ev}', which is not defined")

# An item reaches into the resource pack for its icon and back into the
# behavior pack for the entity it throws. Both are silent failures in game:
# a missing icon shows up as the purple-and-black checker, and a throwable
# whose projectile does not resolve simply vanishes from the hand.
icons = docs.get(os.path.join(RP, "textures/item_texture.json"),
                 {}).get("texture_data", {})
item_ids = set()
for p in sorted(glob.glob(os.path.join(BP, "items/*.json"))):
    it = docs[p]["minecraft:item"]
    rel = os.path.relpath(p, ROOT)
    comps = it.get("components", {})
    item_ids.add(it["description"]["identifier"])

    proj = comps.get("minecraft:projectile")
    if proj and proj["projectile_entity"] not in bp_ids:
        errs.append(f"{rel}: throws '{proj['projectile_entity']}', "
                    f"which does not exist")
    if "minecraft:throwable" in comps and not proj:
        errs.append(f"{rel}: throwable, but no minecraft:projectile says what")

    icon = comps.get("minecraft:icon")
    if isinstance(icon, dict):
        icon = icon.get("textures", {}).get("default")
    if not icon:
        errs.append(f"{rel}: no minecraft:icon")
    elif icon not in icons:
        errs.append(f"{rel}: icon '{icon}' is not in item_texture.json")
    else:
        t = icons[icon]["textures"]
        for one in ([t] if isinstance(t, str) else t):
            if not os.path.exists(os.path.join(RP, one + ".png")):
                errs.append(f"{rel}: icon texture '{one}.png' is missing")

for p in sorted(glob.glob(os.path.join(BP, "loot_tables/**/*.json"),
                          recursive=True)):
    for pool in docs[p].get("pools", []):
        for e in pool.get("entries", []):
            if e.get("name", "").startswith("pk:") and e["name"] not in item_ids:
                errs.append(f"{os.path.relpath(p, ROOT)}: drops '{e['name']}', "
                            f"which is not an item this pack defines")

for p in sorted(glob.glob(os.path.join(BP, "recipes/*.json"))):
    for key, r in docs[p].items():
        if not key.startswith("minecraft:recipe"):
            continue
        res = r.get("result", {})
        for one in (res if isinstance(res, list) else [res]):
            if one.get("item", "").startswith("pk:") and one["item"] not in item_ids:
                errs.append(f"{os.path.relpath(p, ROOT)}: makes "
                            f"'{one['item']}', which is not an item this "
                            f"pack defines")

for p in sorted(glob.glob(os.path.join(BP, "spawn_rules/*.json"))):
    sid = docs[p]["minecraft:spawn_rules"]["description"]["identifier"]
    if sid not in bp_ids:
        errs.append(f"{os.path.relpath(p, ROOT)}: no behavior-pack entity "
                    f"for {sid}")

for pack, kind in ((BP, "data"), (RP, "resources")):
    m = docs[os.path.join(pack, "manifest.json")]
    if m["modules"][0]["type"] != kind:
        errs.append(f"{os.path.basename(pack)}: module type should be '{kind}'")
    if not os.path.exists(os.path.join(pack, "pack_icon.png")):
        errs.append(f"{os.path.basename(pack)}: pack_icon.png is missing")

bones_by_geo = {}
for p, d in docs.items():
    for g in (d.get("minecraft:geometry", []) if isinstance(d, dict) else []):
        gid = g["description"]["identifier"]
        tw, th = g["description"]["texture_width"], g["description"]["texture_height"]
        bones_by_geo[gid] = {b["name"] for b in g["bones"]}
        claimed = []
        for b in g["bones"]:
            if "parent" in b and b["parent"] not in bones_by_geo[gid]:
                errs.append(f"{gid}: bone '{b['name']}' has unknown parent '{b['parent']}'")
            for c in b.get("cubes", []):
                u, v = c["uv"]
                w, h, dd = c["size"]
                nw, nh = 2 * dd + 2 * w, dd + h
                if u + nw > tw or v + nh > th:
                    errs.append(f"{gid}/{b['name']}: uv net {nw}x{nh} at {u},{v} "
                                f"overflows {tw}x{th}")
                for ou, ov, onw, onh, obn in claimed:
                    if u < ou + onw and ou < u + nw and v < ov + onh and ov < v + nh:
                        errs.append(f"{gid}: uv overlap, {b['name']} vs {obn}")
                claimed.append((u, v, nw, nh, b["name"]))

# "animation.arboliva.walk" is expected to animate "geometry.arboliva", which
# is what keeps one mob's clip from quietly naming another mob's bones.
for p in glob.glob(os.path.join(RP, "animations/*.json")):
    for an, a in docs[p]["animations"].items():
        gid = "geometry." + an.split(".")[1]
        if gid not in bones_by_geo:
            errs.append(f"{an}: no {gid} to animate")
            continue
        for bn in a.get("bones", {}):
            if bn not in bones_by_geo[gid]:
                errs.append(f"{an}: animates bone '{bn}' that {gid} lacks")

print(f"parsed {len(paths)} json files")
for e in errs:
    print("ERROR", e)
print("PASS" if not errs else f"{len(errs)} error(s)")
sys.exit(1 if errs else 0)
