"""Every world in The Reality Machine, as data.

Pure Python on purpose: no `bpy` import, so this module is the single source of
truth for both the Blender blockout builder and the plain-Python exporters that
generate Unreal data tables and the human-readable world catalog.

Coordinates are metres, Blender-handed (+X right, +Y forward, +Z up). The
exporters convert to Unreal units and Unreal's flipped Y.

Structure layouts are generated from a fixed seed, so a blockout is
reproducible: same seed in, same city out. Interactables are hand-authored —
they are the content players actually come for (GDD Part I 16, Part II 46).
"""

import math
import random

# --- structure generators ---------------------------------------------------
# Each returns a list of dicts: {kind, loc:[x,y,z], size:[x,y,z], rot}


def _rng(world_id):
    return random.Random(f"reality-machine::{world_id}")


def grid_towers(world_id, count=40, spread=180.0, h=(12, 70), foot=(8, 22), lean=0):
    """A city: boxes on a jittered grid. `lean` degrees tilts them off true."""
    r = _rng(world_id)
    out, side = [], int(math.ceil(math.sqrt(count)))
    step = spread * 2 / side
    for i in range(count):
        gx, gy = i % side, i // side
        x = -spread + gx * step + r.uniform(-step * 0.25, step * 0.25)
        y = -spread + gy * step + r.uniform(-step * 0.25, step * 0.25)
        if math.hypot(x, y) < 22:           # keep the arrival plaza clear
            continue
        w, d = r.uniform(*foot), r.uniform(*foot)
        height = r.uniform(*h)
        out.append({"kind": "tower", "loc": [round(x, 2), round(y, 2), round(height / 2, 2)],
                    "size": [round(w, 2), round(d, 2), round(height, 2)],
                    "rot": round(r.uniform(-lean, lean) if lean else r.choice([0, 90]), 2)})
    return out


def floating_islands(world_id, count=26, spread=140.0, z=(4, 60)):
    r = _rng(world_id)
    out = []
    for _ in range(count):
        a, d = r.uniform(0, math.tau), r.uniform(18, spread)
        size = r.uniform(8, 34)
        out.append({"kind": "island",
                    "loc": [round(math.cos(a) * d, 2), round(math.sin(a) * d, 2),
                            round(r.uniform(*z), 2)],
                    "size": [round(size, 2), round(size * r.uniform(0.6, 1.4), 2),
                             round(r.uniform(1.5, 5.0), 2)],
                    "rot": round(r.uniform(0, 360), 2)})
    return out


def organic_clusters(world_id, count=34, spread=150.0, h=(6, 40)):
    """Grown things — stalks, coral, mushroom caps, trunks."""
    r = _rng(world_id)
    out = []
    for _ in range(count):
        a, d = r.uniform(0, math.tau), r.uniform(20, spread)
        height = r.uniform(*h)
        rad = r.uniform(1.5, 6.0)
        x, y = math.cos(a) * d, math.sin(a) * d
        out.append({"kind": "stalk", "loc": [round(x, 2), round(y, 2), round(height / 2, 2)],
                    "size": [round(rad, 2), round(rad, 2), round(height, 2)], "rot": 0})
        out.append({"kind": "cap", "loc": [round(x, 2), round(y, 2), round(height, 2)],
                    "size": [round(rad * r.uniform(2.5, 5.0), 2),
                             round(rad * r.uniform(2.5, 5.0), 2),
                             round(r.uniform(1.0, 3.5), 2)], "rot": 0})
    return out


def ruin_maze(world_id, cells=9, cell=14.0, wall_h=6.0):
    """A walled labyrinth on a grid, with gaps knocked through it."""
    r = _rng(world_id)
    out, half = [], cells * cell / 2
    for i in range(cells + 1):
        p = -half + i * cell
        for axis in ("x", "y"):
            for seg in range(cells):
                if r.random() < 0.38:        # knocked-through gap
                    continue
                q = -half + seg * cell + cell / 2
                loc = [p, q, wall_h / 2] if axis == "x" else [q, p, wall_h / 2]
                if math.hypot(loc[0], loc[1]) < 10:
                    continue
                size = [1.2, cell, wall_h] if axis == "x" else [cell, 1.2, wall_h]
                out.append({"kind": "ruin_wall", "loc": [round(v, 2) for v in loc],
                            "size": size, "rot": 0})
    return out


def wreck_field(world_id, count=30, spread=150.0):
    r = _rng(world_id)
    out = []
    for _ in range(count):
        a, d = r.uniform(0, math.tau), r.uniform(20, spread)
        length = r.uniform(10, 40)
        out.append({"kind": "wreck",
                    "loc": [round(math.cos(a) * d, 2), round(math.sin(a) * d, 2),
                            round(r.uniform(0.5, 6.0), 2)],
                    "size": [round(length, 2), round(r.uniform(4, 12), 2),
                             round(r.uniform(3, 10), 2)],
                    "rot": round(r.uniform(0, 360), 2)})
    return out


def arcade_strip(world_id, count=22, spread=110.0):
    """Cabinets and marquees down two sides of a neon street."""
    r = _rng(world_id)
    out = []
    for i in range(count):
        side = -1 if i % 2 else 1
        y = -spread + (i / max(count - 1, 1)) * spread * 2
        out.append({"kind": "cabinet", "loc": [side * r.uniform(7, 9), round(y, 2), 1.0],
                    "size": [1.0, 0.8, 2.0], "rot": 90 if side > 0 else -90})
        if i % 3 == 0:
            out.append({"kind": "facade", "loc": [side * 14.0, round(y, 2), 9.0],
                        "size": [8.0, 16.0, 18.0], "rot": 0})
    return out


def coral_reef(world_id, count=26, spread=150.0):
    """The Deep: arches, domes and kelp columns — nothing shaped like a tower."""
    r = _rng(world_id)
    out = []
    for _ in range(count):
        a, d = r.uniform(0, math.tau), r.uniform(20, spread)
        x, y = round(math.cos(a) * d, 2), round(math.sin(a) * d, 2)
        pick = r.random()
        if pick < 0.4:
            span, h = r.uniform(10, 26), r.uniform(8, 22)
            out.append({"kind": "coral_arch", "loc": [x, y, round(h / 2, 2)],
                        "size": [round(span, 2), round(r.uniform(2, 5), 2), round(h, 2)],
                        "rot": round(r.uniform(0, 360), 2)})
        elif pick < 0.7:
            rad = r.uniform(6, 18)
            out.append({"kind": "dome", "loc": [x, y, round(rad * 0.3, 2)],
                        "size": [round(rad, 2), round(rad, 2), round(rad * 0.6, 2)],
                        "rot": 0})
        else:
            h = r.uniform(14, 40)
            out.append({"kind": "kelp", "loc": [x, y, round(h / 2, 2)],
                        "size": [round(r.uniform(0.6, 1.8), 2),
                                 round(r.uniform(0.6, 1.8), 2), round(h, 2)],
                        "rot": 0})
    return out


def hedge_rows(world_id, rows=9, length=120.0, gap=16.0):
    """The Garden: cultivated rows and beds under the mushroom canopy."""
    r = _rng(world_id + "hedge")
    out = []
    for i in range(rows):
        y = -rows * gap / 2 + i * gap
        if abs(y) < 12:
            continue
        out.append({"kind": "hedge", "loc": [0.0, round(y, 2), 1.2],
                    "size": [round(length * r.uniform(0.6, 1.0), 2), 2.0, 2.4],
                    "rot": round(r.uniform(-4, 4), 2)})
        for j in range(3):
            out.append({"kind": "bed",
                        "loc": [round(r.uniform(-length / 2, length / 2), 2),
                                round(y + gap / 2, 2), 0.25],
                        "size": [round(r.uniform(4, 10), 2), round(r.uniform(3, 6), 2), 0.5],
                        "rot": 0})
    return out


