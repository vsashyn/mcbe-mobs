# Pokémon

A Minecraft Bedrock add-on with five custom mobs. `pk:pikachu` is a tameable
electric mob that fights with a Thunder Shock projectile. `pk:arboliva` is a
tameable olive tree that answers with a six-shot volley of oil. `pk:rayquaza`
is the black shiny Rayquaza, a five-block sky serpent that never lands.
`pk:kleavor` has axes for hands and no ranged attack at all. `pk:squirtle` is
the water starter: it swims, it shoots Water Gun, and it hits harder the closer
it gets to fainting.

The folders, the pack names and the built `.mcaddon` still say Pikachu, from
when it was the only mob here.

## Pikachu

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

## Arboliva

Arboliva is built as a tree, not as an animal with leaves on. A flared trunk
stands on two short roots, tapers through a pale segment that carries the face,
and finishes in a canopy of two overlapping slabs with a leaf blade sprouting
off the top. Four branches arch out on the diagonals from just under that
canopy, each one weeping back down into a wide leaf frond with an olive hanging
below it. Two more olives dangle from the canopy rim. It stands two blocks tall
and the canopy spreads about a block and a half across, so it overhangs its own
hitbox the way a tree should.

Wild Arboliva stand in bright savanna and forest, alone or in pairs. They are
slow, they keep clear of monsters, and they follow anyone holding bone meal.
Feed one bone meal and it has a 30% chance to tame per handful.

A tamed Arboliva follows its owner, sits and stays when you interact with it,
heals from bone meal and apples, and gets tougher (44 health, 5 attack damage
instead of 30 and 3). Two tamed adults fed apples or oak saplings will breed,
and the baby stands in for Dolliv at 45% scale.

Oil Salvo takes the card at its word. Six globs go out in one burst 0.2 seconds
apart, 2 damage each and two seconds of slowness where they land, from up to 14
blocks. The volley has a three block dead zone, so up close Arboliva swings its
branches instead. Being a two block tall tree, it also shrugs off knockback,
ignores poison and wither, and takes double from fire and lava. It has no panic
behavior either, so it stands its ground and burns.

On death it drops 0-2 sticks, an oak sapling, or a handful of bone meal.

## Black Rayquaza

`pk:rayquaza` is the shiny Rayquaza: charcoal where the ordinary one is
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

Air Lock is its ability in the games: it cancels the weather. Here it runs
`weather clear` whenever the sky is not clear, then sits out 30 seconds before
it will do that again. It needs commands allowed in the world. With cheats off
nothing breaks, the weather just stays.

Taming costs a meteorite. Feed it ancient debris, or a golden apple if you have
not reached the Nether yet, and it has a 34% chance to bond per feed. A tamed
Rayquaza carries 220 health, defends its owner, teleports to keep up, heals
from golden apples and ancient debris, and can be ridden: interact without
sneaking to mount, and `minecraft:input_air_controlled` puts WASD and the mouse
in charge of all three dimensions.

On death it drops 2-4 phantom membrane, plus dragon breath or, one roll in
four, the ancient debris back.

## Kleavor

`pk:kleavor` is the axe. Both arms end in a slab of stone wider than its head,
and the rest of the mob follows from that. It is the only one here with no
projectile, and the only one that would rather you came closer.

Wild Kleavor stand alone in forest and taiga, at any light. They leave players
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

## Squirtle

`pk:squirtle` is the only mob here that is as much at home in water as out of
it. It is a squat biped: a big round head over a cream plastron, a red-brown
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

Torrent is its ability, and here it does what the games say: below a third of
its health, Squirtle's water moves hit 1.5× harder. The shooter swaps from
`pk:water_gun` to `pk:water_gun_torrent`, 6 damage instead of 4, and swaps back
if it heals. Everything else about the attack stays the same, so Torrent is a
damage change and nothing else.

The shell is worth something and the type chart costs it. It shrugs off half of
any fall, fire, lava or burn damage and most knockback, breathes water so it
never drowns, and takes double from lightning, which is the exact opposite of
Pikachu.

On death it drops 0-2 prismarine shards, or a raw cod.

## Poké Ball

`pk:poke_ball` is an item you throw. It is the one thing in the pack that is
not a mob, and it is what turns the mobs into something you can carry.

Craft it from three red dye over two iron ingots with a redstone between them,
over three white dye. That makes two. Hold one and use it the way you would a
snowball.

