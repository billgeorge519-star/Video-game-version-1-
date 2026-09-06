"""Invariants for the world data.

These are the checks that actually caught bugs while the roster was written:
two worlds built from an identical set of shapes (they read as the same place),
and objects that drifted into sharing a name. Run them with:

    python3 -m unittest discover -s tests -v
"""

import ast
import os
import subprocess
import sys
import unittest
from collections import Counter
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "blender"))

from world_data import WORLDS  # noqa: E402


class WorldShape(unittest.TestCase):
    """Every world carries the fields the builder and the exporters read."""

    def test_required_fields(self):
        for key, world in WORLDS.items():
            with self.subTest(world=key):
                for field in ("name", "tagline", "kind", "rules", "portal",
                              "structures", "interactables"):
                    self.assertIn(field, world, f"{key} is missing '{field}'")
                self.assertEqual(len(world["portal"]), 3,
                                 f"{key} portal must be [x, y, z]")
                self.assertIn(world["kind"], ("home", "hub", "reality"))

    def test_rules_are_usable(self):
        for key, world in WORLDS.items():
            with self.subTest(world=key):
                gravity = world["rules"].get("gravity", 1.0)
                self.assertTrue(
                    isinstance(gravity, (int, float)) or gravity == "variable",
                    f"{key} gravity must be a number or the string 'variable'")
                pvp = world["rules"].get("pvp", False)
                self.assertIn(pvp, (True, False, "zoned"),
                              f"{key} pvp must be True, False or 'zoned'")

    def test_structures_are_well_formed(self):
        for key, world in WORLDS.items():
            for i, part in enumerate(world["structures"]):
                with self.subTest(world=key, index=i):
                    self.assertIn("kind", part)
                    self.assertEqual(len(part["loc"]), 3)
                    self.assertEqual(len(part["size"]), 3)
                    self.assertTrue(all(v > 0 for v in part["size"]),
                                    f"{key} structure {i} has a zero dimension")


class Interactables(unittest.TestCase):
    """The 218 discoverable objects are the content. They get checked hardest."""

    def test_every_object_is_complete(self):
        for key, world in WORLDS.items():
            for thing in world["interactables"]:
                with self.subTest(world=key, obj=thing.get("name")):
                    for field in ("name", "at", "prompt", "does"):
                        self.assertTrue(thing.get(field),
                                        f"{key}/{thing.get('name')} has no '{field}'")
                    self.assertEqual(len(thing["at"]), 3)
                    self.assertTrue(all(isinstance(v, (int, float))
                                        for v in thing["at"]))

    def test_names_are_unique_across_the_multiverse(self):
        """Two objects sharing a name makes the data tables ambiguous."""
        names = [t["name"] for w in WORLDS.values() for t in w["interactables"]]
        dupes = [n for n, count in Counter(names).items() if count > 1]
        self.assertEqual(dupes, [], f"duplicate object names: {dupes}")

    def test_every_world_has_something_to_find(self):
        for key, world in WORLDS.items():
            with self.subTest(world=key):
                self.assertGreaterEqual(
                    len(world["interactables"]), 8,
                    f"{key} has too little to discover to be worth visiting")

    def test_prompts_are_short_enough_to_be_a_prompt(self):
        for key, world in WORLDS.items():
            for thing in world["interactables"]:
                with self.subTest(world=key, obj=thing["name"]):
                    self.assertLessEqual(
                        len(thing["prompt"]), 40,
                        "an interact prompt is a few words on screen, not a sentence")


class WorldsAreDistinct(unittest.TestCase):
    """The point of nineteen worlds is that they are nineteen different places."""

    def test_no_two_worlds_share_a_structure_vocabulary(self):
        signatures = {
            key: tuple(sorted(Counter(s["kind"] for s in world["structures"])))
            for key, world in WORLDS.items()
        }
        clashes = [(a, b) for a, b in combinations(signatures, 2)
                   if signatures[a] == signatures[b] and signatures[a]]
        self.assertEqual(clashes, [],
                         f"worlds built from identical shapes: {clashes}")

    def test_names_and_taglines_are_distinct(self):
        for field in ("name", "tagline"):
            values = [w[field] for w in WORLDS.values()]
            dupes = [v for v, c in Counter(values).items() if c > 1]
            self.assertEqual(dupes, [], f"duplicate {field}: {dupes}")


class Determinism(unittest.TestCase):
    """Seeded layouts: the same file must always describe the same place."""

    def test_layouts_are_reproducible(self):
        import importlib
        import world_data
        before = [s["loc"] for s in WORLDS["living_city"]["structures"]]
        importlib.reload(world_data)
        after = [s["loc"] for s in world_data.WORLDS["living_city"]["structures"]]
        self.assertEqual(before, after,
                         "world layout changed between two loads of the same data")


class BlenderScriptsParse(unittest.TestCase):
    """CI has no Blender, but a syntax error is still catchable here."""

    def test_scripts_are_valid_python(self):
        for name in ("rm_common.py", "build_world.py", "export_fbx.py"):
            path = os.path.join(ROOT, "blender", name)
            with self.subTest(script=name):
                with open(path) as handle:
                    ast.parse(handle.read(), filename=path)


class GeneratedFilesAreCurrent(unittest.TestCase):
    """WORLDS.md and the data tables are committed; they must match the data.

    Note this test has a side effect: it runs the generator, so a stale
    generated file in your working tree is rewritten in place. That is the fix
    anyway — but it means a local failure leaves you with the corrected files
    already written, needing only a commit.
    """

    def test_regenerating_changes_nothing(self):
        if not os.path.isdir(os.path.join(ROOT, ".git")):
            self.skipTest("not a git checkout")
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "gen_data.py")],
                       check=True, capture_output=True, cwd=ROOT)
        diff = subprocess.run(["git", "diff", "--name-only"],
                              check=True, capture_output=True, text=True, cwd=ROOT)
        stale = [line for line in diff.stdout.split() if line]
        self.assertEqual(
            stale, [],
            "generated files did not match the world data. The generator has "
            "just been run for you, so these files are now correct — commit "
            f"them: {stale}")


if __name__ == "__main__":
    unittest.main()