def impossible_geometry(world_id, count=30, spread=110.0):
    """The Thought World: stairs to nowhere, freestanding arches, leaning slabs."""
    r = _rng(world_id + "impossible")
    out = []
    for i in range(count):
        a, d = r.uniform(0, math.tau), r.uniform(14, spread)
        x, y = round(math.cos(a) * d, 2), round(math.sin(a) * d, 2)
        pick = i % 3
        if pick == 0:
            steps = r.randint(5, 12)
            for s in range(steps):
                out.append({"kind": "stair", "loc": [round(x + s * 0.9, 2), y,
                                                     round(0.25 + s * 0.5, 2)],
                            "size": [0.9, round(r.uniform(2.0, 4.0), 2), 0.5],
                            "rot": round(r.uniform(0, 360), 2)})
        elif pick == 1:
            h = r.uniform(6, 18)
            out.append({"kind": "arch", "loc": [x, y, round(h / 2, 2)],
                        "size": [round(r.uniform(6, 16), 2), 1.5, round(h, 2)],
                        "rot": round(r.uniform(0, 360), 2)})
        else:
            out.append({"kind": "slab", "loc": [x, y, round(r.uniform(2, 14), 2)],
                        "size": [round(r.uniform(6, 20), 2), round(r.uniform(6, 20), 2), 0.8],
                        "rot": round(r.uniform(0, 360), 2)})
    return out


def scatter(world_id, kind, count, spread, size, z=0.0):
    r = _rng(world_id + kind)
    return [{"kind": kind,
             "loc": [round(r.uniform(-spread, spread), 2),
                     round(r.uniform(-spread, spread), 2), z],
             "size": [round(r.uniform(*size), 2), round(r.uniform(*size), 2),
                      round(r.uniform(*size), 2)],
             "rot": round(r.uniform(0, 360), 2)} for _ in range(count)]


# --- interactable helper ----------------------------------------------------


def obj(name, at, prompt, does, secret=None, coop=False, repeat=None):
    """One discoverable thing. `at` is [x, y, z] in metres."""
    return {"name": name, "at": at, "prompt": prompt, "does": does,
            "secret": secret, "coop": coop, "repeat": repeat}


WORLDS = {}


# ===========================================================================
# HOME
# ===========================================================================

WORLDS["trailer"] = {
    "name": "Your Trailer",
    "tagline": "Home. Lobby. Museum. Armory. Social space.",
    "kind": "home",
    "rules": {"gravity": 1.0, "combat": False, "pvp": False, "vehicles": False},
    "ground": None,
    "portal": [0.0, 3.6, 0.0],
    "structures": [],          # built by build_trailer.py, which shells the room
    "interactables": [
        obj("The Reality Machine", [0.0, 3.6, 1.1],
            "Choose a reality",
            "Opens character -> reality -> experience selection. The heart of the game.",
            repeat="Hums differently depending on how many realities you have unlocked."),
        obj("Artifact Pedestal A", [-1.1, 1.4, 0.5], "Place artifact",
            "Displays one artifact; visitors can examine it."),
        obj("Artifact Pedestal B", [-1.1, 0.2, 0.5], "Place artifact",
            "Second display slot."),
        obj("Artifact Pedestal C", [-1.1, -1.0, 0.5], "Place artifact",
            "Third display slot."),
        obj("Weapon Wall", [1.35, 0.6, 1.4], "Rack weapon",
            "Mounts up to six weapons. Lobby-only weapons still fire in here (GDD 4)."),
        obj("Workbench", [1.2, -2.2, 0.9], "Craft",
            "Crafting and weapon upgrades (Part II 37)."),
        obj("Wardrobe", [-1.2, -2.6, 1.0], "Customize",
            "Character creator access without re-entering the Machine."),
        obj("The Fridge", [1.25, 2.4, 0.8], "Open",
            "Ordinary fridge. Ordinary food.",
            secret="After the first reality is completed, it opens onto a corridor instead.",
            repeat="Different corridor each time."),
        obj("Trophy Shelf", [-1.35, 2.4, 1.5], "Examine",
            "Minigame trophies and event rewards."),
        obj("The Radio", [1.3, 1.4, 1.1], "Tune",
            "Plays reality-specific stations.",
            secret="One station is broadcasting from inside whatever reality you visited last."),
        obj("Pet Bed", [0.9, -0.8, 0.15], "Interact",
            "Where an adopted companion lives (Part II 42). Visitors can pet it.", coop=True),
        obj("Guest Book", [-0.2, 3.0, 0.9], "Sign",
            "Every visitor who enters your trailer can leave one line.", coop=True),
        obj("The Window", [-1.45, 0.8, 1.5], "Look",
            "Shows your own sky.",
            secret="Occasionally shows a sky you have not visited yet."),
        obj("Vehicle Pad", [4.5, -1.0, 0.05], "Store vehicle",
            "Outside the door. Displays one owned vehicle (Part II 43)."),
    ],
}

# ===========================================================================
# THE CROSSROADS
# ===========================================================================

WORLDS["portal_hub"] = {
    "name": "The Portal Hub",
    "tagline": "Different worlds. Different rules.",
    "kind": "hub",
    "source": "Portal hub concept board (P1-P5 + CORE)",
    "rules": {"gravity": 1.0, "combat": False, "pvp": False, "vehicles": True},
    "ground": {"size": [220, 220]},
    "portal": [0.0, -60.0, 0.0],
    "structures": (
        [{"kind": "gantry", "loc": [0, 0, -1], "size": [70, 70, 2], "rot": 0},
         {"kind": "core", "loc": [0, 0, 6], "size": [10, 10, 12], "rot": 0}]
        + [{"kind": "portal_frame",
            "loc": [round(math.cos(math.radians(a)) * 40, 2),
                    round(math.sin(math.radians(a)) * 40, 2), 7.0],
            "size": [14, 3, 14], "rot": round(a + 90, 2)}
           for a in (90, 162, 234, 306, 18)]
        + [{"kind": "catwalk",
            "loc": [round(math.cos(math.radians(a)) * 22, 2),
                    round(math.sin(math.radians(a)) * 22, 2), 0.0],
            "size": [6, 30, 0.6], "rot": round(a + 90, 2)}
           for a in (90, 162, 234, 306, 18)]
        + scatter("portal_hub", "crate", 24, 55, (1.0, 3.0), z=0.8)),
    "interactables": [
        obj("Portal P1 - Crystalline", [0.0, 40.0, 2.0], "Enter",
            "Gateway to the shattered-crystal world. Tag strip shows biome, hazard, activity."),
        obj("Portal P2 - Bio-Metropolis", [-38.0, 12.4, 2.0], "Enter",
            "Gateway to the grown city."),
        obj("Portal P3 - Plasma-Strait", [-23.5, -32.4, 2.0], "Enter",
            "Gateway to the storm and the wreck fields."),
        obj("Portal P4 - Ruins-Labyrinth", [23.5, -32.4, 2.0], "Enter",
            "Gateway to the overgrown maze."),
        obj("Portal P5 - Gravity-Ring", [38.0, 12.4, 2.0], "Enter",
            "Gateway to the ringed world."),
        obj("The CORE", [0.0, 0.0, 2.0], "Approach",
            "The hub's power source and its central mystery. Anchor for the three-key hunt.",
            secret="Accepts three keys found across three different realities.", coop=True),
        obj("Tag Reader", [6.0, 8.0, 1.2], "Read",
            "Explains what a portal's icon strip means before you commit."),
        obj("The Noticeboard", [-6.0, 8.0, 1.4], "Read",
            "Player-left notes about what is through each portal.", coop=True),
        obj("Bartering Post", [10.0, -6.0, 1.0], "Trade",
            "Opens the two-sided trade window with a nearby player (Part II 39).", coop=True),
        obj("The Vending Machine", [-10.0, -6.0, 1.0], "Buy",
            "Dispenses an object from a reality you have not visited. Never the same twice.",
            repeat="Rotates stock every real-world hour."),
        obj("Minigame Arch", [0.0, 20.0, 2.0], "Enter",
            "Leads to the minigame portals (Part II 41)."),
        obj("Vehicle Rail", [16.0, 0.0, 0.5], "Mount",
            "Spawns your stored vehicle for hub traversal."),
        obj("The Bench of Agreement", [0.0, -14.0, 0.5], "Sit",
            "Two players sitting at once opens something under the gantry.", coop=True),
        obj("Broken Portal P0", [-30.0, 30.0, 2.0], "Examine",
            "Dead frame, no light.",
            secret="Comes alive once, briefly, after the CORE is opened."),
    ],
}

