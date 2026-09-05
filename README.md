# Pokémon add-on for Minecraft Bedrock

A Minecraft Bedrock add-on with seven custom mobs and a Poké Ball that carries
them. Every mob is tameable, six of them fight with a custom projectile, and
all of them are built out of plain behavior and resource pack JSON with no
scripting API and no experimental toggles.

| Mob | Identifier | Wild HP / attack | Tamed HP / attack | Tame item | Where it spawns |
| --- | --- | --- | --- | --- | --- |
| Pikachu | `pk:pikachu` | 16 / 2 | 24 / 4 | Sweet berries, 35% a berry | Forest and plains, daylight, groups of 1-3 |
| Arboliva | `pk:arboliva` | 30 / 3 | 44 / 5 | Bone meal, 30% a handful | Savanna and forest, bright light, 1-2 |
| Black Rayquaza | `pk:rayquaza` | 160 / 10 | 220 / 14 | Ancient debris or a golden apple, 34% | Anywhere in the Overworld above y 80, alone and rare |
| Kleavor | `pk:kleavor` | 40 / 7 | 60 / 9 | Flint, 25% a piece | Forest and taiga, light 4 and up, alone |
| Squirtle | `pk:squirtle` | 20 / 3 | 30 / 5 | Raw cod, 30% a fish | Beach, river and swamp, 1-3 |
| Galarian Moltres | `pk:moltres` | 120 / 8 | 170 / 11 | Blaze rod or magma cream, 28% | Overworld surface above y 64, light 7 and under, alone and rare |
| Lapras | `pk:lapras` | 50 / 4 | 80 / 6 | Prismarine crystals, 22% | Ocean near the surface, frozen ocean most often, 1-2 |

The folders, the pack names and the built `.mcaddon` still say Pikachu, from
when it was the only mob here.

## Contents

