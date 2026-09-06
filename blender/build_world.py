"""Blockout builder — turns world_data.py into real Blender scenes.

Headless usage (from the repo root):

    blender --background --python blender/build_world.py -- --world living_city
    blender --background --python blender/build_world.py -- --all
    blender --background --python blender/build_world.py -- --all --fbx

Each world produces:
    build/blend/<world>.blend      the editable blockout
    build/fbx/<world>.fbx          Unreal-ready geometry (with --fbx)
    build/markers/<world>.json     gameplay marker transforms, in Unreal units

The geometry is deliberately grey boxes at true scale. It exists so the space
can be walked, timed and playtested before a single asset is sculpted — the
blockout is the level design, the art comes later.
"""

import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import bpy                                                    # noqa: E402
import rm_common as rm                                        # noqa: E402
from world_data import WORLDS                                 # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build"))


def build_ground(world, col):
    ground = world.get("ground")
    if not ground:
        return None
    x, y = ground["size"]
    return rm.box("SM_World_Ground", (x, y, 1.0), (0, 0, -0.5), col=col)


def build_structures(world, col):
    """Grey-box every generated structure. Kind drives the primitive used."""
    made = []
    for i, part in enumerate(world["structures"]):
        name = f"SM_{part['kind'].title().replace('_', '')}_{i:03d}"
        loc, size, rot = part["loc"], part["size"], part.get("rot", 0.0)
        if part["kind"] in ("stalk", "core", "cabinet"):
            obj = rm.cylinder(name, radius=max(size[0], 0.1) / 2, depth=size[2],
                              location=loc, col=col)
            obj.rotation_euler.z = rot * 3.14159265 / 180.0
        elif part["kind"] == "portal_frame":
            obj = rm.torus(name, major=size[0] / 2, minor=0.5, location=loc,
                           rotation=(90, 0, rot), col=col)
        else:
            obj = rm.box(name, size, loc, rotation_z=rot, col=col)
        made.append(obj)
    return made


def build_trailer_shell(col):
    """The one hand-authored space: 3 m x 9 m interior, 2.5 m ceiling."""
    rm.room("Trailer", inner=(3.0, 9.0, 2.5), wall=0.12, col=col,
            door=("+x", 1.0))
    rm.box("SM_Trailer_Step", (1.4, 1.2, 0.18), (2.3, 0.0, -0.09), col=col)
    rm.box("SM_Trailer_Deck", (4.0, 3.0, 0.12), (4.2, -1.0, -0.06), col=col)
    # Furniture blockout — replaced by real assets, sized so the space reads now.
    rm.box("SM_Trailer_Couch", (0.9, 2.0, 0.8), (-1.0, -0.4, 0.4), col=col)
    rm.box("SM_Trailer_Table", (0.8, 1.0, 0.45), (0.2, -0.6, 0.22), col=col)
    rm.box("SM_Trailer_Bed", (1.4, 2.0, 0.5), (-0.7, -3.2, 0.25), col=col)
    rm.box("SM_Trailer_Bench", (0.7, 1.8, 0.9), (1.1, -2.2, 0.45), col=col)
    rm.box("SM_Trailer_Counter", (0.6, 2.4, 0.9), (1.15, 1.6, 0.45), col=col)
    # The machine itself: a ring on a plinth at the far end.
    rm.box("SM_Machine_Plinth", (1.6, 0.8, 0.4), (0.0, 3.6, 0.2), col=col)
    rm.torus("SM_Machine_Ring", major=0.9, minor=0.12, location=(0.0, 3.6, 1.3),
             rotation=(90, 0, 0), col=col)
    for i in range(3):
        rm.cylinder(f"SM_Trailer_Pedestal_{i + 1:02d}", radius=0.18, depth=1.0,
                    location=(-1.1, 1.4 - i * 1.2, 0.5), col=col)
    rm.box("SM_Trailer_WeaponWall", (0.1, 2.2, 1.2), (1.44, 0.6, 1.4), col=col)


def build(world_id, want_fbx=False):
    world = WORLDS[world_id]
    rm.reset_scene()
    rm._MARKERS.clear()

    shell = rm.collection("SHELL")
    props = rm.collection("PROPS")
    markers = rm.collection("MARKERS")

    if world["kind"] == "home":
        build_trailer_shell(shell)
    else:
        build_ground(world, shell)
        build_structures(world, props)

    rm.collection("PROPS")
    rm.calibration_cube(props)

    # Arrival portal, and one marker per interactable.
    rm.marker("PORTAL_Arrival", tuple(world["portal"]), kind="Portal",
              note="Where players arrive and where the ejection portal opens.",
              col=markers)
    for thing in world["interactables"]:
        safe = "".join(c if c.isalnum() else "_" for c in thing["name"]).strip("_")
        rm.marker(f"INT_{safe}", tuple(thing["at"]), kind="Interactable",
                  note=thing["does"], col=markers)

    os.makedirs(os.path.join(ROOT, "blend"), exist_ok=True)
    blend = os.path.join(ROOT, "blend", f"{world_id}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    rm.write_markers(os.path.join(ROOT, "markers", f"{world_id}.json"))
    print(f"[rm] built {world['name']}  ->  {blend}")

    if want_fbx:
        import export_fbx
        export_fbx.export(os.path.join(ROOT, "fbx", f"{world_id}.fbx"))
    return blend


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="build_world")
    ap.add_argument("--world", help="world id from world_data.WORLDS")
    ap.add_argument("--all", action="store_true", help="build every world")
    ap.add_argument("--fbx", action="store_true", help="also export FBX for Unreal")
    ap.add_argument("--list", action="store_true", help="list world ids and exit")
    args = ap.parse_args(argv)

    if args.list:
        for key, world in WORLDS.items():
            print(f"{key:18} {world['name']}")
        return
    targets = list(WORLDS) if args.all else [args.world or "trailer"]
    for world_id in targets:
        if world_id not in WORLDS:
            raise SystemExit(f"unknown world '{world_id}' — try --list")
        build(world_id, want_fbx=args.fbx)


if __name__ == "__main__":
    main()