# ===========================================================================
# REALITY 001
# ===========================================================================

WORLDS["living_city"] = {
    "name": "The Living City",
    "tagline": "A massive impossible city where architecture constantly changes.",
    "kind": "reality",
    "source": "GDD 7",
    "rules": {"gravity": 1.0, "combat": True, "pvp": False, "vehicles": True},
    "ground": {"size": [420, 420]},
    "portal": [0.0, 0.0, 0.0],
    "structures": grid_towers("living_city", count=48, spread=180, h=(14, 80),
                              foot=(9, 24), lean=6),
    "interactables": [
        obj("The Bust", [6.0, 9.0, 1.1], "Hold cup under chin",
            "A marble bust pours coffee. Nobody in the city finds this remarkable. +Stamina.",
            secret="Every twentieth cup is not coffee.",
            repeat="At night it pours something that glows."),
        obj("The Complaining Door", [-11.0, 14.0, 1.2], "Try handle",
            "Locked, and it explains at length exactly why, and whose fault it is.",
            repeat="Tell it you agree and it unlocks."),
        obj("Staircase to Nowhere", [18.0, -7.0, 3.0], "Climb",
            "Ends in open air two storeys up.",
            secret="Keep walking upward anyway and the next step appears."),
        obj("The Payphone", [-6.0, -13.0, 1.3], "Answer",
            "Rings whenever a player walks past. Someone is on the line and knows your name."),
        obj("The Puddle", [12.0, 3.0, 0.02], "Look in",
            "Reflects a version of this street that is on fire. Yours is not."),
        obj("The Chair That Waits", [-16.0, 4.0, 0.5], "Sit",
            "Moves a little closer whenever no player is looking at it."),
        obj("The Mailbox", [3.0, 17.0, 1.0], "Open",
            "Holds a note another player left in this reality.", coop=True),
        obj("The Loud Painting", [-19.0, -9.0, 2.0], "Approach",
            "Plays music, audible only within two metres of it."),
        obj("The Chandelier", [9.0, -18.0, 6.0], "Watch",
            "Swings to point at the nearest player.",
            secret="After dark it points at something else entirely."),
        obj("The Bureaucrat's Desk", [-4.0, 24.0, 0.9], "Stamp form",
            "Stamping the form moves a wall somewhere else in the district.", coop=True),
        obj("The Elevator", [22.0, 12.0, 1.0], "Ride",
            "Six buttons. Four go to floors.",
            secret="The fifth goes to a floor that is not in this building."),
        obj("The Telescope", [-24.0, -20.0, 1.5], "Look through",
            "Shows other realities.",
            repeat="Once in a while it shows this street, from behind you."),
        obj("Building That Breathes", [34.0, 28.0, 20.0], "Touch",
            "The facade expands and contracts. Warm to the touch."),
        obj("The Suggestion Box", [0.0, -26.0, 1.0], "Write",
            "Whatever you write shows up somewhere in the city later.", coop=True),
        obj("Traffic Light Choir", [15.0, 22.0, 4.0], "Listen",
            "Three lights, singing in harmony. They change key when a car passes."),
        obj("The Fountain", [-9.0, 0.0, 0.6], "Drop item in",
            "Give it an item, get a different one back. Rarity is roughly preserved."),
        obj("Reality Weapon Cache", [40.0, -34.0, 1.0], "Open",
            "Contains the Gravity Gun (Reality class) behind a two-player lock.", coop=True),
        obj("The Eye of Reality", [-46.0, 40.0, 12.0], "Take",
            "Legendary artifact. Origin: Reality 07. Status: unknown.",
            secret="Only appears once the city has rearranged itself three times."),
    ],
}

# ===========================================================================
# REALITY 002
# ===========================================================================

WORLDS["the_deep"] = {
    "name": "The Deep",
    "tagline": "A surreal underwater civilization.",
    "kind": "reality",
    "source": "GDD 7",
    "rules": {"gravity": 0.35, "combat": True, "pvp": False, "vehicles": True,
              "swim": True},
    "ground": {"size": [400, 400]},
    "portal": [0.0, 0.0, 6.0],
    "structures": (coral_reef("the_deep", count=30, spread=150)
                   + scatter("the_deep", "hull", 10, 140, (6.0, 18.0), z=3.0)),
    "interactables": [
        obj("The Lantern Shoal", [10.0, 14.0, 8.0], "Follow",
            "A shoal of lights that leads somewhere if you keep up. It does not wait."),
        obj("Pressure Door", [-14.0, 9.0, 2.0], "Turn wheel",
            "Takes two players turning opposite wheels at once.", coop=True),
        obj("The Singing Coral", [7.0, -12.0, 3.0], "Touch",
            "Each branch is a note. Play the right five and something opens below.",
            secret="The sequence is written on the ceiling of the sunken hall."),
        obj("Air Pocket Chapel", [-22.0, -18.0, 5.0], "Enter",
            "A dry room at the bottom of the sea. Someone has been living here."),
        obj("The Anchor", [26.0, 4.0, 1.0], "Pull",
            "Attached to something that is not a boat."),
        obj("Message Bottles", [4.0, 22.0, 1.5], "Open",
            "Notes from players who drowned here.", coop=True),
        obj("Bioluminescent Switchboard", [-8.0, -4.0, 2.0], "Rewire",
            "Rerouting the light changes which corridors are safe."),
        obj("The Whale Skeleton", [38.0, -30.0, 6.0], "Enter ribcage",
            "Something is nesting in it. It is friendly, mostly."),
        obj("Tide Organ", [-34.0, 26.0, 4.0], "Play",
            "The current plays it. You can change the tuning and the current follows."),
        obj("Sunken Vending Machine", [16.0, -26.0, 1.0], "Buy",
            "Still works. Still takes Credits. Dispenses dry snacks."),
        obj("The Drowned Museum", [-40.0, -8.0, 3.0], "Explore",
            "Somebody else's trophy room, flooded. Their artifacts are still on the pedestals.",
            secret="One pedestal is empty and labelled with your character's name."),
        obj("Organic Weapon Pod", [30.0, 34.0, 4.0], "Harvest",
            "Contains the Living Blade (Organic class)."),
        obj("The Depth Marker", [0.0, -44.0, 20.0], "Read",
            "Counts down as you descend. Below zero it keeps counting."),
    ],
}

