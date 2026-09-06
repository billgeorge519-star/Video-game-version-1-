"""FBX export with the settings Unreal Engine 5 expects.

These values are the contract with the engine — see ../PIPELINE.md. Change them
and every asset in the project shifts, rotates or rescales, so change them once
and re-export everything, never per-asset.
"""

import os

import bpy

UNREAL_FBX = dict(
    # Scale: build in metres, let FBX carry the unit conversion to centimetres.
    global_scale=1.0,
    apply_unit_scale=True,
    apply_scale_options="FBX_SCALE_UNITS",
    # Axes: Blender is Z-up/-Y-forward, Unreal is Z-up/+X-forward.
    axis_forward="-Z",
    axis_up="Y",
    use_space_transform=True,
    bake_space_transform=False,
    # Content
    object_types={"MESH", "EMPTY"},
    use_mesh_modifiers=True,
    mesh_smooth_type="FACE",
    use_tspace=True,
    colors_type="SRGB",
    # Rigs (off for blockouts; on for characters)
    add_leaf_bones=False,
    bake_anim=False,
    # Textures stay in Unreal, not in the FBX.
    path_mode="AUTO",
    embed_textures=False,
)


def export(filepath, selection_only=False):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=selection_only,
                             **UNREAL_FBX)
    print(f"[rm] exported FBX -> {filepath}")
    return filepath