- [Platform](#platform)
- [Installing](#installing)
- [Mobs](#mobs), one section each for [Pikachu](#pikachu), [Arboliva](#arboliva), [Black Rayquaza](#black-rayquaza), [Kleavor](#kleavor), [Squirtle](#squirtle), [Galarian Moltres](#galarian-moltres), [Lapras](#lapras), and the [projectiles](#projectiles) they shoot
- [Items](#items), covering the [Poké Ball](#poké-ball), [full balls](#full-poké-balls), [spawn eggs](#spawn-eggs), [how catching works](#how-catching-works)
- [Repository layout](#repository-layout)
- [Building](#building)
- [Testing in game](#testing-in-game)
- [Tuning](#tuning)
- [How the animation works](#how-the-animation-works)
- [Known gaps](#known-gaps)
- [Credits and license](#credits-and-license)

## Platform

This is a **Bedrock** add-on. It runs on the version of Minecraft that ships on
Windows 10/11, Android, iOS and iPadOS, Fire tablets, Xbox, PlayStation and
Switch, the one that reads `.mcaddon` files and pack folders full of JSON.

It will not run on Minecraft Java Edition. Java mods are compiled code against
Forge, Fabric or NeoForge, and nothing in this repository transfers. There is no
Java port planned.

| | |
| --- | --- |
| Minimum game version | 1.21.0, set as `min_engine_version` in both manifests |
| Packs | One behavior pack and one resource pack, each with its own UUID |
| Experimental toggles | None. Custom items use the stable `1.21.0` item format |
| Scripting API | Not used. No `@minecraft/server`, so no Beta APIs toggle |
| Commands | Only Black Rayquaza's Air Lock runs one, and it degrades quietly without cheats |
| Multiplayer | Works on a Realm or a dedicated server the same way it works locally, as long as both packs are applied to the world |

The behavior pack declares the resource pack as a dependency by UUID and
version, so enabling the behavior pack in a world pulls the resource pack in
with it. `tools/bump_version.py` moves the header version, both module versions
and both dependency versions together, which is what keeps that link from
breaking.

Consoles cannot import an `.mcaddon` from a filesystem, because there is no
filesystem to import from. The usual route onto a console is a Realm, or a world
built on Windows or a phone with both packs already applied and then uploaded.

## Installing

### From a release

Download the `.mcaddon` and open it. Minecraft imports both packs. Enable them
per world under Settings, then Behavior Packs and Resource Packs. Enabling the
behavior pack pulls the resource pack in.

### From source

```sh
git clone <this repo>
cd <this repo>
./build.sh
open dist/Pikachu.mcaddon
```

`build.sh` needs Python 3 and `zip`, both of which macOS and most Linux
installs already have. It bumps the patch version, runs `tools/validate.py`,
and refuses to build if the validator finds anything.

The version bump matters. Minecraft rejects an `.mcaddon` whose pack UUID and
version both match one it already holds, with the error "identical pack
detected". That means the build was byte-identical as far as the game is
concerned, not that anything is broken. Pass `--no-bump` to rebuild without
moving the version, or run `python3 tools/bump_version.py 1.2.0` to set one
explicitly.

If a stale copy is still in the way, remove the old pack in game under Settings,
Storage, then Packs, and import again.

### Development folders

Importing on every change gets old fast. For day-to-day work copy the two
folders straight into the game's data directory instead, which needs no import
and no version bump.

| Platform | Path |
| --- | --- |
| Windows | `%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\` |
| Android | `/storage/emulated/0/Android/data/com.mojang.minecraftpe/files/games/com.mojang/` |
| iOS | Minecraft's app folder in Files, under `games/com.mojang/` |

Behavior packs go in `development_behavior_packs/`, resource packs in
`development_resource_packs/`. Bedrock reloads those on world restart, so you
can edit a JSON file and just leave and rejoin the world.

## Mobs

### Pikachu

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

### Arboliva

Arboliva is built as a tree, not as an animal with leaves on. A flared trunk
stands on two short roots, tapers through a pale segment that carries the face,
and finishes in a canopy of two overlapping slabs with a leaf blade sprouting
off the top. Four branches arch out on the diagonals from just under that
canopy, each one weeping back down into a wide leaf frond with an olive hanging
below it. Two more olives dangle from the canopy rim. It stands four blocks
tall and the canopy spreads about three blocks across, so it reads as a real
tree in the treeline. Its hitbox stays at one block by two, wrapped around the
trunk only, so it fits doorways and paths like any other mob while the canopy
overhangs the way a tree should.

Wild Arboliva stand in bright savanna and forest, alone or in pairs. They are
slow, they keep clear of monsters, and they follow anyone holding bone meal.
Feed one bone meal and it has a 30% chance to tame per handful.

A tamed Arboliva follows its owner, sits and stays when you interact with it,
heals from bone meal and apples, and gets tougher (44 health, 5 attack damage
instead of 30 and 3). Two tamed adults fed apples or oak saplings will breed,
and the baby stands in for Dolliv at 90% scale, a shade under two blocks tall.

Oil Salvo takes the card at its word. Six globs go out in one burst 0.2 seconds
apart, 2 damage each and two seconds of slowness where they land, from up to 14
blocks. The volley has a three block dead zone, so up close Arboliva swings its
branches instead. Being a tree, it also shrugs off knockback, ignores poison and
wither, and takes double from fire and lava. It has no panic behavior either, so
it stands its ground and burns.

On death it drops 0-2 sticks, an oak sapling, or a handful of bone meal.

### Black Rayquaza

`pk:rayquaza` is the shiny Rayquaza, charcoal where the ordinary one is
emerald, keeping the hollow yellow rings, the red-rimmed rudders and the pale
grey blades swept back along the jaw. It is ten segments long, about five and
a half blocks nose to tail, and it has no walk cycle because it never touches
the ground.

The Pokedex has it living in the ozone layer, feeding on meteoroids, and coming
down only to break up a fight, so that is what it does. It spawns alone and
rarely, and only where the ground stands above y 80. It ignores players until
provoked, but hunts anything in the `monster` family within 40 blocks, firing a
three-shot burst of Dragon Pulse from up to 32 blocks out while it keeps
circling. It has 160 health, shrugs off most knockback, and takes no damage
from lightning, fire, falling, drowning or freezing.

Air Lock is its ability in the games, and it cancels the weather. Here it runs
`weather clear` whenever the sky is not clear, then sits out 30 seconds before
it will do that again. It needs commands allowed in the world. With cheats off
nothing breaks, the weather just stays.

Taming costs a meteorite. Feed it ancient debris, or a golden apple if you have
not reached the Nether yet, and it has a 34% chance to bond per feed. A tamed
Rayquaza carries 220 health, defends its owner, teleports to keep up, heals
from golden apples and ancient debris, and can be ridden. Interact without
sneaking to mount, and `minecraft:input_air_controlled` puts WASD and the mouse
in charge of all three dimensions.

On death it drops 2-4 phantom membrane, plus dragon breath or, one roll in
four, the ancient debris back.

### Kleavor

`pk:kleavor` is the axe. Both arms end in a slab of stone wider than its head,
and the rest of the mob follows from that. It is the only one here with no
projectile, and the only one that would rather you came closer.

Wild Kleavor stand alone in forest and taiga, anywhere the light is 4 or
brighter, so a shaded forest floor counts. They leave players
alone until provoked, but they hunt anything in the `monster` family within 20
blocks, and they walk through leaves, vines and bamboo rather than around them,
breaking what they pass. One crossing a forest leaves a trail you can follow.

Taming costs flint, which is as close as Minecraft gets to the black augurite
Kleavor evolves from. Each piece has a 25% chance to bond. A tamed one carries
60 health and 9 attack damage instead of 40 and 7, follows its owner, sits when
you interact with it, heals from honeycomb and flint, and breeds on honeycomb.
The baby stands in for Scyther at half scale.

The stone plates are worth something. It takes half damage from fire, lava and
burning, a quarter from a fall, and keeps its feet under most knockback. Water
runs the other way, and drowning costs it double.

On death it drops 0-2 flint, a couple of cobblestone, or one worn stone axe.

### Squirtle

`pk:squirtle` is the only mob here that is as much at home in water as out of
it. It is a squat biped, a big round head over a cream plastron, a red-brown
shell that wraps wider than the body so its edges show from the front, stubby
clawed arms and legs, and a three-segment tail that curls back and up over the
shell.

Wild Squirtle stand on beaches, along rivers and in swamps, alone or in small
groups. They wander between land and water on their own, keep clear of
monsters, panic toward water rather than away from it, and follow anyone
holding raw cod. Feed one cod and it has a 30% chance to tame per fish.

A tamed Squirtle follows its owner, withdraws into its shell when you interact
with it, heals from cod and salmon, and gets tougher (30 health, 5 attack
damage instead of 20 and 3). Two tamed adults fed salmon or tropical fish will
breed.

Water Gun is the attack. A single jet, 4 damage with knockback, from 3 to 13
blocks; inside three blocks it tackles instead. The jet barely slows in water,
so a Squirtle fighting in a river is as dangerous as one on the bank.

Torrent is its ability, and here it does what the games say. Below a third of
its health, Squirtle's water moves hit 1.5x harder. The shooter swaps from
`pk:water_gun` to `pk:water_gun_torrent`, 6 damage instead of 4, and swaps back
if it heals. Everything else about the attack stays the same, so Torrent is a
damage change and nothing else.

The shell is worth something and the type chart costs it. It shrugs off half of
any fall, fire, lava or burn damage and most knockback, breathes water so it
never drowns, and takes double from lightning, which is the exact opposite of
Pikachu.

On death it drops 0-2 prismarine shards, or a raw cod.

### Galarian Moltres

`pk:moltres` is the Galar form, not the orange bird from Kanto. It is black
where the Kantonian one is yellow, its beak, cap and legs are scarlet, its eyes
are pale blue, and everything that would be a feather is a magenta flame.
Twenty-one of the model's forty-five bones are flame, six on each wing, three
in the crest, one off each side of the nape and four on the tail, and not one
of them ever holds still.

The Pokedex calls it the Malevolent Pokemon and says its aura consumes the
spirit of whatever it touches, leaving a burned-out shadow behind. So this is
the one mob in the pack that goes for a player unprovoked. It takes anything in
the `monster` family within 32 blocks and any player within 20, it has to see
its target, and it gives up on one it has not seen for six seconds. A hit lands
8 damage and three seconds of wither. At range it throws Fiery Wrath, three
bolts of 6 that also set what they touch alight for three seconds.

Berserk is its ability in the games, a special attack boost once its health
falls below half. Here dropping under half swaps in a component group that
raises melee to 12, stretches the wither to four seconds and turns the burst
into four bolts on a 0.9 to 1.8 second cycle instead of three on 1.4 to 2.8. It
drops back out if the bird heals over the line again. A wild one crosses at 60
health, a tamed one at 85.

It spawns alone and rarely, only on the surface above y 64 and only at light
level 7 or under, which in practice means at night or under a storm.

Taming costs a trip to the Nether. Feed it a blaze rod or magma cream and it
has a 28% chance to bond per feed. A tamed Moltres carries 170 health, defends
its owner, teleports to keep up, heals from magma cream and blaze rods, and can
be ridden the same way Rayquaza can. Interact without sneaking to mount.

On death it drops 3-6 feathers, plus blaze powder or, one roll in four, a blaze
rod.

### Lapras

`pk:lapras` is the ferry. It is the biggest thing in the pack that still
touches the ground, two and a half blocks from its keel to the curl of its
ears, and the only one you can ride across water.

The build is a plesiosaur. A flared torso carries a grey shell of three slabs
stepping inward to a crown, with ten blunt knobs sunk into them, and four
paddles on the corners with the front pair longer than the back. A three-link
neck stands off the front and holds a small head with two brown eyes, a short
horn and a curled ear each side. Blue hide, darker blue blotches, and a cream
keel running unbroken from the chin to between the flippers.

Its hitbox is 1.4 by 2.4 wrapped around the body alone, so the paddles and the
shell rim overhang it the way Arboliva's canopy does. It still will not fit a
one-block doorway, which is the point of a mob this size.

Wild Lapras spawn in ocean biomes near the surface, most often frozen ocean,
then deep ocean, then open water, and never more than two together. They are
gentle, and nothing makes one go after a player who has not hit it first. They
wander between water and shore, keep clear of monsters, panic toward water
rather than away from it, and follow anyone holding kelp.

Taming costs prismarine crystals, which is as close as this game gets to an
offering worth making to something that was hunted to near extinction. Each
one has a 22% chance to bond.

A tamed Lapras carries 80 health and 6 attack damage instead of 50 and 4,
follows its owner, heals from kelp, cooked cod and prismarine crystals, and
breeds on cooked salmon or kelp. Interact to climb on, sneak and interact to
make it sit and stay. Those two share one button and do not collide because
`crouching_skip_interact` on the rideable drops a crouching interact through to
`minecraft:sittable`. `minecraft:input_ground_controlled` hands WASD the reins
once you are aboard, and since the navigation is amphibious it steers on water
as readily as on land, which is Surf.

Ice Beam is the attack. One shard, 5 damage and four seconds of slowness 2,
from 4 to 16 blocks, with almost no gravity and no loss of speed in water. It
does not knock back, so what a Lapras does to something chasing it is slow it
down and keep swimming.

Water Absorb and Shell Armor are its abilities and both land here as damage
rules. Water Absorb reads a `water_move` family off whatever hit it, which
`pk:water_gun`, `pk:water_gun_torrent` and `pk:ice_beam` all carry, and takes
nothing from any of them, so a Squirtle cannot touch a Lapras with a jet and
neither can another Lapras. Shell Armor is a quarter off every melee hit and
every projectile. Being Water and Ice it also breathes water, ignores freezing,
and takes double from fire, lava and lightning.

On death it drops 0-2 prismarine shards, a couple of ice, or one packed ice.

### Projectiles

Every projectile is a full entity with its own model, texture and flight
behavior, spawned by `minecraft:behavior.ranged_attack` on the mob that shoots
it.

| Move | Identifier | Shooter | Damage | Range | Shape |
| --- | --- | --- | --- | --- | --- |
| Thunder Shock | `pk:thunder_shock` | Pikachu | 4 | up to 12 | One bolt, no gravity |
| Oil Salvo | `pk:oil_salvo` | Arboliva | 2 each | 3 to 14 | Six globs 0.2s apart, 2s slowness on hit |
| Dragon Pulse | `pk:dragon_pulse` | Black Rayquaza | 7 each | 4 to 32 | Three bolts 0.35s apart, no gravity |
| Water Gun | `pk:water_gun` | Squirtle | 4 | 3 to 13 | One jet with knockback |
| Water Gun, Torrent | `pk:water_gun_torrent` | Squirtle under a third health | 6 | 3 to 13 | The same jet at 1.5x |
| Fiery Wrath | `pk:fiery_wrath` | Galarian Moltres | 6 each | 4 to 24 | Three bolts 0.25s apart, no gravity, 3s alight |
| Ice Beam | `pk:ice_beam` | Lapras | 5 | 4 to 16 | One shard, near-flat, no knockback, 4s slowness 2 |

## Items

### Poké Ball

`pk:poke_ball` is an item you throw. It is the one thing in the pack that is
not a mob, and it is what turns the mobs into something you can carry.

Craft it from three red dye over two iron ingots with a redstone between them,
over three white dye. That makes two.

```
red dye      red dye      red dye
iron ingot   redstone     iron ingot   ->  2 x Poké Ball
white dye    white dye    white dye
```

Hold one and use it the way you would a snowball. Empty balls stack to 16.

A ball that hits a Pokémon either catches it or is wasted. A tamed one always
goes in, since it is already yours. A wild one resists, and Arboliva and
Squirtle go in three times in five, Kleavor one in two, Lapras two in five,
Rayquaza one in five.
A ball that misses, hits a block, or fails to hold is gone.

Pikachu is the exception right now. Its `pk:on_captured` skips the roll and
always holds, so the catch is easy to test without fighting the dice. Put the
`randomize` back the way the other four have it to give Pikachu its odds again.

### Full Poké Balls

A caught Pokémon leaves a ball lying where it stood, its button in the colour
of what is inside. That ball on the ground is an entity. Interact with it to
pick it up as an item, named for its occupant.

| Item | Identifier | Ground entity | Stack |
| --- | --- | --- | --- |
| Poké Ball | `pk:poke_ball` | none, it is only an item | 16 |
| Poké Ball (Pikachu) | `pk:poke_ball_pikachu` | `pk:caught_pikachu` | 1 |
| Poké Ball (Arboliva) | `pk:poke_ball_arboliva` | `pk:caught_arboliva` | 1 |
| Poké Ball (Black Rayquaza) | `pk:poke_ball_rayquaza` | `pk:caught_rayquaza` | 1 |
| Poké Ball (Kleavor) | `pk:poke_ball_kleavor` | `pk:caught_kleavor` | 1 |
| Poké Ball (Squirtle) | `pk:poke_ball_squirtle` | `pk:caught_squirtle` | 1 |
| Poké Ball (Galarian Moltres) | `pk:poke_ball_moltres` | `pk:caught_moltres` | 1 |
| Poké Ball (Lapras) | `pk:poke_ball_lapras` | `pk:caught_lapras` | 1 |

Throw a full ball and the Pokémon comes out a third of a second later, wherever
the ball got to, tamed to whoever threw it.

So the ball is a one-way trip for a wild Pokémon and a pocket for a tame one.
A baby comes back grown, and nothing but the owner survives the trip. Health,
sitting, name and age are all lost. Full balls do not stack.

### Spawn eggs

Every mob is spawnable, so Bedrock generates a spawn egg for each one and puts
it in the creative inventory.

`pk:pikachu_spawn_egg`, `pk:arboliva_spawn_egg`, `pk:rayquaza_spawn_egg`,
`pk:kleavor_spawn_egg`, `pk:squirtle_spawn_egg`, `pk:moltres_spawn_egg`,
`pk:lapras_spawn_egg`.

### How catching works

None of this needs the scripting API. The ball is in the `poke_ball` family and
lands one point of damage, and every Pokémon reads that hit off its own
`minecraft:damage_sensor`, the way a creeper reads a lightning strike. The
trigger matches on the family, swallows the damage and fires `pk:on_captured`.

The family test has to name `damager`, not `other`. On a projectile hit Bedrock
puts the ball in `damager` and the player who threw it in `other`, so a filter
on `other` asks whether the thrower is a Poké Ball, comes back no every time,
and lets the hit through as one point of ordinary damage. That is what a broken
ball looks like from inside the game: the Pokémon flinches and stays where it
is. The filter is written as an `any_of` over both subjects so it holds if a
future version moves the ball back into `other`.
Anything without that trigger just takes the point, so a cow gets a bruise and
nothing else. The event hands the mob a `minecraft:transformation` into the
ball that lies on the ground, and the full ball transforms the other way on a
0.3 second delay. `keep_owner` carries the thrower through both turns, which is
what makes the Pokémon that comes out belong to the player who threw it.

The hit has to be real damage for a damage sensor to see it, which is the whole
reason the ball deals a point at all. The thrown ball also carries a
`definition_event` on its `on_hit` that fires the same event on what it struck.
Either path alone catches the Pokémon, and both firing at once changes nothing,
because the event is written so that repeating it lands in the same place.

That event catches first and asks questions second. `pk:on_captured` adds
`pk:caught` outright, and only then does a wild Pokémon roll to break free,
which removes the group again well inside the transformation's 0.35 second
delay. Written the other way round, a filter that failed to evaluate would
leave the ball doing nothing at all, and a ball that quietly does nothing is
the hardest thing here to debug.

Covering a new mob means four files that name a species
(`entities/caught_<mob>.json`, `entities/poke_ball_<mob>_thrown.json`,
`items/poke_ball_<mob>.json`, `loot_tables/entities/caught_<mob>.json`), an
entry in `OCCUPANTS` in `gen_textures.py` and in `item_texture.json`, and four
things on the mob itself, the `pk:caught` group, the `pk:on_captured` and
`pk:break_free` events, `minecraft:entity_transformed`, and the `poke_ball`
trigger at the head of its damage sensor. `validate.py` catches every one of
those you forget except the ones on the mob.

## Repository layout

```
pikachu_BP/                           behavior pack
  entities/pikachu.json               stats, AI, taming, breeding, growth
  entities/thunder_shock.json         the projectile Pikachu shoots
  entities/arboliva.json              same, for Arboliva
  entities/oil_salvo.json             the glob Arboliva shoots, six at a time
  entities/rayquaza.json              stats, flight, taming, riding, Air Lock
  entities/kleavor.json               stats, AI, taming, breeding, block breaking
  entities/dragon_pulse.json          the bolt Rayquaza shoots, three at a time
  entities/squirtle.json              stats, amphibious movement, taming, Torrent
  entities/water_gun.json             the jet Squirtle shoots
  entities/water_gun_torrent.json     the same jet at 1.5x, once Torrent is up
  entities/moltres.json               stats, flight, hostility, taming, riding, Berserk
  entities/fiery_wrath.json           the bolt Moltres shoots, three at a time
  entities/lapras.json                stats, amphibious movement, taming, riding
  entities/ice_beam.json              the shard Lapras shoots
  entities/poke_ball_thrown.json      the ball in flight; catches what it hits
  entities/poke_ball_*_thrown.json    a full ball, turns back into its mob
  entities/caught_*.json              a ball on the ground, waiting to be picked up
  items/poke_ball.json                the empty ball, and one item per full one
  recipes/poke_ball.json              iron, redstone and two dyes
  spawn_rules/*.json                  where and how often each one spawns
  loot_tables/entities/*.json         death drops
pikachu_RP/                           resource pack
  entity/*.entity.json                ties model, texture and animations together
  models/entity/pikachu.geo.json      mob and projectile, 64x64 and 16x16 UV
  models/entity/arboliva.geo.json     20 bones on a 128x64 sheet, plus the glob
  models/entity/rayquaza.geo.json     40 bones on a 128x128 sheet, plus the bolt
  models/entity/kleavor.geo.json      27 bones, 33 cubes, 128x128, no projectile
  models/entity/squirtle.geo.json     11 bones on a 64x64 sheet, plus the jet
  models/entity/moltres.geo.json      45 bones, 51 cubes, 256x128, plus the bolt
  models/entity/lapras.geo.json       22 bones, 33 cubes, 128x128, plus the shard
  models/entity/poke_ball.geo.json    five cubes on a 32x32 sheet, one bone
  textures/entity/*/*.png
  animations/pikachu.animation.json   idle, quadruped run, sit, head tracking, spark
  animations/arboliva.animation.json  idle, walk, sit, head tracking, drip
  animations/rayquaza.animation.json  hover, glide, hunt, head tracking, spin
  animations/kleavor.animation.json   idle, walk, chop, sit, head tracking
  animations/squirtle.animation.json  idle, waddle, swim, withdraw, head tracking
  animations/moltres.animation.json   hover, glide, hunt, head tracking, spin
  animations/lapras.animation.json    idle, crawl, swim, rest, head tracking
  animations/poke_ball.animation.json spin in flight, bob at rest
  textures/items/*.png                inventory icons, 16x16
  textures/item_texture.json          maps an icon name onto its png
  texts/en_US.lang                    every name the player reads
  animation_controllers/              picks idle vs walk vs sit, one per mob
  render_controllers/
tools/gen_rayquaza.py                 lays out Rayquaza's 46 cubes and its wave;
                                      run it before gen_textures.py
tools/gen_moltres.py                  lays out Moltres's 51 cubes and its wingbeat;
                                      run it before gen_textures.py
tools/gen_lapras.py                   lays out Lapras's 33 cubes and shelf-packs its
                                      UV; run it before gen_textures.py
tools/gen_textures.py                 redraws every png; edit here, not in an image editor
                                      Arboliva's is painted off its .geo.json
tools/validate.py                     catches broken references before the game does
tools/bump_version.py                 raises the version in both manifests together
build.sh                              packs both folders into dist/Pikachu.mcaddon
.github/workflows/validate.yml        runs the validator on every push and PR
```

## Building

```sh
./build.sh              # bump the patch version, validate, zip
./build.sh --no-bump    # rebuild at the same version
python3 tools/validate.py
python3 tools/bump_version.py 1.2.0
python3 tools/gen_textures.py
python3 tools/gen_rayquaza.py   # run before gen_textures.py when the model moves
```

Textures are generated, not painted. `gen_textures.py` redraws every `.png` in
the resource pack, so an edit in an image editor is lost on the next run. Edit
the script.

`validate.py` is the gate. It parses every JSON file in both packs and fails on
a texture path that does not resolve, a geometry or animation name nothing
defines, an event that adds a component group that was never declared, and a UV
net that overlaps another or runs off the sheet. It also fails on a key that
appears twice in the same JSON object, which is worth having because Bedrock
keeps the second one and says nothing.

It walks every entity in the behavior pack rather than a named list, so a new
mob is checked the moment its files land. It ties an animation to a geometry by
name, so `animation.arboliva.walk` has to animate bones that `geometry.arboliva`
actually has.

Box UV is fixed at one texel per model unit. That ties sheet size to model size,
so a mob cannot be made bigger without either a proportionally bigger sheet or
texels coarser than the rest of the game.

`gen_textures.py` keeps every mob's palette in one flat namespace at the top of
the file, so a new mob whose colour name collides with an older one silently
repaints the older mob. Nothing catches it. `validate.py` does not look at
pixels, and the only sign is an unrelated `.png` turning up in `git status`
after a run. Check that list against the mob you actually touched.

## Testing in game

```
/give @s pk:pikachu_spawn_egg
/give @s pk:arboliva_spawn_egg
/give @s pk:rayquaza_spawn_egg
/give @s pk:kleavor_spawn_egg
/give @s pk:squirtle_spawn_egg
/give @s pk:lapras_spawn_egg
/give @s pk:moltres_spawn_egg
/summon pk:pikachu ~ ~ ~
/summon pk:arboliva ~ ~ ~
/summon pk:rayquaza ~ ~10 ~
/summon pk:kleavor ~ ~ ~
/summon pk:squirtle ~ ~ ~
/summon pk:lapras ~ ~ ~
/summon pk:moltres ~ ~12 ~
/give @s pk:poke_ball 16
/give @s pk:poke_ball_pikachu
```

Summon Rayquaza with some height under it. It has no gravity and no walk cycle,
so at ground level it spends its first seconds shouldering out of the terrain.

Turn on Content Log in Settings, Creator, to see JSON errors as they happen.
`/give @s sweet_berries 64` speeds up taming Pikachu, `/give @s bone_meal 64`
does the same for Arboliva, `/give @s ancient_debris 16` for Rayquaza,
`/give @s flint 64` for Kleavor and `/give @s cod 64` for Squirtle. To see the
chop, summon a Kleavor and a zombie near each other; it goes for the zombie on
its own.

To see Water Gun, hit a Squirtle from a dozen blocks away and back off. It
answers with the jet, and closes to tackle if you come inside three blocks. To
see Torrent, `/effect @e[type=pk:squirtle,c=1] instant_damage 1 1` down to under
a third of its health and watch the jets get heavier.

To see Lapras do the one thing it is for, summon one in the sea, feed it
prismarine crystals until it bonds, then interact to climb on and steer with
WASD. `/give @s prismarine_crystals 32` and `/give @s kelp 64` cover the taming
and the tempting. Water Absorb is quickest to check with two mobs: put a
Squirtle and a tamed Lapras in the same water and hit the Squirtle so it
answers, and the jets should land on the Lapras for nothing at all.

Balls are worth testing on a tamed mob first, because a tame catch never fails.

`/reload` only reloads functions and scripts, so it will not pick up a changed
texture, model or animation. `/reload all` does reload both packs, at the cost of
quitting and rejoining the world.

## Tuning

Spawn rate lives in `spawn_rules/`, under `minecraft:weight`; raise `default` to
see more of them. Taming odds are `probability` in `minecraft:tameable`.
Projectile damage and speed are `impact_damage.damage` and `power` in the
projectile entity. The size of Arboliva's volley is `burst_shots` and
`burst_interval` in `minecraft:behavior.ranged_attack`. How readily a wild
Pokémon goes into a ball is the pair of weights under `randomize` in its
`pk:on_captured` event, and how far a full ball flies before it opens is
`delay` on the thrown ball's `minecraft:transformation`.

## How the animation works

Every clip in the pack is written by hand as a Molang expression rather than
keyframed, so the notes below are the reasoning behind the numbers. Change a
number and the paragraph tells you what else has to move with it.

### Pikachu's stances

Pikachu stands and idles upright on two legs. The moment it moves it drops onto
all fours and bounds like a rabbit.

Get the sign right before anything else. A positive x rotation in a Bedrock
animation pitches a bone nose-down and swings a hanging limb backward, the same
convention `query.target_x_rotation` feeds a head. Vanilla says so twice. The
rabbit swings its front legs forward on `jump_rotation * -40`, and a sitting
ocelot pitches its body to -45 and puts its front legs back at +42.15 so they
stand vertical. Every value in this clip was written the other way round until
now, which is why Pikachu ran on its back with its face to the sky.

The torso holds 71 degrees nose-down and rocks 6 more as the front paws land,
which lays the body flat and carries the head down and forward. The head takes
the opposite 6, so it holds a steady 48 degrees nose-down for the whole cycle,
watching the ground it is about to cover instead of bobbing with the body. Ears,
tail and every limb are written the same way, as the world angle they should
hold minus the torso pitch, because a child bone inherits its parent's pitch and
nothing else stops it riding along.

The gait is a bound, not a trot. Both front paws swing as one pair and both hind
legs as another, with the hind pair trailing by 55 degrees and the right of each
pair by 12, which is enough asymmetry to keep the bound from reading as a
mirror. The body rides a squared cosine, which flattens the bottom of the hop.
The paws are on the ground for a third of the cycle and in the air for the rest.

A limb reaches its lowest point where its swing crosses zero, not where the
swing peaks, so each swing is a sine centred on that limb's contact phase. The
pitch does the rest of the work. At 77 degrees, the pitch as the front paws
land, the shoulder sits exactly 4 units up, which is the length of the front
leg, and the hip never leaves 3, which is the length of the hind leg. Both pairs
reach the ground with nothing stretched, so no limb carries a position offset.
Move the pitch and the paws float or sink.

The number to know is the 66 that scales `modified_distance_moved`. That query
counts about four units per block, so 66 is one bound every 1.4 blocks, and a
paw slides under a twentieth of a block while it is down. Vanilla small
quadrupeds use 38.17 for a trot, which lands a footfall every 1.2 blocks. A
bound puts both front paws down once per cycle where a trot lands them twice, so
it needs roughly double the constant to keep that spacing. This was 24, a hop
every 3.75 blocks, and the paws skated.

The animation controller blends between standing and bounding over 0.3s, so the
change of stance reads as a crouch rather than a snap.

Sitting had the same inverted signs. A tamed Pikachu now settles back on its
haunches with the hind legs folded forward and the front paws propped straight,
the way a sitting ocelot does, instead of pitching forward with its legs out
behind it.

### Arboliva's sway

Arboliva is a tree, so nothing about it snaps. The rig hangs in chains, trunk
to face segment to canopy to blade, and branch to frond to olive, and every
link moves later and further than the link above it.

Idle runs off `query.life_time` so it never stops moving, even standing still.
The trunk leans 1.6 degrees side to side, the canopy lags it by 40 degrees of
phase and doubles the amplitude, the blade lags by 65 and doubles again, and
the olives lag by 85 and swing 7. Each joint down the chain is a low-pass
filter with a delay, which is the whole trick behind something looking heavy
and organic instead of rigidly parented.

The four branches share those amplitudes but each carries its own phase
offset, 25, 42, 60 and 78 degrees. That is the only thing stopping the canopy
from pulsing as one piece, which is the tell that gives away a rig like this.
The offsets carry down each branch's own frond and olive.

Walking swaps the phase source to `query.modified_distance_moved` and scales
every amplitude by `query.modified_move_speed`, so the sway ramps in and out
with the gait instead of popping on. The roots alternate on a 30 degree cosine
over a long stride. The trunk rolls 4.5 degrees into each step and rides the
double frequency, low at full stride and high where a root passes vertical. The
branches bounce on that same double frequency, once per footfall, with a
single-frequency sway added on top so the bounce and the lean do not line up.

The number worth knowing about is the 18 that scales
`modified_distance_moved`. It sets stride length, not cadence, and it follows
the leg geometry, so it has to move whenever the legs do. Get it wrong and the
feet slide or stutter, which is the one animation fault this rig can have that
a still render will not show.

Sitting is a static pose with one exception. The olives and fronds keep a slow
`life_time` sway, so a sitting Arboliva still reads as alive.

### Rayquaza's flight

The rig is one chain, `neck`, then eight body segments, then the tail, each one
parented to the segment in front, so rotating any of them carries everything
behind it. Every segment runs the same sine on its yaw and lags the segment
ahead by 42 degrees, which is what sends the curve travelling head to tail
instead of swinging the whole body as a unit. The same phase drives a cosine on
the roll, a quarter cycle out, so the serpent screws through the air rather
than wagging flat.

Amplitude and rate carry the mood. Hovering is slow and wide, 8 degrees at 95 a
second. Gliding tightens to 5.5 degrees at 200 and folds the arms back along
the body. Hunting is 4.5 at 300, jaw open 20 degrees, jaw blades flared out
and claws forward. The controller picks between the three on `query.has_target`
and `query.modified_move_speed` and blends over 0.4 to 0.6 seconds, so a change
of gait reads as an acceleration rather than a cut.

Head tracking is deliberately outside that chain. `head` hangs off `root`, not
off `neck`, so `query.target_x_rotation` turns the skull without dragging five
blocks of serpent round after it.

Forty-six cubes is more UV than is safe to keep in two places, so the model
and the clips both come out of `tools/gen_rayquaza.py`, which shelf-packs the
UV net, and the Rayquaza half of `gen_textures.py` reads those slots back out
of the model rather than holding a second copy of the table. Change the model
and you have to rerun both, in that order. Cube sizes have to stay whole
numbers, because a fractional width makes a fractional UV net, and the net
cannot land on whole pixels.

### Kleavor's chop

`minecraft:behavior.delayed_attack` is what makes a visible swing possible.
Where `melee_attack` just deals damage, this one holds the mob in an attack for
a fixed `attack_duration`, lands the blow partway through at `hit_delay_pct`,
and raises `query.is_delayed_attacking` on the client for exactly that window.
The animation controller watches that query, so the chop plays while the blow
is being thrown instead of on a timer that drifts out of step with it.

The clip is 0.75 seconds, the same as `attack_duration`, and its impact frame
sits at 0.34, which is the 45% mark the behavior hits at. It winds back at 0.22,
drives through at 0.34 and has recovered by 0.5.

An arm that extends along x cannot swing on x, because that is the axis it lies
along; rotating it there only rolls the blade like a propeller. The lift is z
and the drive forward is y, and each reads the opposite way on the two sides,
so the left arm raises on +z and the right on -z. Everything below the shoulder
trails, the forearm behind the arm and the blade behind the forearm. That lag is
the whole of the weight.

Idle runs those same two axes at a fifth of the amplitude, and deliberately in
step rather than mirrored, which for arms on opposite sides means one axe is
always drifting up while the other settles. A Kleavor standing still is never
quite still.

Its texture is painted off the model the way Arboliva's is, with one extra
rule. An axe arm is three cubes of two materials, a stone wrist and the two
slabs that make the blade. Every plate is drawn inside a dark border, because
Kleavor is one flat tan from the collar down and without an outline per cube
the chest, the hanging plate and both thighs merge into a single mass at mob
scale.

### Squirtle's four states

The controller picks between idle, waddle, swim and withdraw, in that order of
precedence, off `query.is_sitting`, `query.is_in_water` and
`query.modified_move_speed`.

The waddle is a two-legged gait, so the legs swing in opposite phase and the
arms counter them. The number that matters is the body's vertical bob. A leg
rotated away from vertical lifts its own foot, so the hips have to rise with
it or the feet sink into the ground. With a 3-unit leg swinging 40 degrees the
lift is `3 * (1 - cos 40°)`, about 0.7, and it peaks where the swing peaks.
That is why the bob is `cos²` of the stride phase and not `|cos|` or a plain
sine. Change either the leg length or the 40 and the 0.7 has to move with them.

The stride constant is 26, set when Pikachu's was 24. Pikachu's is now 66,
because `modified_distance_moved` counts about four units per block and 24
stretched one stride over nearly four blocks. Squirtle has the same fault and
this change did not touch it.

Swimming pitches the whole body 48 degrees nose-down and the head cancels 34 of
that, so it looks along its own path instead of at the riverbed. Arms row and
legs kick on the same 300-degree-a-second beat in opposite phase, and the tail
runs a slower wave with each segment lagging the one ahead by 50 degrees, which
is what makes it read as a rudder rather than a flag.

Withdraw is the sit pose, because that is what a turtle does when it stays put.
Head, arms, legs and tail all scale down between 0.4 and 0.5 and slide inward,
which drops them inside a shell that stays full size. Only Moltres's flames
animate `scale` anywhere else in the pack. A slow `life_time` sway on the head and tail keeps a withdrawn
Squirtle from reading as a dropped prop.

### Moltres's wingbeat

Each wing is three bones chained outward, `wing`, `wingmid` and `wingtip`, and
the flap runs one sine through all three with each joint 40 degrees behind the
one inside it. That lag is the whole thing. A wing on a single bone beats like
a plank; the same wing on three with a lag rolls the stroke out to the tip the
way a real one does. A quarter cycle ahead of the roll each joint also pitches,
and the pitch grows outward, so the tip turns its leading edge into the stroke
and the shoulder barely moves.

Everything that burns hangs off whatever it burns on. The six flame sheets on a
wing are children of the joint they sit on, so they inherit the beat for free
and only have to add the flicker on top. That flicker is a rotation and a scale
on one clock, offset per bone by its position in the list so no two flames are
in phase. The scale is what makes it work. A flame that only leans reads as a
wobbling plate, and one that also swells and shrinks reads as fire.

Head tracking is spread down the neck instead of landing on the skull. The
three neck bones take a fifth to a quarter of `query.target_x_rotation` and
`query.target_y_rotation` each and the head takes the last three tenths. A bird
turns to look with its whole neck, and the full angle on one bone snaps the
beak off the end of it. This is the opposite call from Rayquaza, whose head
hangs off `root` precisely so tracking does not drag the body, and the two
differ because five blocks of serpent behind the skull is a lot to drag and
three short neck bones is not.

The three gaits differ only in numbers. Hovering beats 26 degrees at 90 a
second with the legs hanging. Gliding drops to 9 degrees at 55, tips the body
6 degrees onto its line of flight, straightens the neck and folds the legs back
under the tail. Hunting is 34 degrees at 190, beak open 26, talons swung
forward. The controller picks between them on `query.has_target` and
`query.modified_move_speed`, the same way Rayquaza's does.

Fifty-one cubes is more UV than survives being kept in two places, so the model
and the clips both come out of `tools/gen_moltres.py`, which shelf-packs the
net, and the Moltres half of `gen_textures.py` reads those slots back out of
the model. Change the model and both have to run again, in that order.

### Lapras's four states

The controller picks between idle, walk, swim and rest, in that order of
precedence, off `query.is_sitting`, `query.is_in_water` and
`query.modified_move_speed`, which is the shape Squirtle's uses.

Everything with a chain in it runs Arboliva's rule, each link lagging the one
above it and swinging further. The neck is three links with the head on the end
and an ear of four links hanging off that, so the run from shoulder to ear tip
is eight joints deep and no two of them are in step. That is what stops the
neck reading as one rod.

The land walk is a drag rather than a gait. Lapras has no legs, so the four
paddles row against the ground on the diagonal, front left with rear right, and
the body rolls six degrees into each stroke. The arithmetic worth knowing is
the sign. A paddle lies along x, so its fore and aft sweep is a rotation about
y, and a rotation about y reads the opposite way on the two sides, positive
swinging the left tip forward and the right tip back. Pair that with a diagonal
gait, which already puts the two sides half a cycle apart, and the two sign
flips cancel: mirrored flippers end up carrying the same number. It looks like
a copy-paste error in the file and is correct on the screen. The lift is z, and
that one does mirror, so the left paddle rises on positive and the right on
negative.

The stride constant is 14, against Squirtle's 26 and Pikachu's 24. It sets
stride length rather than cadence and it follows the body, and this body is
three times the length of Squirtle's.

Swimming is the gait Lapras is built for, so it runs off `query.life_time`
rather than distance moved and keeps beating while the mob holds station. Both
front paddles beat together through 30 degrees at 190 a second, with a 12
degree feather a quarter cycle out, which is the underwater flight stroke a sea
turtle uses rather than a fish's tail. The rear pair follows 55 degrees late at
half the amplitude and steers. The body pitches five degrees nose down and the
neck puts three of them back, so Lapras looks along its path with its throat
clear of the water.

Rest is the sit pose and it is a swan curve. The neck leans 19, 15 and -9
degrees back over the shell and the head pitches 24 forward off the end, so the
head finishes level while the neck folds under it. The paddles flatten out of
their resting roll, and a slow `life_time` sway stays on the neck, the ears and
the tail, so a sitting Lapras still reads as alive.

## Known gaps

No custom sounds. Adding them means shipping `.ogg` files plus a
`sounds/sound_definitions.json`, and wiring `minecraft:ambient_sound_interval`
in the behavior pack. Thunder Shock borrows vanilla `cast.spell` and
`random.fizz`, Oil Salvo and Water Gun both borrow `random.bow` and
`random.splash`, and Ice Beam borrows `cast.spell` and `random.glass`.

No cheek-spark particles on the caster, and no aroma burst on Arboliva. Bedrock
has no event hook on `minecraft:behavior.ranged_attack`, so both need a
scripting-API listener or a melee-driven animation controller instead.

Kleavor's chop is untested in game. `query.is_delayed_attacking` is the query
the ravager's attack animation reads, and the controller here is wired the same
way, but nothing has confirmed the swing lands on the same frame as the damage.

Squirtle has no Rain Dish. The hidden ability heals a sixteenth of max health a
turn in rain, and Bedrock has no heal-over-time component to hang that on, so
it would need the scripting API.

Squirtle is untested in game. Torrent leans on `minecraft:environment_sensor`
and the `actor_health` filter, and it guards itself against re-firing by
swapping `minecraft:type_family` to carry a `torrent` family that the sensor
then tests for. That guard is the part most likely to be wrong, and the symptom
would be the component group being re-added every tick rather than once. The
withdraw pose is also the only place in the pack that animates bone `scale`.

Moltres is untested in game. Berserk is wired the same way as Squirtle's
Torrent, an `minecraft:environment_sensor` on `actor_health` guarded by a
`berserk` family it swaps into `minecraft:type_family`, so it carries the same
risk: if the guard does not hold, the component group is re-added every tick
instead of once. It is also the first mob here that attacks a player who has
not touched it, and the first to hand out a status effect, three seconds of
wither off `minecraft:attack`. Whether 120 health and an 8-damage bird that
comes at you at night is a fair fight or a nuisance is a question only playing
it answers.

Lapras is untested in game, and three things about it are guesses. Riding on
water leans on `minecraft:input_ground_controlled` with amphibious navigation,
which the reference documents for a ground mount and not for a swimming one; if
the controls do not answer in water, the swap to try is Rayquaza's
`minecraft:input_air_controlled`. Sitting and riding are layered on the same
interact, with `crouching_skip_interact` on the rideable meant to drop a
crouching interact through to `minecraft:sittable`, and nothing has confirmed
the two do not fight over it. And Water Absorb reads a `water_move` family off
the damaging entity through the same `any_of` over `damager` and `other` that
the Poké Ball trigger uses, so if that resolution is wrong the jets land for
full damage instead of none.

Lapras has no Sing, no Perish Song and no Hydration. The first two need a sound
file the pack does not ship, and Hydration needs a heal-over-time component
Bedrock does not have.

Riding Rayquaza is untested in game. `minecraft:input_air_controlled` is what
the reference documents for three-dimensional WASD control of a mount, but no
vanilla mob uses it; the happy ghast steers with `minecraft:free_camera_controlled`
plus `minecraft:vertical_movement_action` instead. If the controls do not answer,
those two are the swap to try, and they will raise the pack's floor above
`min_engine_version` 1.21.0.

## Credits and license

The code, the JSON and the generator scripts in this repository are MIT
licensed. See [LICENSE](LICENSE).

Pokémon, the Poké Ball, and the names and designs of Pikachu, Arboliva,
Rayquaza, Kleavor and Squirtle belong to Nintendo, Creatures Inc. and GAME
FREAK Inc. This is an unofficial fan project, it is not affiliated with or
endorsed by any of them, and it is not for sale.

Minecraft is a trademark of Mojang Studios. This add-on is not an official
Minecraft product and is not approved by or associated with Mojang or
Microsoft.