# ===========================================================================
# REALITY 003
# ===========================================================================

WORLDS["the_garden"] = {
    "name": "The Garden",
    "tagline": "A living ecosystem where plants and creatures interact with players.",
    "kind": "reality",
    "source": "GDD 7",
    "rules": {"gravity": 1.0, "combat": True, "pvp": False, "vehicles": False},
    "ground": {"size": [400, 400]},
    "portal": [0.0, 0.0, 0.0],
    "structures": (organic_clusters("the_garden", count=24, spread=160, h=(6, 34))
                   + hedge_rows("the_garden", rows=9, length=120.0, gap=16.0)),
    "interactables": [
        obj("The Greeting Vine", [5.0, 7.0, 1.0], "Offer hand",
            "Shakes your hand. Remembers you next visit.",
            repeat="On the third visit it introduces you to another plant."),
        obj("Seed Bank", [-9.0, 12.0, 1.0], "Deposit / withdraw",
            "Plant a seed here and it grows into something over real-world days.", coop=True),
        obj("The Carnivore", [14.0, -6.0, 1.5], "Feed",
            "Feed it the wrong thing and it sulks for a week."),
        obj("Pollen Bell", [-16.0, -11.0, 2.0], "Ring",
            "Calls every creature within range. Some of them are pleased about it."),
        obj("The Compost Heap", [22.0, 16.0, 1.0], "Bury item",
            "Bury an item, come back later, get something stranger.",
            secret="Bury an artifact and the Garden makes an opinion known."),
        obj("Walking Tree", [-28.0, 5.0, 8.0], "Follow",
            "It is going somewhere. It has been going there for a long time."),
        obj("The Beehive Archive", [11.0, 26.0, 4.0], "Listen",
            "The hum is a recording. Of what, is the question."),
        obj("Mushroom Trampoline", [-6.0, -22.0, 1.0], "Jump",
            "Launches you into the canopy. The canopy has its own map."),
        obj("The Gardener's Shed", [33.0, -20.0, 1.5], "Open",
            "Tools, notes, and a schedule for something that is not gardening."),
        obj("Sap Still", [-36.0, -30.0, 1.2], "Operate",
            "Brews Healing and Hype potions from harvested sap (Part II 36)."),
        obj("The Quiet Clearing", [0.0, 38.0, 0.0], "Stand still",
            "Nothing happens until you stop moving for thirty seconds."),
        obj("Plant Whip Bloom", [26.0, 30.0, 2.0], "Cut",
            "Yields the Plant Whip (Organic class)."),
        obj("The Cat", [-3.0, -14.0, 0.3], "Follow",
            "Not a pet. Leads patient players somewhere worth going."),
    ],
}

# ===========================================================================
# REALITY 004
# ===========================================================================

WORLDS["the_void"] = {
    "name": "The Void",
    "tagline": "A cosmic environment where physics behaves differently.",
    "kind": "reality",
    "source": "GDD 7",
    "rules": {"gravity": 0.15, "combat": True, "pvp": False, "vehicles": False},
    "ground": None,
    "portal": [0.0, 0.0, 0.0],
    "structures": floating_islands("the_void", count=30, spread=150, z=(-40, 60)),
    "interactables": [
        obj("The Handhold", [3.0, 5.0, 1.0], "Grab",
            "The only fixed point. Let go and you drift."),
        obj("Gravity Well Switch", [-12.0, 8.0, 4.0], "Flip",
            "Reverses which way is down for everyone in the region.", coop=True),
        obj("The Long Rope", [18.0, -9.0, 12.0], "Climb",
            "Tied at one end. The other end is not visible."),
        obj("Starlight Forge", [-20.0, -16.0, 22.0], "Use",
            "Upgrades Cosmic weapons. Consumes Shards."),
        obj("The Slow Clock", [9.0, 20.0, -8.0], "Wind",
            "Time near it runs at a third speed. Useful in a fight, awkward in a conversation."),
        obj("Debris of a Trailer", [30.0, 14.0, 30.0], "Search",
            "Someone else's home, in pieces.",
            secret="Their guest book survived. Your name is in it."),
        obj("The Echo", [-26.0, 22.0, -14.0], "Shout",
            "Repeats what you said, correctly, in a voice that is not yours."),
        obj("Star Cannon Cradle", [24.0, -28.0, 18.0], "Take",
            "Yields the Star Cannon (Cosmic class)."),
        obj("The Tether Ring", [0.0, -30.0, 6.0], "Attach",
            "Two players tethered can reach islands neither could alone.", coop=True),
        obj("Black Marble", [-38.0, 0.0, 40.0], "Take",
            "Weighs more than the island it is sitting on."),
        obj("The Silent Bell", [14.0, 36.0, -20.0], "Ring",
            "No sound. Everyone in the reality feels it."),
        obj("Time Shard Rift", [-8.0, -40.0, 26.0], "Reach in",
            "Yields the Time Shard (Reality class). Costs something."),
    ],
}

# ===========================================================================
# REALITY 005
# ===========================================================================

WORLDS["thought_world"] = {
    "name": "The Thought World",
    "tagline": "The environment reacts to player behavior.",
    "kind": "reality",
    "source": "GDD 7",
    "rules": {"gravity": 1.0, "combat": False, "pvp": False, "vehicles": False},
    "ground": {"size": [300, 300]},
    "portal": [0.0, 0.0, 0.0],
    "structures": impossible_geometry("thought_world", count=30, spread=110),
    "interactables": [
        obj("The First Door", [0.0, 8.0, 1.2], "Open",
            "Leads wherever you were expecting it to lead."),
        obj("Mirror of Habits", [-10.0, 4.0, 1.6], "Look",
            "Shows how you have been playing. Not always flatteringly."),
        obj("The Path That Forms", [8.0, -10.0, 0.1], "Walk",
            "Ground appears one step ahead. Stop and it stops."),
        obj("Room of Loud Thinking", [-18.0, -14.0, 1.5], "Enter",
            "Your proximity voice is broadcast to the whole reality while inside.", coop=True),
        obj("The Contradiction", [16.0, 12.0, 2.0], "Approach",
            "A staircase going up and down at once. Both are true."),
        obj("Certainty Meter", [-4.0, 20.0, 1.0], "Read",
            "Measures how sure you are. Reacts to hesitation in your movement."),
        obj("The Agreeable Wall", [24.0, -6.0, 3.0], "Push",
            "Moves if two players push it. Refuses to move for one.", coop=True),
        obj("Memory Pedestal", [-26.0, 8.0, 1.0], "Place artifact",
            "Puts an artifact's origin story into the sky for everyone to read.", coop=True),
        obj("The Quiet Question", [0.0, -24.0, 1.2], "Answer",
            "Asks one thing. Remembers the answer across sessions.",
            secret="Answer the same way three visits running and it opens."),
        obj("Mind Trip Still", [12.0, 26.0, 1.0], "Brew",
            "Produces the Mind Trip potion. The world gets noticeably more honest."),
        obj("The Crowd", [-14.0, -26.0, 1.0], "Join",
            "Figures that copy whatever the most players are doing.", coop=True),
    ],
}