A ball that hits a Pokémon either catches it or is wasted. A tamed one always
goes in, since it is already yours. A wild one resists, and Pikachu and
Arboliva go in three times in five, Kleavor one in two, Rayquaza one in five.
A ball that misses, hits a block, or fails to hold is gone.

A caught Pokémon leaves a ball lying where it stood, its button in the colour
of what is inside. Interact with that ball to pick it up as a full ball, named
for its occupant. Throw the full ball and the Pokémon comes out a third of a
second later, wherever the ball got to, tamed to whoever threw it.

So the ball is a one-way trip for a wild Pokémon and a pocket for a tame one.
A baby comes back grown, and nothing but the owner survives the trip: health,
sitting, name and age are all lost. Empty balls stack to 16, full ones do not
stack at all.

None of this needs the scripting API. The catch is a `definition_event` on the
thrown ball's `on_hit`, which fires `pk:on_captured` on whatever it hit. A mob
with no such event does nothing with it, which is why a cow shrugs the ball
off. The event hands the mob a `minecraft:transformation` into the ball that
lies on the ground, and the full ball transforms the other way on a 0.3 second
delay. `keep_owner` carries the thrower through both turns, which is what makes
the Pokémon that comes out belong to the player who threw it.

Covering a new mob means four files that name a species
(`entities/caught_<mob>.json`, `entities/poke_ball_<mob>_thrown.json`,
`items/poke_ball_<mob>.json`, `loot_tables/entities/caught_<mob>.json`), an
entry in `OCCUPANTS` in `gen_textures.py` and in `item_texture.json`, and the
`pk:caught` group plus the `pk:on_captured`, `pk:break_free` and
`minecraft:entity_transformed` events on the mob itself. `validate.py` catches
every one of those you forget except the last.

