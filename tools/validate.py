#!/usr/bin/env python3
"""Cross-checks the two packs before they ship.

Bedrock fails quietly on a bad reference, so this catches the mistakes that
otherwise show up as an invisible mob: a texture path that does not resolve, a
geometry or animation name nothing defines, an event that adds a component
group that was never declared, a UV net that runs off the texture.

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

pk = docs[os.path.join(BP, "entities/pikachu.json")]["minecraft:entity"]
groups = set(pk["component_groups"])


def walk(ev, node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("add", "remove"):
                for g in v.get("component_groups", []):
                    if g not in groups:
                        errs.append(f"event {ev}: unknown component group '{g}'")
            else:
                walk(ev, v)
    elif isinstance(node, list):
        for v in node:
            walk(ev, v)


for ev, body in pk["events"].items():
    walk(ev, body)
if pk["components"]["minecraft:shooter"]["def"] not in bp_ids:
    errs.append("minecraft:shooter points at an entity that does not exist")
if not os.path.exists(os.path.join(BP, pk["components"]["minecraft:loot"]["table"])):
    errs.append("loot table is missing")
if pk["components"]["minecraft:tameable"]["tame_event"]["event"] not in pk["events"]:
    errs.append("tame_event is not defined")

for pack, kind in ((BP, "data"), (RP, "resources")):
    m = docs[os.path.join(pack, "manifest.json")]
    if m["modules"][0]["type"] != kind:
        errs.append(f"{os.path.basename(pack)}: module type should be '{kind}'")
    if not os.path.exists(os.path.join(pack, "pack_icon.png")):
        errs.append(f"{os.path.basename(pack)}: pack_icon.png is missing")

bones_by_geo = {}
for p, d in docs.items():
    for g in d.get("minecraft:geometry", []):
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

pik = bones_by_geo.get("geometry.pikachu", set())
shock = bones_by_geo.get("geometry.thunder_shock", set())
for p in glob.glob(os.path.join(RP, "animations/*.json")):
    for an, a in docs[p]["animations"].items():
        pool = shock if "thunder" in an else pik
        for bn in a.get("bones", {}):
            if bn not in pool:
                errs.append(f"{an}: animates bone '{bn}' that the geometry lacks")

print(f"parsed {len(paths)} json files")
for e in errs:
    print("ERROR", e)
print("PASS" if not errs else f"{len(errs)} error(s)")
sys.exit(1 if errs else 0)