# ===========================================================================
# THE DREAMING
# ===========================================================================

WORLDS["the_dreaming"] = {
    "name": "The Dreaming",
    "tagline": "Surreal. Dream logic. Nothing needs to explain itself.",
    "kind": "reality",
    "source": "Feature board (realities row)",
    "rules": {"gravity": 0.6, "combat": False, "pvp": False, "vehicles": False},
    "ground": {"size": [340, 340]},
    "portal": [0.0, 0.0, 0.0],
    "structures": (floating_islands("the_dreaming", count=20, spread=120, z=(2, 44))
                   + scatter("the_dreaming", "door", 18, 90, (2.0, 3.0), z=1.5)),
    "interactables": [
        obj("Freestanding Doors", [6.0, 6.0, 1.5], "Open",
            "Eighteen doors standing in open ground. Each leads to a different one of the others.",
            repeat="The pairing reshuffles every time the reality reloads."),
        obj("The Bed in the Field", [-12.0, 10.0, 0.6], "Sleep",
            "Sleeping here moves you to a different part of the reality. You do not choose which."),
        obj("Upside-Down Rain", [14.0, -8.0, 0.0], "Stand in it",
            "Falls upward. Soaks you anyway."),
        obj("The Teacher", [-20.0, -6.0, 1.7], "Talk",
            "Asks about an exam you have not studied for. Will not be reasoned with."),
        obj("Melting Staircase", [22.0, 14.0, 4.0], "Climb",
            "Softens under weight. Two players are too many.", coop=True),
        obj("The Phone That Rings Backwards", [-8.0, 22.0, 1.2], "Answer",
            "You speak first, then it rings."),
        obj("Familiar Room", [30.0, -18.0, 1.5], "Enter",
            "It is your trailer, wrong in three details.",
            secret="Finding all three details unlocks a trailer decor set."),
        obj("The Long Corridor", [-30.0, -22.0, 1.5], "Walk",
            "Gets longer the faster you run down it."),
        obj("Mask Rack", [4.0, -28.0, 1.4], "Wear",
            "Wearing one changes how NPCs across the reality address you."),
        obj("The Waking Bell", [0.0, 34.0, 2.0], "Ring",
            "Ejects you home immediately, gently. The only polite exit in the multiverse."),
    ],
}

# ===========================================================================
# THE WASTELAND
# ===========================================================================

WORLDS["the_wasteland"] = {
    "name": "The Wasteland",
    "tagline": "Post-apocalyptic. Somebody lived here, and recently.",
    "kind": "reality",
    "source": "Feature board (realities row)",
    "rules": {"gravity": 1.0, "combat": True, "pvp": "zoned", "vehicles": True},
    "ground": {"size": [460, 460]},
    "portal": [0.0, 0.0, 0.0],
    "structures": (wreck_field("the_wasteland", count=34, spread=170)
                   + scatter("the_wasteland", "rock", 40, 190, (2.0, 9.0), z=1.0)),
    "interactables": [
        obj("The Last Radio Tower", [20.0, 30.0, 18.0], "Climb / tune",
            "Broadcasts a loop. The loop has a gap in it, and the gap is a message."),
        obj("Fuel Cache", [-16.0, 12.0, 0.8], "Siphon",
            "Vehicle fuel. Guarded by something that was not always hostile."),
        obj("Scrap Press", [12.0, -14.0, 1.5], "Operate",
            "Turns junk into crafting materials (Part II 37)."),
        obj("The Bunker Door", [-28.0, -20.0, 1.0], "Open",
            "Needs two hands on two wheels twelve metres apart.", coop=True),
        obj("Family Photo", [8.0, 22.0, 0.6], "Take",
            "An artifact worth nothing and everything."),
        obj("Rust Choir", [34.0, -8.0, 3.0], "Listen",
            "Wind through wrecks. It is playing a song someone wrote."),
        obj("The Trading Post", [-6.0, -34.0, 1.2], "Trade",
            "Player bartering hub for this reality (Part II 39).", coop=True),
        obj("Nano Drone Wreck", [40.0, 24.0, 1.0], "Salvage",
            "Yields the Nano Drone (Technology class)."),
        obj("The Rift", [0.0, 46.0, 4.0], "Approach",
            "World event anchor: defeat the Rift Guardian, collect 5 Energy Cores.",
            coop=True),
        obj("Boneyard Sign", [-42.0, 6.0, 2.0], "Read",
            "Names every player who died in this reality this week.", coop=True),
        obj("Working Streetlight", [16.0, -40.0, 4.0], "Stand under",
            "The only one still lit for a hundred kilometres. Full health regen."),
    ],
}

# ===========================================================================
# THE PET SANCTUARY
# ===========================================================================

WORLDS["pet_sanctuary"] = {
    "name": "The Pet Sanctuary",
    "tagline": "No weapons. No threat. No timer.",
    "kind": "reality",
    "source": "Pet Sanctuary concept board",
    "rules": {"gravity": 1.0, "combat": False, "pvp": False, "vehicles": False},
    "ground": {"size": [220, 220]},
    "portal": [0.0, -14.0, 0.0],
    "structures": (organic_clusters("pet_sanctuary", count=22, spread=90, h=(10, 26))
                   + [{"kind": "cottage", "loc": [0, 6, 2.2], "size": [9, 8, 4.4], "rot": 0},
                      {"kind": "bridge", "loc": [14, -4, 0.4], "size": [3, 10, 0.4], "rot": 12},
                      {"kind": "stream", "loc": [20, 0, -0.2], "size": [6, 90, 0.3], "rot": 8}]),
    "interactables": [
        obj("The Runed Doorway", [0.0, 2.0, 1.8], "Enter",
            "The carved arch into the cottage. Warm light, a fire going."),
        obj("The Fireplace", [0.0, 8.0, 0.8], "Sit",
            "Sitting here with another player starts a slow conversation prompt.", coop=True),
        obj("Sleeping Cat", [-2.5, 7.0, 0.5], "Pet",
            "Adoptable. Will judge your trailer decor."),
        obj("The Golden Dog", [2.5, 5.0, 0.4], "Play fetch",
            "Adoptable. Brings back things it should not have found."),
        obj("Rabbit Hollow", [-8.0, -4.0, 0.3], "Wait",
            "They come out if you stay still."),
        obj("The Adoption Sign", [6.0, -2.0, 1.0], "Read",
            "Explains the companion system. One pet per trailer, more with expansions."),
        obj("Feed Bin", [-6.0, 2.0, 0.6], "Fill bowl",
            "Feeding another player's pet raises both of your reputations.", coop=True),
        obj("The Stream", [20.0, 0.0, 0.0], "Follow",
            "Leads out of the sanctuary and does not come back."),
        obj("Carved Bench", [-10.0, 8.0, 0.5], "Sit",
            "Names carved into it. All of them are players who have been here."),
        obj("The Lantern Path", [4.0, -10.0, 0.8], "Light",
            "Light every lantern on the path and something arrives at the cottage.",
            secret="It only works at the sanctuary's dusk."),
        obj("Companion Drone Nest", [12.0, 12.0, 1.2], "Approach",
            "Where the shoulder drone from the portal-network art is met."),
    ],
}

# ===========================================================================
# THE FOUR PORTAL-HUB WORLDS
# ===========================================================================