## Layout

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
  textures/entity/*/*.png
  animations/pikachu.animation.json   idle, quadruped run, sit, head tracking, spark
  animations/arboliva.animation.json  idle, walk, sit, head tracking, drip
  animations/rayquaza.animation.json  hover, glide, hunt, head tracking, spin
  models/entity/kleavor.geo.json      27 bones, 33 cubes, 128x128, no projectile
  animations/kleavor.animation.json   idle, walk, chop, sit, head tracking
  models/entity/squirtle.geo.json     11 bones on a 64x64 sheet, plus the jet
  animations/squirtle.animation.json  idle, waddle, swim, withdraw, head tracking
  models/entity/poke_ball.geo.json    five cubes on a 32x32 sheet, one bone
  animations/poke_ball.animation.json spin in flight, bob at rest
  textures/items/*.png                inventory icons, 16x16
  textures/item_texture.json          maps an icon name onto its png
  texts/en_US.lang                    every name the player reads
  animation_controllers/              picks idle vs walk vs sit, one per mob
  render_controllers/
tools/gen_rayquaza.py                 lays out Rayquaza's 46 cubes and its wave;
                                      run it before gen_textures.py
tools/gen_textures.py                 redraws every png; edit here, not in an image editor
                                      Arboliva's is painted off its .geo.json
tools/validate.py                     catches broken references before the game does
tools/bump_version.py                 raises the version in both manifests together
build.sh                              packs both folders into dist/Pikachu.mcaddon
```

`validate.py` walks every entity in the behavior pack rather than a named list,
so a new mob is checked the moment its files land. It ties an animation to a
geometry by name, so `animation.arboliva.walk` has to animate bones that
`geometry.arboliva` actually has, and it fails the build on a UV net that
overlaps another or runs off the sheet.

Box UV is fixed at one texel per model unit. That ties sheet size to model
size, so a mob cannot be made bigger without either a proportionally bigger
sheet or texels coarser than the rest of the game.

`gen_textures.py` keeps every mob's palette in one flat namespace at the top of
the file, so a new mob whose colour name collides with an older one silently
repaints the older mob. Nothing catches it: `validate.py` does not look at
pixels, and the only sign is an unrelated `.png` turning up in `git status`
after a run. Check that list against the mob you actually touched.

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
/give @s pk:arboliva_spawn_egg
/give @s pk:rayquaza_spawn_egg
/give @s pk:kleavor_spawn_egg
/give @s pk:squirtle_spawn_egg
/summon pk:pikachu ~ ~ ~
/summon pk:arboliva ~ ~ ~
/summon pk:rayquaza ~ ~10 ~
/summon pk:kleavor ~ ~ ~
/summon pk:squirtle ~ ~ ~
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

To see Water Gun, hit a Squirtle from a dozen blocks away and back off: it
answers with the jet, and closes to tackle if you come inside three blocks. To
see Torrent, `/effect @e[type=pk:squirtle,c=1] instant_damage 1 1` down to under
a third of its health and watch the jets get heavier.
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

## Pikachu's stances

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

## Arboliva's sway

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
over a long stride. The trunk rolls 4.5 degrees into each step and rides the double frequency, low
at full stride and high where a root passes vertical. The branches bounce on
that same double frequency, once per footfall, with a single-frequency sway
added on top so the bounce and the lean do not line up.

The number worth knowing about is the 18 that scales
`modified_distance_moved`. It sets stride length, not cadence, and it follows
the leg geometry, so it has to move whenever the legs do. Get it wrong and the
feet slide or stutter, which is the one animation fault this rig can have that
a still render will not show.

Sitting is a static pose with one exception. The olives and fronds keep a slow
`life_time` sway, so a sitting Arboliva still reads as alive.

## Rayquaza's flight

The rig is one chain: `neck`, then eight body segments, then the tail, each one
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
numbers: a fractional width makes a fractional UV net, and the net cannot land
on whole pixels.

## Kleavor's chop

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
trails: the forearm behind the arm, the blade behind the forearm. That lag is
the whole of the weight.

Idle runs those same two axes at a fifth of the amplitude, and deliberately in
step rather than mirrored, which for arms on opposite sides means one axe is
always drifting up while the other settles. A Kleavor standing still is never
quite still.

Its texture is painted off the model the way Arboliva's is, with one extra
rule: an axe arm is three cubes of two materials, a stone wrist and the two
slabs that make the blade. Every plate is drawn inside a dark border, because
Kleavor is one flat tan from the collar down and without an outline per cube
the chest, the hanging plate and both thighs merge into a single mass at mob
scale.

## Squirtle's four states

The controller picks between idle, waddle, swim and withdraw, in that order of
precedence, off `query.is_sitting`, `query.is_in_water` and
`query.modified_move_speed`.

The waddle is a two-legged gait, so the legs swing in opposite phase and the
arms counter them. The number that matters is the body's vertical bob. A leg
rotated away from vertical lifts its own foot, so the hips have to rise with
it or the feet sink into the ground: with a 3-unit leg swinging 40 degrees the
lift is `3 * (1 - cos 40°)`, about 0.7, and it peaks where the swing peaks.
That is why the bob is `cos²` of the stride phase and not `|cos|` or a plain
sine. Change either the leg length or the 40 and the 0.7 has to move with them.

The stride constant is 26. Squirtle's legs are the same length as Pikachu's, so
it sits near Pikachu's 24, a little quicker because a biped takes two steps to
a bound's one.

Swimming pitches the whole body 48 degrees nose-down and the head cancels 34 of
that, so it looks along its own path instead of at the riverbed. Arms row and
legs kick on the same 300-degree-a-second beat in opposite phase, and the tail
runs a slower wave with each segment lagging the one ahead by 50 degrees, which
is what makes it read as a rudder rather than a flag.

Withdraw is the sit pose, because that is what a turtle does when it stays put.
Head, arms, legs and tail all scale down between 0.4 and 0.5 and slide inward,
which drops them inside a shell that stays full size; nothing else in the pack
animates `scale`. A slow `life_time` sway on the head and tail keeps a withdrawn
Squirtle from reading as a dropped prop.

## Not done yet

No custom sounds. Adding them means shipping `.ogg` files plus a
`sounds/sound_definitions.json`, and wiring `minecraft:ambient_sound_interval`
in the behavior pack. Thunder Shock borrows vanilla `cast.spell` and
`random.fizz`, Oil Salvo and Water Gun both borrow `random.bow` and
`random.splash`.

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
then tests for; that guard is the part most likely to be wrong, and the symptom
would be the component group being re-added every tick rather than once. The
withdraw pose is also the only place in the pack that animates bone `scale`.

Riding Rayquaza is untested in game. `minecraft:input_air_controlled` is what
the reference documents for three-dimensional WASD control of a mount, but no
vanilla mob uses it; the happy ghast steers with `minecraft:free_camera_controlled`
plus `minecraft:vertical_movement_action` instead. If the controls do not answer,
those two are the swap to try, and they will raise the pack's floor above
`min_engine_version` 1.21.0.
