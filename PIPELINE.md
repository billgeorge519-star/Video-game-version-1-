# Blender → Unreal pipeline

The settings on this page are a contract. Change one and every asset in the
project shifts, rotates or rescales — so change it once, deliberately, and
re-export everything.

---

## The one number that matters

**1 Blender metre = 100 Unreal units.**

Model in metres. The FBX exporter carries the conversion. Every scene the
builder generates includes `SM_ZZ_CalibrationCube_2m` — a cube exactly 2 m on
each side.

**Verify it in thirty seconds:** import any world's FBX, select the calibration
cube, and read its bounds in the Details panel. It must say **200 × 200 × 200
uu**. If it says 2, the unit scale was dropped; if it says 20000, it was applied
twice. Fix the export settings, not the individual asset.

## Axes

| | Blender | Unreal |
|---|---|---|
| Up | +Z | +Z |
| Forward | −Y | +X |
| Handedness | right | left |

The exporter uses `axis_forward="-Z"`, `axis_up="Y"`. The Y flip is why
`scripts/gen_data.py` negates Y when it writes Unreal coordinates — that
negation is deliberate, not a bug.

## FBX export settings

All defined once in `blender/export_fbx.py` as `UNREAL_FBX`:

| Setting | Value | Why |
|---|---|---|
| Scale | 1.0 | Metres in, unit conversion carried by the file |
| Apply Scalings | `FBX_SCALE_UNITS` | Puts the metre→centimetre factor in the FBX header |
| Forward / Up | `-Z` / `Y` | Unreal's convention |
| Object types | MESH, EMPTY | Empties become the gameplay markers |
| Smoothing | Face | Unreal warns and guesses without it |
| Tangent space | on | Correct normal maps |
| Leaf bones | off | They pollute every skeleton in Unreal |
| Textures | not embedded | Textures are authored and owned in Unreal |

## Naming

| Prefix | For | Example |
|---|---|---|
| `SM_` | Static mesh | `SM_Trailer_Couch` |
| `SK_` | Skeletal mesh | `SK_Explorer` |
| `UCX_<mesh>_NN` | Convex collision | `UCX_SM_Trailer_Couch_01` |
| `INT_` | Interactable marker | `INT_The_Bust` |
| `PORTAL_` | Portal marker | `PORTAL_Arrival` |
| `T_`, `M_`, `MI_` | Texture, material, instance | `M_Neon_Base` |

Unreal picks up `UCX_` hulls automatically when *Auto Generate Collision* is
**off** in the import dialog. Leave it off. Generated collision on a greybox is
usually wrong in the one place a player will find it.

## Import settings in Unreal

Static meshes:

- **Import Uniform Scale** 1.0 — the FBX already carries the conversion
- **Auto Generate Collision** off — use the `UCX_` hulls
- **Combine Meshes** off — one asset per object, so a single prop can be replaced
- **Generate Lightmap UVs** on
- **Build Nanite** on for anything that will be seen up close

Levels: import the FBX into `/Game/Blockout/<World>/` and drag it into the map,
or use `build/markers/<world>.json` to place gameplay actors from the data.

## LODs and the platform floor

The multiverse has to run on a Switch as well as a tower (GDD 21). Budget the
blockout with the floor in mind:

| Tier | Triangles per prop | Texture | Lighting |
|---|---|---|---|
| High (PC / PS5 / Series X) | Nanite, unbudgeted | 4K | Lumen |
| Mid (Series S, older PC) | ≤ 20k | 2K | Lumen, reduced |
| Floor (Switch-class) | ≤ 8k, 3 LODs | 1K | Baked / distance fields |

A world that only works on the top tier is a world that ships on one platform.

## Materials

Author materials in Unreal, not Blender. Blender's job is form; Unreal owns
shading, because that is where the reactive, sound-driven, world-changing
material behaviour in GDD 18 and 19 lives. Export vertex colours where they
carry meaning — the blockout uses them for nothing yet, so they are free for
masking later.

## What lives where

```
blender/world_data.py       every world, as data — THE source of truth
blender/build_world.py      generates the blockout scenes
blender/export_fbx.py       the export contract
scripts/gen_data.py         Unreal DataTables + markers + world catalog
scripts/gen_atlas.py        the visual atlas page
unreal/                     project file and engine config
build/                      generated; safe to delete and regenerate
```

Add a world to `world_data.py` and the blockout, the data tables, the markers,
the catalog and the atlas all update together. Nothing is hand-maintained
twice.