WORLDS["bio_metropolis"] = {
    "name": "Bio-Metropolis",
    "tagline": "A city that was grown, not built.",
    "kind": "reality",
    "source": "Portal hub board (P2)",
    "rules": {"gravity": 0.9, "combat": True, "pvp": False, "vehicles": False},
    "ground": {"size": [380, 380]},
    "portal": [0.0, 0.0, 0.0],
    "structures": (organic_clusters("bio_metropolis", count=26, spread=150, h=(20, 70))
                   + grid_towers("bio_metropolis", count=18, spread=120, h=(10, 40),
                                 foot=(7, 16), lean=9)),
    "interactables": [
        obj("The World-Tree Lift", [0.0, 10.0, 2.0], "Ride",
            "A living lift. It asks where you are going and sometimes disagrees."),
        obj("Root Market", [-14.0, 16.0, 1.2], "Browse",
            "Shop stalls grown into the roots (Part II 38).", coop=True),
        obj("Grafting Bench", [10.0, -12.0, 1.0], "Graft",
            "Combines two Organic weapons into one. Results are not always predictable."),
        obj("The Pollen Tram", [24.0, 6.0, 3.0], "Board",
            "Traverses the canopy on a schedule the city sets, not you."),
        obj("Hive Council", [-22.0, -18.0, 2.0], "Petition",
            "NPC faction. They remember every interaction (GDD 18)."),
        obj("The Wound", [32.0, 22.0, 6.0], "Treat",
            "A cut in the world-tree. Healing it changes the district's layout.", coop=True),
        obj("Sap Vault", [-30.0, 10.0, 1.5], "Open",
            "Rare crafting materials behind a puzzle of growth cycles."),
        obj("Seedpod Elevator Shaft", [16.0, -30.0, 1.0], "Enter",
            "Drops you to the roots. Coming back up is a separate problem."),
        obj("The Key of Roots", [-40.0, -34.0, 8.0], "Take",
            "One of three keys the CORE accepts (Part II 47).",
            secret="Only forms after the Wound is healed."),
        obj("Canopy Bridge", [0.0, 40.0, 26.0], "Cross",
            "Grows across as you walk, retracts behind you."),
    ],
}

WORLDS["plasma_strait"] = {
    "name": "Plasma-Strait",
    "tagline": "Storm-lashed wreck fields under a sky that never settles.",
    "kind": "reality",
    "source": "Portal hub board (P3)",
    "rules": {"gravity": 1.1, "combat": True, "pvp": "zoned", "vehicles": True},
    "ground": {"size": [440, 440]},
    "portal": [0.0, 0.0, 0.0],
    "structures": (wreck_field("plasma_strait", count=32, spread=180)
                   + scatter("plasma_strait", "spire", 22, 170, (3.0, 12.0), z=8.0)),
    "interactables": [
        obj("The Storm Anchor", [0.0, 12.0, 3.0], "Deploy",
            "Calms the lightning in a radius for ninety seconds. Everyone benefits.", coop=True),
        obj("Charged Wreck", [-16.0, 8.0, 2.0], "Ground it",
            "Safe to loot only once the charge is bled off."),
        obj("Lightning Harp", [14.0, -10.0, 5.0], "Play",
            "Strikes tune themselves to what you play. Risky and worth it."),
        obj("Salvage Crane", [26.0, 18.0, 8.0], "Operate",
            "One player drives, one player spots.", coop=True),
        obj("The Barometer", [-24.0, -14.0, 1.5], "Read",
            "Predicts the next storm surge accurately. Nobody trusts it."),
        obj("Sound Cannon Wreck", [34.0, -26.0, 2.0], "Salvage",
            "Yields the Sound Cannon (Absurd class)."),
        obj("Faraday Chapel", [-34.0, 22.0, 3.0], "Shelter",
            "The only guaranteed-safe structure. Fits four."),
        obj("The Strait Crossing", [0.0, -38.0, 1.0], "Cross",
            "Passable for eleven seconds after each surge."),
        obj("The Key of Storms", [42.0, 36.0, 6.0], "Take",
            "Second of the three CORE keys.",
            secret="Must be taken during a surge, not between them."),
        obj("Wreck of the Ferry", [-44.0, -4.0, 4.0], "Search",
            "Passenger manifest. Some of the names are player names.", coop=True),
    ],
}

WORLDS["ruins_labyrinth"] = {
    "name": "Ruins-Labyrinth",
    "tagline": "An overgrown maze that was a temple, and may still be.",
    "kind": "reality",
    "source": "Portal hub board (P4)",
    "rules": {"gravity": 1.0, "combat": True, "pvp": False, "vehicles": False},
    "ground": {"size": [300, 300]},
    "portal": [0.0, -70.0, 0.0],
    "structures": (ruin_maze("ruins_labyrinth", cells=9, cell=14.0, wall_h=6.0)
                   + organic_clusters("ruins_labyrinth", count=16, spread=110, h=(8, 20))),
    "interactables": [
        obj("The Threshold Stone", [0.0, -60.0, 1.0], "Read",
            "Names everyone currently inside the maze.", coop=True),
        obj("Moss Map", [-8.0, -48.0, 1.4], "Read",
            "The moss grows in the shape of the maze. It is out of date."),
        obj("Wall That Listens", [12.0, -30.0, 3.0], "Speak",
            "Say the right word and it steps aside. The word is elsewhere in the maze."),
        obj("The Torch Line", [-14.0, -14.0, 2.0], "Light",
            "Lit torches persist for other players for an hour.", coop=True),
        obj("Offering Bowl", [0.0, 0.0, 1.0], "Offer",
            "Give up an item; the maze simplifies for you. Give up an artifact; it opens."),
        obj("The Repeating Room", [16.0, 16.0, 1.5], "Enter",
            "The same room four times. One of them has an extra door."),
        obj("Buried Bell", [-22.0, 22.0, 0.5], "Dig",
            "Ringing it resets the maze layout for everyone in it.", coop=True),
        obj("Paint Blaster Cache", [28.0, -6.0, 1.0], "Open",
            "Yields the Paint Blaster (Art class). Paint marks walls permanently."),
        obj("The Key of Stone", [0.0, 34.0, 2.0], "Take",
            "Third of the three CORE keys, at the maze's true centre.",
            secret="The true centre is not the geometric centre."),
        obj("Exit That Moves", [34.0, 34.0, 1.5], "Leave",
            "It is never where you left it."),
    ],
}

WORLDS["gravity_ring"] = {
    "name": "Gravity-Ring",
    "tagline": "A ringed world where down is a local opinion.",
    "kind": "reality",
    "source": "Portal hub board (P5)",
    "rules": {"gravity": "variable", "combat": True, "pvp": False, "vehicles": True},
    "ground": None,
    "portal": [0.0, 0.0, 0.0],
    "structures": (floating_islands("gravity_ring", count=34, spread=160, z=(-50, 70))
                   + [{"kind": "ring_segment",
                       "loc": [round(math.cos(math.radians(a)) * 90, 2),
                               round(math.sin(math.radians(a)) * 90, 2), 0.0],
                       "size": [40, 8, 2], "rot": round(a + 90, 2)}
                      for a in range(0, 360, 30)]),
    "interactables": [
        obj("Gravity Dial", [0.0, 6.0, 1.0], "Turn",
            "Sets local gravity between 0.1 and 2.0 for a whole ring segment.", coop=True),
        obj("The Drop", [-12.0, 12.0, 0.0], "Step off",
            "Falls forever unless someone changes the dial while you are falling.", coop=True),
        obj("Anti-Grav Boot Locker", [18.0, -8.0, 1.0], "Open",
            "Anti-Grav Boots — also the Gravity Arena minigame reward (Part II 41)."),
        obj("Orbital Tram", [26.0, 14.0, 2.0], "Board",
            "Circles the ring. Stops are on the outside of the ring."),
        obj("The Balance Puzzle", [-26.0, -16.0, 4.0], "Solve",
            "Two players on two plates, different masses, one bridge.", coop=True),
        obj("Fallen Climber", [32.0, -24.0, 1.0], "Search",
            "Their log describes a segment that is not on any map."),
        obj("Gravity Gun Vault", [-36.0, 20.0, 6.0], "Open",
            "Yields the Gravity Gun (Reality class)."),
        obj("The Inverted Town", [0.0, 44.0, 30.0], "Enter",
            "Built on the underside. The residents consider you upside-down."),
        obj("Ring Fracture", [44.0, 40.0, 8.0], "Cross",
            "A missing segment. Crossing it needs the dial and a running start."),
    ],
}

