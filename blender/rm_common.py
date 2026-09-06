"""Shared helpers for The Reality Machine's Blender blockout scripts.

Everything here is headless-safe: it runs under `blender --background --python`.

Conventions (see ../PIPELINE.md):
  * Build in metres. 1 Blender unit = 1 m = 100 Unreal units.
  * Boxes are built by hand rather than with primitive ops so that size is
    baked into the vertices and every object ships with a clean 1,1,1 scale.
  * Static meshes are SM_<Area>_<Thing>. Collision hulls are UCX_<meshname>_NN.
  * Gameplay positions are Empties, exported to markers.json for Unreal.
"""

import json
import math
import os

import bpy

# --- scene ------------------------------------------------------------------


def reset_scene():
    """Delete everything and return an empty metric scene."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras,
                  bpy.data.lights):
        for item in list(block):
            if item.users == 0:
                block.remove(item)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = "METERS"
    return scene


def collection(name):
    """Get or create a top-level collection and make it active."""
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)

    layer = bpy.context.view_layer.layer_collection.children.get(col.name)
    if layer is not None:
        bpy.context.view_layer.active_layer_collection = layer
    return col


def _link(obj, col):
    for existing in list(obj.users_collection):
        existing.objects.unlink(obj)
    col.objects.link(obj)
    return obj


# --- geometry ---------------------------------------------------------------


def box(name, size, location=(0.0, 0.0, 0.0), rotation_z=0.0, col=None):
    """A box with its size baked into the mesh, origin at its own centre.

    size and location are metres; rotation_z is degrees.
    """
    sx, sy, sz = (s / 2.0 for s in size)
    verts = [
        (-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
        (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz),
    ]
    faces = [
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0),
    ]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = (0.0, 0.0, math.radians(rotation_z))
    return _link(obj, col or bpy.context.scene.collection)


def room(name, inner, wall=0.12, col=None, door=None, floor=True, ceiling=True):
    """Four walls (plus optional floor/ceiling) around an inner volume.

    inner is the interior (x, y, z) in metres, measured to the inside faces.
    door is (wall, width) where wall is one of -x +x -y +y; that wall is built
    in two pieces with a gap of the given width in the middle.
    """
    ix, iy, iz = inner
    parts = []
    if floor:
        parts.append(box(f"SM_{name}_Floor", (ix + wall * 2, iy + wall * 2, wall),
                         (0, 0, -wall / 2), col=col))
    if ceiling:
        parts.append(box(f"SM_{name}_Ceiling", (ix + wall * 2, iy + wall * 2, wall),
                         (0, 0, iz + wall / 2), col=col))

    door_wall, door_w = door if door else (None, 0.0)
    for side, sign, axis in (("-x", -1, "x"), ("+x", 1, "x"),
                             ("-y", -1, "y"), ("+y", 1, "y")):
        along = iy if axis == "x" else ix
        centre = ((sign * (ix + wall) / 2, 0, iz / 2) if axis == "x"
                  else (0, sign * (iy + wall) / 2, iz / 2))
        span = (wall, along + wall * 2, iz) if axis == "x" else (along + wall * 2, wall, iz)

        if side != door_wall:
            parts.append(box(f"SM_{name}_Wall_{side.replace('-','N').replace('+','P')}",
                             span, centre, col=col))
            continue

        # Split this wall around a doorway.
        leaf = (along - door_w) / 2.0
        offset = (door_w + leaf) / 2.0
        for tag, direction in (("A", -1), ("B", 1)):
            if axis == "x":
                piece_span = (wall, leaf, iz)
                piece_loc = (centre[0], direction * offset, centre[2])
            else:
                piece_span = (leaf, wall, iz)
                piece_loc = (direction * offset, centre[1], centre[2])
            parts.append(box(
                f"SM_{name}_Wall_{side.replace('-','N').replace('+','P')}_{tag}",
                piece_span, piece_loc, col=col))
    return parts


def cylinder(name, radius, depth, location=(0, 0, 0), verts=24, col=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius,
                                        depth=depth, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    return _link(obj, col or bpy.context.scene.collection)


def torus(name, major, minor, location=(0, 0, 0), rotation=(0, 0, 0), col=None):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major, minor_radius=minor, location=location,
        rotation=[math.radians(a) for a in rotation],
        major_segments=32, minor_segments=12)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    return _link(obj, col or bpy.context.scene.collection)


def collision_for(obj, index=1, col=None):
    """A UCX box hull matching an object's bounds — Unreal picks it up on import."""
    dims = obj.dimensions
    hull = box(f"UCX_{obj.name}_{index:02d}",
               (max(dims.x, 0.01), max(dims.y, 0.01), max(dims.z, 0.01)),
               tuple(obj.location), col=col)
    hull.display_type = "WIRE"
    return hull


# --- markers ----------------------------------------------------------------

_MARKERS = []


def marker(name, location, kind="Interactable", note="", rotation_z=0.0, col=None):
    """An Empty that names a gameplay position. Also recorded for markers.json."""
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "ARROWS"
    obj.empty_display_size = 0.5
    obj.location = location
    obj.rotation_euler = (0.0, 0.0, math.radians(rotation_z))
    obj["rm_kind"] = kind
    obj["rm_note"] = note
    _link(obj, col or bpy.context.scene.collection)

    _MARKERS.append({
        "name": name,
        "kind": kind,
        "note": note,
        # Unreal units, and Unreal's left-handed Y. See PIPELINE.md.
        "location_uu": [round(location[0] * 100, 2),
                        round(-location[1] * 100, 2),
                        round(location[2] * 100, 2)],
        "yaw": rotation_z,
    })
    return obj


def write_markers(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        json.dump({"units": "unreal_cm", "markers": _MARKERS}, handle, indent=2)
    print(f"[rm] wrote {len(_MARKERS)} markers -> {path}")
    return path


def calibration_cube(col=None):
    """Exactly 2 m. It must measure 200 uu in Unreal — see PIPELINE.md."""
    return box("SM_ZZ_CalibrationCube_2m", (2.0, 2.0, 2.0), (0, 0, 1.0), col=col)
