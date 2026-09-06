# The Reality Machine

A multiplayer psychedelic multiverse. You start in your trailer, walk into a
machine, and come out somewhere impossible. What you find, you bring home.

> Customize your character, enter a mysterious machine inside your personal
> trailer, travel into impossible shared realities, discover strange weapons and
> artifacts, explore with other players, and bring your discoveries home to build
> a personal museum of everything you've experienced.

**Original IP.** Inspired by psychedelic animated storytelling and immersive art
installations at the level of ideas — never copied from them. See GDD §2 and §47.

- **[`GDD.md`](GDD.md)** — the design document. Part I is the foundation;
  Part II documents the systems the concept boards add.
- **[`WORLDS.md`](WORLDS.md)** — every world and every discoverable object.
  Generated, not hand-written.
- **[`PIPELINE.md`](PIPELINE.md)** — Blender → Unreal, in exact settings.

---

## What is actually here

Not a game yet — the machine that builds one. Nineteen worlds exist as real
data: layouts, rules, and 218 things a player can walk up to and touch. From
that one file this kit generates 3D blockouts, Unreal data tables, gameplay
marker transforms, and a visual atlas.

| | |
|---|---|
| Spaces | 19 (1 home, 2 hubs, 16 realities) |
| Discoverable objects | 218, each with a prompt and a behaviour |
| Objects needing two players | 40 |
| Blockout structures | ~1,180, generated from seeds |

Nothing here is placeholder text. Every object has a position in metres, a
prompt, what it does, and — where it earns one — a secret or a reason to come
back.

## Ten-minute start

You need **Python 3** (already on most machines) and **Blender 4.x**
(free, blender.org). Unreal Engine 5.4+ when you are ready to walk the worlds.

```bash
# 1. Data tables, marker files and the world catalog. No Blender needed.
python3 scripts/gen_data.py

# 2. Everything, including 3D blockouts and Unreal-ready FBX.
./scripts/build_all.sh

# Just one world, while iterating:
blender --background --python blender/build_world.py -- --world living_city --fbx

# What worlds exist:
blender --background --python blender/build_world.py -- --list
```

Output lands in `build/`:

```
build/blend/<world>.blend      editable blockout scenes
build/fbx/<world>.fbx          import straight into Unreal
build/markers/<world>.json     gameplay marker transforms, in Unreal units
build/unreal/DT_Worlds.csv     world roster — import as a DataTable
build/unreal/DT_Interactables.csv   all 218 objects — import as a DataTable
build/atlas.html               the visual atlas of every world
```

## Then, in Unreal

1. Open `unreal/RealityMachine.uproject` (5.4+). The config already sets up
   multiplayer networking, EOS, Enhanced Input, Lumen and Nanite — multiplayer
   is wired from the start, per GDD 22, rather than retrofitted.
2. Import `build/fbx/trailer.fbx` into `/Game/Blockout/Trailer/`. Import
   Uniform Scale **1.0**, Auto Generate Collision **off**.
3. Check the calibration cube reads **200 uu** (see PIPELINE.md). Thirty
   seconds now saves a week later.
4. Import both CSVs as DataTables into `/Game/Data/`.
5. Walk the trailer. Then walk `living_city`. That is the vertical slice's
   first two spaces, at true scale, ready for a character controller.

## The toolchain

| Job | Tool | Cost |
|---|---|---|
| Modelling, sculpting, rigging, animation | **Blender 4.x** | free |
| Engine, multiplayer, lighting, AI, audio | **Unreal Engine 5.4+** | free until revenue |
| Accounts, friends, parties, matchmaking | **Epic Online Services** | free |
| Proximity voice (GDD 9) | **EOS Voice**, or Vivox / Odin | free tier |
| Scanned environment assets | **Fab / Quixel Megascans** | free tier |
| Textures | **Krita** or **GIMP**; Substance Painter if budget allows | free / paid |
| Audio editing | **Audacity** or **Reaper**; MetaSounds in-engine | free / cheap |
| Binary version control | **Git LFS** (see `unreal/.gitattributes`) | free |

Perforce is the industry default for a team over about five people; Git LFS is
fine until then, and the `.gitattributes` here is already set up for it.

## The rule that governs all of it

The game must be **original IP** (GDD 2). Several of the reference boards this
kit was built from contain third-party characters and names — they are mood
reference only, and GDD Part II 47 lists exactly what must be replaced and with
what. Check marquees, posters, screens and background signage before anything
is modelled; that is where borrowed IP survives unnoticed into a build.

## Checks

```bash
python3 -m unittest discover -s tests -v
```

Twelve checks, no dependencies, run on every push and pull request. They cover
the mistakes this data is actually prone to: two worlds built from an identical
set of shapes (they read as the same place), objects that drift into sharing a
name, an interact prompt that grew into a sentence, a world layout that stops
being reproducible, a syntax error in a Blender script CI cannot run, and
generated files committed out of date.

## Changing a world

Edit `blender/world_data.py` — nothing else. Add an entry to `WORLDS`, or add
an `obj(...)` to an existing world's `interactables`. Then re-run
`./scripts/build_all.sh` and commit what it regenerates. The blockout, the data
tables, the markers, the catalog and the atlas all follow. There is no second
place to keep in sync, and CI fails if you forget to commit the regenerated
files.

## Why grey boxes

The blockout is the level design. A space is walked, timed and playtested
before anything is sculpted — that is how you find out that the plaza is too
big and the corridor is too long, while those are still one number in a file.
Art comes after the space works.