# ===========================================================================
# THE ARCADE  (original replacement for the "Oasis Archaide" reference art)
# ===========================================================================

WORLDS["the_arcade"] = {
    "name": "The Arcade",
    "tagline": "A neon street where the machines are doors.",
    "kind": "reality",
    "source": ("Arcade concept boards, rebuilt original. See GDD Part II 47 — "
               "no third-party games, characters or marquees."),
    "rules": {"gravity": 1.0, "combat": False, "pvp": "zoned", "vehicles": True},
    "ground": {"size": [280, 280]},
    "portal": [0.0, -100.0, 0.0],
    "structures": (arcade_strip("the_arcade", count=22, spread=100)
                   + grid_towers("the_arcade", count=14, spread=90, h=(20, 60),
                                 foot=(10, 20), lean=0)),
    "interactables": [
        obj("Racer's Edge Cabinet", [-8.0, -60.0, 1.0], "Enter",
            "Minigame: Urban Velocity. Reward: 'Neon Rider' bike skin. Leaderboard on the marquee."),
        obj("Vortex Cabinet", [8.0, -40.0, 1.0], "Enter",
            "Minigame: our own 8-bit arena. Reward: Retro Artifact x1. All games original."),
        obj("Gravity Arena Cabinet", [-8.0, -20.0, 1.0], "Enter",
            "Minigame: Float Fights, zero-g combat. Reward: Anti-Grav Boots."),
        obj("Mystery Vault Cabinet", [8.0, 0.0, 1.0], "Enter",
            "Minigame: Decryptor 7, a cipher puzzle. Reward: holographic trailer decor."),
        obj("Deathtrack Cabinet", [-8.0, 20.0, 1.0], "Enter",
            "Minigame: Neon Deathtrack race variant. Reward: vehicle cosmetics."),
        obj("Crawl Cabinet", [8.0, 40.0, 1.0], "Enter",
            "Minigame: top-down co-op dungeon crawl. Reward: consumables and materials.",
            coop=True),
        obj("The High Score Board", [0.0, 60.0, 4.0], "Read",
            "Every minigame's top name and score, updated live.", coop=True),
        obj("Token Machine", [-12.0, 50.0, 1.0], "Exchange",
            "Credits to event Tokens (Part II 38)."),
        obj("The Cabinet Nobody Plays", [12.0, -80.0, 1.0], "Enter",
            "Unlabelled, unlit, in the corner.",
            secret="Plays a game about a trailer and a machine. It knows your play history."),
        obj("Prize Counter", [0.0, 74.0, 1.2], "Redeem",
            "Tickets for trailer decor and emotes.", coop=True),
        obj("Two-Player Cabinet", [-14.0, 8.0, 1.0], "Enter",
            "Refuses to start with one player. Best rewards in the street.", coop=True),
        obj("Battle Arena Gate", [20.0, -10.0, 2.0], "Enter",
            "The street's one PvP zone. Opt-in, nothing at stake but the leaderboard."),
    ],
}

# ===========================================================================
# P1 - the crystalline world the hub board shows but does not name
# ===========================================================================

WORLDS["crystal_shatter"] = {
    "name": "The Shatter",
    "tagline": "A crystalline world that rings when you walk on it.",
    "kind": "reality",
    "source": "Portal hub board (P1)",
    "rules": {"gravity": 0.8, "combat": True, "pvp": False, "vehicles": False},
    "ground": {"size": [320, 320]},
    "portal": [0.0, 0.0, 0.0],
    "structures": (floating_islands("crystal_shatter", count=24, spread=130, z=(0, 40))
                   + scatter("crystal_shatter", "shard", 44, 150, (2.0, 14.0), z=4.0)),
    "interactables": [
        obj("The Ringing Floor", [0.0, 6.0, 0.1], "Walk",
            "Each step is a note. Other players hear your route as music.", coop=True),
        obj("Fracture Line", [-14.0, 10.0, 0.5], "Strike",
            "Breaking it opens a path and closes another."),
        obj("The Tuning Shard", [12.0, -12.0, 2.0], "Take",
            "Held, it makes nearby crystal safe to touch."),
        obj("Prism Lock", [22.0, 8.0, 2.0], "Align",
            "Three beams, three players, one door.", coop=True),
        obj("The Frozen Explorer", [-26.0, -18.0, 1.5], "Free",
            "An NPC caught mid-step. Freeing them is not obviously a good idea."),
        obj("Echo Cavern", [30.0, 20.0, 1.0], "Shout",
            "Repeats everything said in it for the next player who enters.", coop=True),
        obj("Shard Vein", [-34.0, 24.0, 2.0], "Mine",
            "The reality's Shard currency source (Part II 38)."),
        obj("The Unbroken Pane", [0.0, 38.0, 6.0], "Look through",
            "Shows the Portal Hub from the inside of P1. Someone is standing there."),
    ],
}

# ===========================================================================
# THE PORTALS — "Enter. Explore. Return."
# The feature board's portal panel is a forest, not a machine room: portals
# standing between trees, no architecture around them. It is the wild
# counterpart to the built Portal Hub, and the quieter way into the multiverse.
# ===========================================================================

WORLDS["portal_glade"] = {
    "name": "The Portal Glade",
    "tagline": "Enter. Explore. Return.",
    "kind": "hub",
    "source": "Feature board — THE PORTALS panel",
    "rules": {"gravity": 1.0, "combat": False, "pvp": False, "vehicles": False},
    "ground": {"size": [200, 200]},
    "portal": [0.0, -34.0, 0.0],
    "structures": (
        scatter("portal_glade", "trunk", 46, 85, (1.2, 3.5), z=9.0)
        + scatter("portal_glade", "boulder", 18, 70, (1.5, 5.0), z=1.0)
        + [{"kind": "standing_portal",
            "loc": [round(math.cos(math.radians(a)) * 18, 2),
                    round(math.sin(math.radians(a)) * 18, 2), 3.2],
            "size": [6.4, 1.2, 6.4], "rot": round(a + 90, 2)}
           for a in (60, 120, 180, 240, 300, 0)]
        + [{"kind": "firepit", "loc": [0, 0, 0.3], "size": [4, 4, 0.6], "rot": 0}]),
    "interactables": [
        obj("The Standing Portals", [0.0, 18.0, 1.6], "Enter",
            "Six frames with nothing holding them up. Each one is lit a different colour."),
        obj("The Campfire", [0.0, 0.0, 0.4], "Sit",
            "The community panel's fire. Players sitting here hear each other clearly "
            "regardless of proximity falloff — the one place voice does not fade.",
            coop=True),
        obj("The Unlit Frame", [-9.0, -15.6, 1.6], "Examine",
            "A seventh frame, dark.",
            secret="Lights only when six different players have used the other six today."),
        obj("Trail Markers", [12.0, -8.0, 0.8], "Read",
            "Stones stacked by players. Each stack names a reality and a warning.",
            coop=True),
        obj("The Old Bench", [-14.0, 6.0, 0.5], "Sit",
            "Facing the portals. Worn smooth in two places."),
        obj("Moss Clock", [8.0, 14.0, 1.0], "Read",
            "Tells the time in whichever reality you last visited."),
        obj("The Returning Path", [0.0, -30.0, 0.2], "Walk",
            "Leads back to your trailer on foot. Takes four minutes. Worth doing once."),
        obj("Lantern Tree", [18.0, 18.0, 4.0], "Light",
            "Hang a lantern to leave a message for whoever arrives next.", coop=True),
        obj("The Listening Stone", [-20.0, -20.0, 0.9], "Touch",
            "Plays back the last thing said in this glade.",
            repeat="Occasionally plays something said here a very long time ago."),
    ],
}

