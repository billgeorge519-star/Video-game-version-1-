#!/usr/bin/env bash
# Build every world's blockout and export it for Unreal.
#
#   ./scripts/build_all.sh              # data + all blockouts + FBX
#   ./scripts/build_all.sh --data-only  # data tables and catalog only, no Blender
#
# Set BLENDER=/path/to/blender if it is not on your PATH.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
BLENDER="${BLENDER:-blender}"

echo "==> data tables, markers and world catalog"
python3 "$HERE/gen_data.py"

echo "==> world atlas"
python3 "$HERE/gen_atlas.py"

if [ "${1:-}" = "--data-only" ]; then
  echo "==> done (data only)"
  exit 0
fi

if ! command -v "$BLENDER" >/dev/null 2>&1; then
  echo "!! Blender not found as '$BLENDER'."
  echo "   Install it (https://www.blender.org/download/) or set BLENDER=/path/to/blender."
  echo "   Everything above was still generated."
  exit 1
fi

echo "==> blockouts (this takes a minute)"
"$BLENDER" --background --python "$ROOT/blender/build_world.py" -- --all --fbx

echo
echo "==> done"
echo "    blend    $ROOT/build/blend/"
echo "    fbx      $ROOT/build/fbx/       -> import into Unreal"
echo "    markers  $ROOT/build/markers/"
echo "    tables   $ROOT/build/unreal/    -> import as DataTables"
