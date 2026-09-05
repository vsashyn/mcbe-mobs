# Pikachu

A Minecraft Bedrock add-on that adds `pk:pikachu`, a tameable electric mob that
fights with a Thunder Shock projectile.

## What it does

Wild Pikachu spawn in daylight in forest and plains biomes, in groups of one to
three. They wander, keep away from monsters, and follow anyone holding sweet
berries. Feed one sweet berries and it has a 35% chance to tame per berry.

A tamed Pikachu follows its owner, sits and stays when you interact with it,
heals from sweet berries and apples, and gets tougher (24 health, 4 attack
damage instead of 16 and 2). It attacks whatever attacks its owner, and whatever
its owner attacks, by firing Thunder Shock from up to 12 blocks away. Two tamed
adults fed apples will breed.

Pikachu take no damage from lightning. On death they drop 0-2 redstone, or
occasionally a gold nugget.

## Layout

```
pikachu_BP/                          behavior pack
  entities/pikachu.json              stats, AI, taming, breeding, growth
  entities/thunder_shock.json        the projectile Pikachu shoots
  spawn_rules/pikachu.json           where and how often it spawns
  loot_tables/entities/pikachu.json  death drops
pikachu_RP/                          resource pack
  entity/*.entity.json               ties model, texture and animations together
  models/entity/pikachu.geo.json     both geometries, 64x64 and 16x16 UV
  textures/entity/pikachu/*.png
  animations/pikachu.animation.json  idle, quadruped run, sit, head tracking, spark
  animation_controllers/             picks idle vs run vs sit
  render_controllers/
tools/gen_textures.py                redraws every png; edit here, not in an image editor
tools/validate.py                    catches broken references before the game does
tools/bump_version.py                raises the version in both manifests together
build.sh                             packs both folders into dist/Pikachu.mcaddon
```

## Installing

Run `./build.sh`, then open `dist/Pikachu.mcaddon`. Minecraft imports both packs
and you enable them per world under Settings, then Behavior Packs and Resource
Packs. The behavior pack depends on the resource pack, so enabling the behavior
pack pulls the other in.

`build.sh` bumps the patch version before zipping, because Minecraft rejects an
.mcaddon whose pack UUID and version both match one it already holds. The error
reads "identical pack detected" and it means the build was byte-identical as far
as the game is concerned, not that anything is broken. Pass `--no-bump` to
rebuild without moving the version, or `python3 tools/bump_version.py 1.2.0` to
set one explicitly.

If a stale copy is still in the way, remove the old pack in game under Settings,
Storage, then Packs, and import again.

Importing on every change gets old fast. For day-to-day work copy the two
folders straight into the game's data directory instead, which needs no import
and no version bump:

| Platform | Path |
| --- | --- |
| Windows | `%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\` |
| Android | `/storage/emulated/0/Android/data/com.mojang.minecraftpe/files/games/com.mojang/` |
| iOS | Minecraft's app folder in Files, under `games/com.mojang/` |

Behavior packs go in `development_behavior_packs/`, resource packs in
`development_resource_packs/`. Bedrock reloads those on world restart, so you
can edit a JSON file and just leave and rejoin the world.

## Testing in game

```
/give @s pk:pikachu_spawn_egg
/summon pk:pikachu ~ ~ ~
```

Turn on Content Log in Settings, Creator, to see JSON errors as they happen.
`/give @s sweet_berries 64` speeds up taming.

`/reload` only reloads functions and scripts, so it will not pick up a changed
texture, model or animation. `/reload all` does reload both packs, at the cost of
quitting and rejoining the world.

## Tuning

Spawn rate lives in `spawn_rules/pikachu.json` under `minecraft:weight`, raise
`default` to see more of them. Taming odds are `probability` in
`minecraft:tameable`. Thunder Shock damage and speed are `impact_damage.damage`
and `power` in `entities/thunder_shock.json`.

## Stances

Pikachu stands and idles upright on two legs. The moment it moves it drops onto
all fours and bounds like a rabbit.

The torso pitches 86 degrees forward, which is what carries the head down and
forward into a normal animal posture, and it rocks another 10 degrees nose-down
as the front paws land. The head cancels both, so it holds a steady 60 degrees
nose-down through the whole cycle instead of bobbing with the body.

The gait is a bound, not a trot: both front paws swing as one pair and both hind
legs as another, with the hind pair trailing by 48 degrees. The body rides a
squared cosine arc, which flattens the bottom of the hop so the paws have a wide
window to meet the ground and a long flight phase in between.

Two things there are easy to get wrong. A limb reaches its lowest point where its
swing crosses zero, not where the swing peaks, so each swing is a sine centred on
that limb's contact phase rather than a cosine. And a limb hanging off a pitched
torso needs its drop expressed in the torso's frame: a fall of `d` in world space
is `[0, -d*cos(p), -d*sin(p)]` where `p` is the pitch at the moment of contact.
Both limb offsets were solved by sweeping the cycle and taking each pair's
deepest frame, so change the pitch or the swing amplitudes and they have to be
solved again or the paws will float or sink.

The animation controller blends between standing and bounding over 0.3s, so the
change of stance reads as a crouch rather than a snap.

## Tooling

`Blockbench MCP` drives the Blockbench desktop app over MCP, which is what the
`.agents/skills/blockbench-*` skills in this repo expect. Install the plugin in
Blockbench under File, Plugins, Load Plugin from URL:

```
https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js
```

It then serves `http://localhost:3000/bb-mcp` (port and endpoint are under
Settings, General). `.mcp.json` registers it for this project. Among its 94 tools
are `capture_screenshot` and `capture_app_screenshot`, which matter more than
they sound: they let a model be looked at rather than reasoned about from
coordinates.

`Minecraft Creator Tools` is Mojang's own toolset, with a validator whose rules
are the ones Mojang actually cares about. Needs Node 22+, and the EULA has to be
accepted once before anything runs:

```
npm install -g @minecraft/creator-tools
npx mct eula
npx mct validate addon -i . -v
```

It also runs as an MCP server of its own, `npx mct mcp -i .`, working against the
project folder.

## Not done yet

No custom sounds. Adding them means shipping `.ogg` files plus a
`sounds/sound_definitions.json`, and wiring `minecraft:ambient_sound_interval`
in the behavior pack. The projectile borrows vanilla `cast.spell` and
`random.fizz` in the meantime.

No cheek-spark particles on the caster. Bedrock has no event hook on
`minecraft:behavior.ranged_attack`, so that needs a scripting-API listener or a
melee-driven animation controller instead.