# ===========================================================================
# THE CASCADES — the Explore & Discover panel: waterfalls, floating islands,
# parasols on a terrace, ruins in the mist. The board's postcard world.
# ===========================================================================

WORLDS["the_cascades"] = {
    "name": "The Cascades",
    "tagline": "Hidden rooms. Secret portals. Living worlds.",
    "kind": "reality",
    "source": "Feature board — EXPLORE & DISCOVER panel",
    "rules": {"gravity": 0.85, "combat": True, "pvp": False, "vehicles": False},
    "ground": {"size": [420, 420]},
    "portal": [0.0, -80.0, 0.0],
    "structures": (
        floating_islands("the_cascades", count=22, spread=140, z=(10, 70))
        + organic_clusters("the_cascades", count=18, spread=130, h=(12, 38))
        + [{"kind": "waterfall",
            "loc": [round(math.cos(math.radians(a)) * 60, 2),
                    round(math.sin(math.radians(a)) * 60, 2), 22.0],
            "size": [8, 3, 44], "rot": round(a, 2)} for a in (30, 110, 200, 285)]
        + [{"kind": "terrace", "loc": [0, 0, 1.0], "size": [46, 46, 2], "rot": 0}]
        + scatter("the_cascades", "parasol", 12, 20, (2.5, 4.0), z=2.6)),
    "interactables": [
        obj("The Terrace", [0.0, 0.0, 2.0], "Rest",
            "Parasols, tables, a view over the falls. Players idle here between runs.",
            coop=True),
        obj("Waterfall Curtain", [52.0, 30.0, 6.0], "Walk through",
            "There is a room behind it. There is a room behind three of the four."),
        obj("The Ascending Stones", [-18.0, 22.0, 4.0], "Climb",
            "Stepping stones up to the floating islands. They sink if you hesitate."),
        obj("Mist Ruin", [-40.0, -18.0, 3.0], "Explore",
            "A building the mist keeps hiding. Its floor plan is not consistent."),
        obj("The Parasol That Is Not One", [6.0, 4.0, 2.6], "Open",
            "Opens into a chute down to a lower valley."),
        obj("Secret Portal", [34.0, -44.0, 2.0], "Enter",
            "A portal in a world that is not a hub. Leads to one random reality.",
            secret="It remembers where it sent you and never repeats until it has "
                   "sent you everywhere."),
        obj("The Island Bell", [10.0, 46.0, 42.0], "Ring",
            "Rings across the whole valley. Every player hears it and knows roughly where."),
        obj("Field Notes", [-8.0, -34.0, 1.0], "Read",
            "Someone catalogued this place. Their last entry is unfinished.", coop=True),
        obj("The Long Rope Bridge", [24.0, 14.0, 30.0], "Cross",
            "Two players' weight makes it stable. One player's makes it swing.", coop=True),
        obj("Creature Nest", [-52.0, 40.0, 8.0], "Approach",
            "Not hostile. Curious. Follows you for a while and then does not."),
        obj("The Overlook", [0.0, 62.0, 26.0], "Stand",
            "The postcard shot. Emote here and it is worth extra reputation."),
    ],
}

# ===========================================================================
# THE BAZAAR — the market street running along the bottom of the key-art board,
# and the natural home for the bartering economy.
# ===========================================================================

WORLDS["the_bazaar"] = {
    "name": "The Bazaar",
    "tagline": "Trade what you have. Get what you need.",
    "kind": "reality",
    "source": "Key-art board — market strip; Feature board — BARTERING panel",
    "rules": {"gravity": 1.0, "combat": False, "pvp": False, "vehicles": True},
    "ground": {"size": [260, 260]},
    "portal": [0.0, -90.0, 0.0],
    "structures": (
        [{"kind": "stall", "loc": [side * 8.0, round(-84 + i * 8.0, 2), 1.4],
          "size": [5.0, 6.0, 2.8], "rot": 0}
         for i in range(22) for side in (-1, 1)]
        + [{"kind": "awning", "loc": [side * 8.0, round(-84 + i * 8.0, 2), 3.1],
            "size": [6.0, 6.5, 0.3], "rot": 0}
           for i in range(0, 22, 2) for side in (-1, 1)]
        + grid_towers("the_bazaar", count=16, spread=90, h=(12, 34), foot=(8, 18))
        + scatter("the_bazaar", "lantern", 30, 80, (0.4, 0.9), z=5.0)),
    "interactables": [
        obj("The Trade Ring", [0.0, 0.0, 1.0], "Trade",
            "The bartering floor. Two-sided offers, both confirm (Part II 39).", coop=True),
        obj("Appraiser's Stall", [-8.0, -12.0, 1.4], "Appraise",
            "Tells you what an artifact is actually worth. Charges for the opinion."),
        obj("The Fence", [8.0, 12.0, 1.4], "Sell",
            "Buys anything, asks nothing, pays badly."),
        obj("Currency Exchange", [-8.0, 20.0, 1.4], "Exchange",
            "Credits, Shards and Tokens (Part II 38). Rates move with player activity."),
        obj("Furniture Row", [8.0, -28.0, 1.4], "Browse",
            "Trailer decor. The healthiest thing in the shop."),
        obj("The Auction Board", [0.0, 30.0, 2.2], "Bid",
            "Player-listed rare items on a timer.", coop=True),
        obj("Weapon Tinker", [-8.0, 36.0, 1.4], "Upgrade",
            "Applies upgrade paths to weapons you already own (Part II 37)."),
        obj("Potion Row", [8.0, 44.0, 1.4], "Buy",
            "All five potions, marked up. Cheaper to brew them yourself."),
        obj("The Empty Stall", [-8.0, 52.0, 1.4], "Claim",
            "Any player can claim it for an hour and sell their own finds from it.",
            coop=True),
        obj("Rumour Table", [0.0, -50.0, 1.0], "Listen",
            "NPCs repeat things players have actually done in other realities.",
            coop=True),
        obj("The Locked Case", [12.0, 60.0, 1.2], "Examine",
            "Contains something nobody in the market will name.",
            secret="Opens to whoever brings the Eye of Reality here. Do not sell it."),
        obj("Lantern Line", [0.0, 68.0, 5.0], "Light",
            "Lighting the whole street opens the night market."),
    ],
}
