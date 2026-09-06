# THE REALITY MACHINE

**Game Design Document — Master Vision / Developer Handoff**

*Working title. Original multiplayer psychedelic multiverse.*

| | |
|---|---|
| **Document status** | Master vision / developer handoff |
| **Primary engine** | Unreal Engine 5 |
| **3D pipeline** | Blender → Unreal Engine 5 |
| **Platforms** | PC, PlayStation, Xbox, Nintendo where technically feasible; future cloud/mobile possibilities |
| **Genre** | Multiplayer open-world exploration / social simulation / action adventure / psychedelic art experience |

> This GDD is the master build specification. New ideas should be judged
> against it rather than constantly changing the foundation.

**The worlds in this document exist as buildable data.** See
[`README.md`](README.md) — 19 spaces and 218 discoverable objects that generate
Blender blockouts, Unreal data tables and [a visual atlas](WORLDS.md) from one
source file.

---

## Table of contents

1. [High-level vision](#1-high-level-vision)
2. [Creative inspiration](#2-creative-inspiration)
3. [The player's trailer](#3-the-players-trailer)
4. [Trailer as personal museum](#4-trailer-as-personal-museum)
5. [Social trailers](#5-social-trailers)
6. [The Reality Machine](#6-the-reality-machine)
7. [Reality selection](#7-reality-selection)
8. [Shared realities](#8-shared-realities)
9. [Proximity voice chat](#9-proximity-voice-chat)
10. [Weapons](#10-weapons)
11. [Weapon discovery](#11-weapon-discovery)
12. [Weapon storage](#12-weapon-storage)
13. [Artifact system](#13-artifact-system)
14. [Death & respawn system](#14-death--respawn-system)
15. [Death animation](#15-death-animation)
16. [Exploration](#16-exploration)
17. [Environmental storytelling](#17-environmental-storytelling)
18. [Realities should feel alive](#18-realities-should-feel-alive)
19. [Art direction](#19-art-direction)
20. [Blender + Unreal pipeline](#20-blender--unreal-pipeline)
21. [Cross-platform design](#21-cross-platform-design)
22. [Multiplayer architecture](#22-multiplayer-architecture)
23. [The trailer → reality loop](#23-the-trailer--reality-loop)
24. [Player progression](#24-player-progression)
25. [Player-created realities — future feature](#25-player-created-realities--future-feature)
26. [Community system](#26-community-system)
27. [First vertical slice](#27-first-vertical-slice)
28. [Success criteria for the prototype](#28-success-criteria-for-the-prototype)
29. [Long-term vision](#29-long-term-vision)
30. [The one-sentence pitch](#30-the-one-sentence-pitch)
31. [Developer priority](#31-developer-priority)
- [The core design principle](#the-core-design-principle)

**Part II — systems from the concept boards** (see
[how Part II relates to Part I](#part-ii--systems-from-the-concept-boards))

32. [Portal hub & the portal network](#32-portal-hub--the-portal-network)
33. [The reality roster](#33-the-reality-roster)
34. [Character creator](#34-character-creator)
35. [The HUD](#35-the-hud)
36. [Potions & consumables](#36-potions--consumables)
37. [Crafting & upgrades](#37-crafting--upgrades)
38. [Economy & the shop](#38-economy--the-shop)
39. [Bartering — player-to-player trade](#39-bartering--player-to-player-trade)
40. [Missions, world events & boss fights](#40-missions-world-events--boss-fights)
41. [Minigames](#41-minigames)
42. [Pets & companions](#42-pets--companions)
43. [Vehicles](#43-vehicles)
44. [Party, voice UI & communities](#44-party-voice-ui--communities)
45. [Key art & marketing language](#45-key-art--marketing-language)
46. [Interactive object design](#46-interactive-object-design)
47. [IP compliance review of the concept art](#47-ip-compliance-review-of-the-concept-art)
48. [Open design questions](#48-open-design-questions)

---

## 1. High-level vision

The Reality Machine is a multiplayer psychedelic open-world experience where
players enter a mysterious machine inside their personal trailer and are
transported into completely different realities.

Players choose:

1. Their character
2. Their reality
3. Their experience

Each reality is an explorable world filled with strange environments,
interactive objects, NPCs, creatures, weapons, artifacts, secrets, puzzles,
hidden locations, environmental storytelling — and other players.

Players who choose the same reality can enter the same shared world and
interact with one another.

The player's trailer is their permanent home base. It functions as:

- Lobby
- Respawn point
- Museum
- Trophy room
- Armory
- Social space
- Customization space
- Reality-selection hub

### The fundamental gameplay loop

```
HOME → CHOOSE REALITY → EXPLORE → DISCOVER → INTERACT → COLLECT → SURVIVE
     → RETURN HOME → DISPLAY → INVITE FRIENDS → EXPLORE AGAIN
```

Once trading and upgrades exist (Part II 37-39), the home half of that loop
becomes the five-step wheel the concept boards show:

```
EXPLORE → COLLECT → TRADE → DISPLAY → UPGRADE → (explore again)
```

---

## 2. Creative inspiration

The project is inspired at a high conceptual level by:

**Psychedelic animated storytelling.** The inspiration is the idea of a
character entering a reality simulator and experiencing radically different
worlds, personalities, philosophies, environments and adventures.

**Immersive art experiences.** The game should take inspiration from the
principles behind immersive art attractions:

- Nonlinear exploration
- Hidden rooms
- Portals
- Surreal architecture
- Interactive installations
- Environmental storytelling
- Bizarre objects
- Interconnected narratives
- Multiple themed realities
- Community / social discovery

### Important IP rule

**The game must be an original intellectual property.**

Do not copy existing characters, dialogue, music, specific worlds, storylines,
logos, individual artworks, exact character designs, exact visual styles, or
copyrighted assets.

The goal is to create a new artistic language inspired by the broader ideas,
not a derivative copy.

---

## 3. The player's trailer

The trailer is the player's home universe. It should initially feel relatively
familiar and cozy while containing increasingly strange elements.

Think: **home + museum + spaceship + workshop + portal station.**

The trailer should be highly customizable. The player can customize:

- Furniture
- Walls
- Floors
- Lighting
- Posters
- Art
- Displays
- Weapon racks
- Artifact pedestals
- Collectibles
- Technology
- Decorations
- Character display areas
- Secret rooms

---

## 4. Trailer as personal museum

Everything the player discovers can potentially become part of their personal
collection.

### Weapons

Weapons recovered from realities can be **displayed** or **used**.

Certain weapons can only function inside the player's lobby unless
specifically permitted by another reality. This prevents extremely powerful
equipment from breaking other worlds.

### Artifacts

Artifacts become collectible pieces of the player's journey.

> **THE EYE OF REALITY**
> Origin: Reality 07
> Rarity: Legendary
> Status: Unknown

Artifacts can be:

- Displayed
- Examined
- Traded where permitted
- Used for progression
- Used to unlock secrets
- Used to unlock new realities

---

## 5. Social trailers

Players can invite other players into their personal trailer.

Visitors can:

- Explore
- Look at trophies
- See artifacts
- Socialize
- Show off collections
- Prepare for adventures
- Access approved activities
- Join the host's reality

This turns the trailer into a social identity. A player's trailer should
eventually communicate:

> *"This is who I am and everywhere I've been."*

---

## 6. The Reality Machine

The central device inside the trailer is the gateway to the multiverse.
Approaching it activates the interface:

```
SELECT YOUR REALITY
```

The player chooses a **character**:

- Human
- Alien
- Robot
- Creature
- Fantasy forms
- Custom avatars

Eventually: a **full character creator**.

---

## 7. Reality selection

Players browse available realities.

| # | Reality | What it is |
|---|---|---|
| 001 | **THE LIVING CITY** | A massive impossible city where architecture constantly changes |
| 002 | **THE DEEP** | A surreal underwater civilization |
| 003 | **THE GARDEN** | A living ecosystem where plants and creatures interact with players |
| 004 | **THE VOID** | A cosmic environment where physics behaves differently |
| 005 | **THE THOUGHT WORLD** | The environment reacts to player behavior |

These are examples — not final worlds.

Every reality should have its own art direction, physics, creatures, music,
rules, NPCs, story, weapons, artifacts and secrets.

---

## 8. Shared realities

This is one of the game's defining features.

When a player selects `REALITY: THE LIVING CITY` they may enter a shared
instance containing other players who selected that reality.

```
127 EXPLORERS CURRENTLY IN THIS REALITY
```

Players can talk, explore, fight, cooperate, solve puzzles, trade, discover
secrets, complete events, make friends, form groups, and explore hidden areas
together.

---

## 9. Proximity voice chat

Voice communication should feel natural.

| Situation | Result |
|---|---|
| A player nearby | Clear voice |
| A player farther away | Quieter voice |
| A player walking away | Voice fades |
| A player behind a wall | Sound becomes muffled |

This should make multiplayer feel like people are actually inhabiting the same
world rather than sitting in a traditional lobby.

---

## 10. Weapons

Weapons are an important part of the fun but should remain consistent with the
game's surreal identity. Weapons should not simply be conventional firearms.

**Reality weapons** — manipulate gravity, space, time, physics, size, distance.

**Organic weapons** — living or biological objects.

**Cosmic weapons** — based around stars, gravity, energy, space.

**Art weapons** — paint becomes physical; drawings become objects; sculptures
come alive; brushes reshape environments.

**Technology weapons** — strange futuristic machines.

**Absurd weapons** — ridiculous objects with surprisingly useful abilities.

---

## 11. Weapon discovery

Weapons should be discovered rather than simply purchased from a menu.

Players might find them, earn them, craft them, defeat creatures for them,
solve puzzles for them, or discover secret rooms containing them.

Weapons should have rarity, abilities, lore, visual identity, and upgrade
paths.

---

## 12. Weapon storage

When a player returns home, weapons can be stored inside the trailer. The
player can build:

- Weapon walls
- Weapon racks
- Display cases
- Pedestals
- Secret vaults

A rare weapon becomes something the player can physically show other people.

---

## 13. Artifact system

Artifacts are separate from weapons. They represent discoveries.

Artifacts could:

- Unlock lore
- Open portals
- Change trailer decorations
- Unlock cosmetics
- Unlock quests
- Activate machines
- Reveal hidden realities
- Trigger environmental events

Some artifacts should be extremely rare. This creates a long-term collection
system.

---

## 14. Death & respawn system

This is a core mechanic. When the player dies inside a reality, they do **not**
remain there. Instead:

```
DEATH
  ↓
Reality reacts
  ↓
The player is shot / ejected back through the portal
  ↓
The player returns to their trailer
  ↓
They spawn inside their personal lobby
```

There should be no generic `Reality Connection Lost` message. The return should
feel like a physical part of the universe — the player is literally thrown back
home from the reality.

---

## 15. Death animation

Potential sequence:

1. Player dies.
2. The environment distorts.
3. The reality collapses around the character.
4. A portal opens.
5. The player is pulled backward.
6. They shoot through a psychedelic tunnel.
7. The screen transitions.
8. The player lands back inside their trailer.

Then they can immediately recover, change equipment, talk to friends, display
discoveries, or enter another reality.

---

## 16. Exploration

The game should reward curiosity. Avoid constantly telling the player
`GO HERE` / `DO THIS` / `KILL THIS` / `COLLECT THAT`.

Instead, make the world itself interesting enough to explore. A player might
see:

- A strange door
- A moving building
- A talking object
- A staircase going nowhere
- A creature hiding behind something
- A portal inside a refrigerator
- A strange sound underground

The player chooses whether to investigate.

---

## 17. Environmental storytelling

Stories should often be discovered rather than explained. A player may find
notes, recordings, symbols, objects, secret rooms, NPC conversations,
environmental changes, and strange artifacts.

Different players may discover different pieces of the same mystery.

---

## 18. Realities should feel alive

The environments should not simply be beautiful backgrounds. They should
react:

- Buildings move
- Plants respond to players
- Creatures interact with each other
- Objects have personalities
- Weather changes
- Music responds to environments
- Architecture transforms
- NPCs remember interactions
- Portals change locations
- Hidden areas reveal themselves

---

## 19. Art direction

The visual identity should combine psychedelic imagery, surreal environments,
experimental animation, immersive installation principles, organic
architecture, cosmic imagery, handmade textures, strange creatures, neon
environments, analog technology, abstract geometry, dream logic, interactive
art, and sound-reactive visuals.

But the final product needs its own recognizable art direction.

**The objective:** make players feel like they walked into an impossible
interactive art museum that happens to be a video game.

---

## 20. Blender + Unreal pipeline

**Blender** — 3D modeling, sculpting, characters, creatures, props, weapons,
environments, rigging, animation, custom assets.

**Unreal Engine 5** — gameplay, multiplayer, lighting, materials, physics,
world building, AI, audio, VFX, UI, portals, networking, save systems,
optimization.

AI coding assistance can help developers create systems, but AI should not
replace the artistic direction of the project.

---

## 21. Cross-platform design

Design the core technology to support scalable graphics.

**Target:** PC, PlayStation, Xbox, and Nintendo hardware where technically
feasible.

**Potential future:** cloud, mobile.

Graphics should have scalable settings. High-end machines can use high-quality
lighting, high-resolution textures, advanced effects and dense environments.
Lower-end devices should use optimized LODs, textures, lighting, particles and
geometry.

---

## 22. Multiplayer architecture

The developer should design multiplayer from the beginning rather than
attempting to add it later.

Core systems:

- Player accounts
- Character identity
- Persistent inventory
- Trailer ownership
- Friends
- Parties
- Shared realities
- Matchmaking / instances
- Voice chat
- Player synchronization
- Item persistence
- Save data

---

## 23. The trailer → reality loop

1. Spawn in trailer.
2. Customize character / equipment.
3. Interact with the Reality Machine.
4. Choose character.
5. Choose reality.
6. Enter portal.
7. Arrive in shared reality.
8. Explore.
9. Meet other players.
10. Fight / solve puzzles / investigate.
11. Discover weapons and artifacts.
12. Return through portal — or die and get ejected back home.
13. Return to trailer.
14. Display discoveries.
15. Invite friends.
16. Enter another reality.

---

## 24. Player progression

Progression should not simply mean Level 1 → Level 2 → Level 3. Instead,
progression can include:

- Collection
- Discovery
- Reputation
- Character customization
- Trailer expansion
- Reality access
- Weapon mastery
- Artifact collection
- Secrets discovered
- Social relationships
- Achievements

---

## 25. Player-created realities — future feature

**This should not be part of the first prototype.** But eventually:

```
CREATE YOUR REALITY
```

Players could eventually customize:

- **Environment** — city, jungle, ocean, space, desert, dream, abstract
- **Physics** — normal gravity, low gravity, flying, floating, changing gravity
- **Creatures**
- **Music**
- **Weather**
- **Rules**
- **Objects**
- **Architecture**

This could eventually become one of the game's biggest features.

---

## 26. Community system

Players can eventually form clubs, exploration groups, art communities, teams,
bands, trading groups, secret societies, and world-specific communities.

The goal is for the game to encourage real social connection, not simply
anonymous matchmaking.

---

## 27. First vertical slice

**Do NOT attempt the entire multiverse first.** The first playable prototype
should contain:

| Piece | Scope |
|---|---|
| **The trailer** | One highly polished trailer |
| **The player** | Basic character |
| **The Reality Machine** | Fully functional |
| **Character selection** | Basic customization |
| **World selection** | One playable reality |
| **Portal** | Fully animated transition |
| **First reality** | One beautiful surreal world |
| **Interaction** | At least 10–20 interactive objects |
| **NPCs** | 3–5 basic characters |
| **Weapons** | Several prototype weapons |
| **Artifacts** | Several collectible objects |
| **Multiplayer** | Multiple players inside the same reality |
| **Proximity voice** | Basic implementation |
| **Death** | Player gets ejected back to trailer |
| **Return** | Player can immediately re-enter |
| **Trailer storage** | Display at least one weapon and artifact |
| **Invitations** | Invite another player to your trailer |

---

## 28. Success criteria for the prototype

The prototype succeeds if someone who has never heard the game's pitch can play
it and naturally understand:

- *"This is my home."*
- *"That's the machine."*
- *"I can choose where to go."*
- *"Other people are actually here."*
- *"I can find crazy stuff."*
- *"If I die, I go home."*
- *"I can bring things home."*
- *"I want to go back in."*

**That last feeling is the most important.**

---

## 29. Long-term vision

The eventual game should feel like a living multiverse. New realities can be
introduced through updates. Each new reality can contain new art direction, new
creatures, new weapons, new artifacts, new mechanics, new NPCs, new mysteries,
and new multiplayer events.

The universe should continue expanding.

---

## 30. The one-sentence pitch

> The Reality Machine is a multiplayer psychedelic multiverse where players
> customize their own character, enter a mysterious machine inside their
> personal trailer, travel into impossible shared realities, discover strange
> weapons and artifacts, explore with other players, and bring their
> discoveries home to build a personal museum of everything they've
> experienced.

---

## 31. Developer priority

**DO NOT BUILD EVERYTHING AT ONCE.** Build in this exact order:

```
 1. Trailer
 2. Player
 3. Reality Machine
 4. Character selection
 5. One portal
 6. One reality
 7. Exploration
 8. One weapon
 9. One artifact
10. Multiplayer
11. Proximity voice
12. Death / ejection
13. Return to trailer
14. Trailer displays
15. Invite friends
16. Polish
17. Expand to Reality #2
```

---

## The core design principle

Don't build a game that merely looks crazy. Build a world where players are
constantly thinking:

- *"What the hell is that?"*
- *"Can I go in there?"*
- *"What happens if I touch this?"*
- *"Where did that portal come from?"*
- *"How did that player get that weapon?"*
- *"What happens if we go through together?"*
- *"I have to bring this artifact home."*

That's the experience that should drive every design decision.

---
---

# PART II — SYSTEMS FROM THE CONCEPT BOARDS

Part I above is the foundation and stays the arbiter: when anything here
conflicts with it, Part I wins. This part documents the systems that appear on
the concept boards and reference images but were not written down in the
original 31 sections — economy, potions, bartering, minigames, pets, vehicles,
the portal hub, the HUD, and the interactive-object language.

**None of Part II belongs in the first vertical slice** (§27) unless §27 or §31
already names it. Everything here is post-slice scope, listed now so the
architecture is built to accept it rather than retrofitted around it. Two
things in particular need early architectural room even though they ship late:
the **economy/inventory** (item identity, ownership, persistence) and
**bartering** (server-authoritative trade), because bolting either onto a
finished inventory is a rewrite.

---

## 32. Portal hub & the portal network

The concept boards show two related spaces that sit between the trailer and the
realities. Both are optional layers over §6 — the Reality Machine in the
trailer must always work on its own, without either of them.

### The portal network (the Machine's browse view)

A vast ring showing the multiverse: galaxies, worlds, drifting structures,
traffic between them. This is the visual language for **browsing realities**
(§7) rather than a place the player stands in. It should read as *scale* — the
player is one traveler at the edge of something enormous.

The lone drone at the traveler's shoulder in that image is the seed of the
**companion** system (§42).

### The portal hub (a physical crossroads)

A built structure — catwalks, bridges, gantries, machinery — with several
active portals arranged around a central **CORE**:

| Slot | Working name | Read |
|---|---|---|
| P1 | *(crystalline)* | Shattered ice / crystal world |
| P2 | **Bio-Metropolis** | Grown-not-built city on a world-tree |
| P3 | **Plasma-Strait** | Storm-lashed wreck fields, lightning skies |
| P4 | **Ruins-Labyrinth** | Overgrown temple maze |
| P5 | **Gravity-Ring** | Ringed planet, orbital approach |
| — | **CORE** | The hub's own power source and its central mystery |

Each portal carries a small **tag strip** of icons — a glanceable summary of
what is through it (biome, hazard, activity type, difficulty). Players standing
at a portal can see the tags before committing.

Design intent: the hub is where players **run into each other between
realities**. It is the multiplayer commons — the place you see somebody else's
weapon and ask where they got it. Treat it as a social space with portals in
it, not a menu with art on it.

**Rule:** the hub is a shortcut, never a toll gate. Dying still ejects the
player home to their trailer (§14) — never to the hub.

---

## 33. The reality roster

Extending §7 with everything the boards name. Player counts shown on the boards
(127 / 83 / 64 / 91 / 48) are examples of the **live population readout** the
selection UI should show, not targets.

| Reality | Flavour | Source |
|---|---|---|
| **The Living City** | Impossible city, architecture in motion | §7 |
| **The Deep** | Surreal underwater civilization | §7 |
| **The Garden** | Living ecosystem, plants respond | §7 |
| **The Void** | Cosmic, physics behaves differently | §7 |
| **The Thought World** | Environment reacts to player behavior | §7 |
| **The Dreaming** | Surreal / dream-logic world | Concept board |
| **The Wasteland** | Post-apocalyptic | Concept board |
| **The Pet Sanctuary** | Calm forest world, no combat | Concept board |
| **Bio-Metropolis** | Grown city on a world-tree | Portal hub board |
| **Plasma-Strait** | Storm and wreckage | Portal hub board |
| **Ruins-Labyrinth** | Overgrown temple maze | Portal hub board |
| **Gravity-Ring** | Ringed world, variable gravity | Portal hub board |
| **The Arcade** | Neon city of playable machines | See §41 and §47 |
| **The Shatter** | Crystalline world that rings underfoot | Portal hub board (P1) |
| **The Portal Glade** | Portals standing in forest, no architecture | Feature board — THE PORTALS |
| **The Cascades** | Waterfalls, floating islands, a terrace | Feature board — EXPLORE & DISCOVER |
| **The Bazaar** | Market street; home of the trade economy | Key-art board — market strip |

### The Portal Glade — the quiet way in

The boards show portals twice: once as built machinery (§32) and once as bare
frames standing between trees, lit from within, with a fire going. Both should
exist. The glade is the multiverse without the technology — you walk into the
woods and there are doors. It is also where the campfire from the community
panel lives, and the one place in the game where proximity voice does **not**
fall off: sit at the fire and everyone at the fire hears you.

### The Pet Sanctuary — a deliberate change of pace

Worth calling out because it breaks the pattern on purpose: a warm, sunlit
forest, a cottage doorway ringed with carved runes, a fire going inside,
animals wandering. No weapons, no threat, no timer.

This is the roster's **rest state**. A multiverse that is relentlessly loud
gets exhausting; one quiet world makes the loud ones land harder. It is also
where companions are met and adopted (§42), which gives players a non-combat
reason to go somewhere.

---

## 34. Character creator

§6 lists the archetypes. The boards show the editor itself:

- **Body**
- **Face**
- **Hair**
- **Skin**
- **Tattoos / markings**
- **Clothes**
- **Accessories**
- Palette swatches per category, preset heads, and a **Save** for named presets

Presets across human, alien, robot, creature and fantasy forms let a new player
be done in fifteen seconds; the full editor is there for the player who wants
an hour. Both paths must exit to the same place: standing in front of the
Machine, ready to go.

Cosmetics bought or earned (§38) feed straight back into these categories.

---

## 35. The HUD

Drawn from the in-world reference frames. Keep it minimal — the world is the
point, and every element earns its pixels.

| Element | Notes |
|---|---|
| **Health** | Bar, bottom-right cluster |
| **Aether** | The resource that powers reality-manipulating weapons and abilities |
| **Credits** | Current balance, only while relevant |
| **Progress / level** | See the caution below and §47 |
| **Artifact toast** | On pickup: name, rarity, a beat of presence — then gone |
| **Objective callout** | Only for an accepted challenge, never ambient nagging |
| **Mini-map** | Reality hubs and zone links; per-reality, and some realities should refuse to give the player one |
| **Proximity voice** | See §44 |

**Caution on the level bar.** §24 is explicit that progression should *not*
reduce to Level 1 → 2 → 3. A visible XP bar quietly makes numbers the point.
Either drop the level readout, or keep levels as one signal among many
(collection, discovery, reputation, secrets) and never gate a reality behind a
level number — gate it behind an artifact, which is §13's job. Flagged in §47
as a decision the team owes an answer to.

---

## 36. Potions & consumables

Temporary effects with real durations, found, crafted, traded and used.

| Potion | Effect | Duration |
|---|---|---|
| **Hype** | +Speed, +Stamina, euphoria | Short |
| **Invisibility** | Stealth, breaks detection | ~5 min |
| **Strength** | +Damage, +Endurance | ~10 min |
| **Mind Trip** | Hallucinations, vision change | ~10 min |
| **Healing** | Health regen, removes status effects | ~5 min |

Design notes:

- **Mind Trip is the signature one.** It is the whole game's identity in a
  bottle — a consumable that changes how the world *looks* rather than what the
  player's numbers are. Other players should be able to tell you are on it.
- Effects must be **visible on other players** — this is a multiplayer game, and
  a buff nobody can see is a spreadsheet entry.
- **No stacking into invincibility.** One effect per category; a new potion of
  the same category replaces rather than adds.
- Nothing here should read as a real-world drug reference. These are reality
  effects, not substances.
- Availability follows the same lobby/reality permission rule as weapons (§4) —
  a reality may forbid a consumable.

---

## 37. Crafting & upgrades

Weapons carry upgrade paths (§11). The boards make the verbs explicit:
**discover → craft → upgrade** for weapons, and **craft / find / trade / use**
for potions.

- Materials come from realities — harvested, looted, dropped by creatures,
  found in secret rooms.
- Crafting happens in the **trailer workshop** (§3), which gives the home base a
  job beyond display.
- Upgrades should change *behavior*, not just damage numbers. A Paint Blaster
  upgrade that makes the paint climb walls is worth ten upgrades that add 5%.

---

## 38. Economy & the shop

Three currencies, deliberately separated so that time, luck and participation
each buy something different:

| Currency | Earned by | Spends on |
|---|---|---|
| **Credits** | Ordinary play | Everyday goods, furniture, most cosmetics |
| **Shards** | Rare finds, deep exploration | Rare cosmetics, high-end upgrades |
| **Tokens** | Timed events (§40) | Event-exclusive items |

**Shop categories:** skins, emotes, furniture, vehicles, upgrades, special
items.

Rules the design should hold to:

- **Never sell artifacts.** Artifacts are the record of where a player has
  actually been (§13); a purchasable artifact is a lie in a museum.
- Never sell power that can't be found. Anything that changes outcomes should be
  discoverable in a reality.
- Furniture and trailer decor are the healthiest thing in the shop — they feed
  the museum (§4) and the social space (§5).

---

## 39. Bartering — player-to-player trade

A two-sided trade window: **your offer** on the left, **their offer** on the
right, both parties confirm.

Requirements:

- **Server-authoritative.** The server owns item ownership; the client only
  displays it. Everything else here is negotiable, this is not.
- Both sides confirm, with a short lock after the final change so nobody can
  swap an item at the last instant.
- Per-item and per-world **trade permissions** (§4: *"traded where permitted"*).
  Some artifacts should be untradeable, and the item should say so on its card.
- A trade log the player can look back at.

Trading is what turns §26's trading groups from a label into an activity, and
it is the reason another player's trailer is worth visiting.

---

## 40. Missions, world events & boss fights

Four activity types: **PvP**, **PvE**, **world events**, **boss fights**.

World events are timed, shared, and visible to everyone in the reality. The
board's example:

> **EVENT: THE RIFT** — *Time left: 2h 34m*
> • Defeat the Rift Guardian
> • Collect 5 Energy Cores
> **Reward:** 500 Credits + rare artifact

Design notes:

- Events are the answer to *"why is anyone else here right now?"* — they give
  strangers a reason to cooperate without a group invite.
- Keep the announcement in-world where possible: the sky changes, something
  arrives, the architecture reacts (§18). A banner is the fallback, not the
  plan.
- PvP must be **opt-in or zoned**. A player carrying an artifact home should
  never lose it to an ambush — that breaks the collection promise the whole
  game rests on.
- Boss fights are the natural gate for legendary artifacts.

---

## 41. Minigames

Portals inside the hub lead to self-contained games — small, replayable, with
leaderboards and cosmetic rewards.

| Minigame | Challenge | Reward |
|---|---|---|
| **Racer's Edge** | *Urban Velocity* | "Neon Rider" bike skin |
| **Retro Arcade Vortex** | *Arcade Arena 8-bit* | Retro Artifact ×1 |
| **Gravity Arena** | *Float Fights* — zero-g combat | Anti-Grav Boots |
| **Mystery Vault** | *Decryptor 7* — cipher puzzle | Holographic trailer decor |
| **Neon Deathtrack** | Race variant | Vehicle cosmetics |
| **Dungeon Crawl** | Top-down co-op crawl | Consumables, materials |

Design notes:

- Leaderboards are per-minigame, showing a top name and score.
- Rewards should be **things you can display at home** — a skin, a decor piece,
  a retro artifact for the shelf. That keeps minigames inside the museum loop
  instead of off to the side.
- Two players entering the same portal together land in the same match.
- **Every retro game inside The Arcade must be original.** See §47. This is the
  single biggest legal exposure in the whole concept set.

---

## 42. Pets & companions

Two related things:

**Companions** — the small drone at the traveler's shoulder in the portal
network art. A companion follows the player into realities, carries a light
utility (spotting interactables, lighting dark spaces, holding overflow loot,
reacting to danger), and is customizable.

**Pets** — met and adopted at The Pet Sanctuary (§33). They live in the trailer,
react to the player and to visitors, and can be displayed and fussed over.

Notes:

- Pets in the trailer are a **social object**: visitors (§5) should be able to
  interact with them.
- Give them opinions. A pet that hides from a particular artifact is
  environmental storytelling (§17) for free.
- Keep companions non-combat, or nearly so. They are company, not a second gun.

---

## 43. Vehicles

Listed on the feature bar and visible in the hub art. Vehicles are traversal and
identity: bikes, hovercraft, and reality-specific oddities.

- Stored and displayed in or beside the trailer.
- Skins are shop and minigame rewards (§41).
- Some realities forbid them; some are built around them.
- A vehicle should always be optional. Nothing essential may be locked behind
  owning one.

---

## 44. Party, voice UI & communities

**Party list.** Named party members down the side, each with an individual
volume slider and a speaking indicator.

**Proximity voice readout.** §9 defines the behavior; the UI makes it legible
with a distance state — **Nearby / Farther / Very far / Behind wall** — plus a
push-to-talk indicator. Players need to understand *why* someone got quiet, or
they will assume the game is broken.

**Communities** (§26), as the boards name them: exploration groups, study
groups, walking groups, trading groups, art collectives, gaming squads, and
**create your own**. They surface in the trailer's Friends panel and travel with
the player into realities.

**Trailer bottom bar:** Customize · Inventory · Museum · Friends · Reality
Machine.

---

## 45. Key art & marketing language

Lines that appear across the boards, kept here so the team writes with one
voice:

- *Infinite worlds. Yours to explore.*
- *Infinite worlds. Real people. Your story.*
- *Same trailer. Infinite worlds.*
- *Explore • Collect • Connect • Return • Repeat*
- *Be you. Or be something else.* (character creator)
- *Different worlds. Different rules.* (reality selection)
- *Magic effects. Real consequences.* (potions)
- *You don't stay down.* (death & respawn)

The visual signature across every board: deep blue-black grounds, magenta and
cyan light, portal rings as the recurring shape, and warm interior light in the
trailer against cold light outside it. That contrast — **cozy home, impossible
outside** — is the art direction in one image, and §19's brief in practice.

---

## 46. Interactive object design

This is the texture the game lives or dies on, and it deserves its own rules.

**The reference:** a marble bust on a pedestal in an otherwise ordinary lobby.
A character walks up, holds a mug under its chin, and the bust pours coffee.
Nobody reacts. It is simply the coffee machine.

That is the register. Not "look how weird this is" — the world is weird and
completely unbothered about it. **Play absurdity straight.** The joke is that
it works, that it is routine, that the NPC standing next to it is only annoyed
you took the last cup.

### Rules for interactive objects

1. **The world never winks.** No object comments on its own strangeness. NPCs
   treat the impossible as municipal infrastructure.
2. **Ordinary silhouette, impossible function.** A bust, a fridge, a payphone, a
   vending machine, a statue. Readable at a glance, wrong on contact — that gap
   is the entire effect.
3. **Reward the second interaction.** Anything worth touching once should do
   something different the third time, or at night, or when two players touch it
   together.
4. **Consequences, however small.** Coffee that actually buffs. A statue that
   remembers you. A door that stays open for everyone after one player opens it.
5. **No tutorial prompts on the funny ones.** Let players find them and tell
   each other. §16's whole argument is that discovery beats instruction.
6. **Make them multiplayer.** An object two players must operate together
   creates a conversation with a stranger, which is what §8 is for.

### Object catalog for the vertical slice

§27 asks for 10–20 interactive objects in the first reality. A starting set,
all original:

| # | Object | What it does |
|---|---|---|
| 1 | **The Bust** | Marble head on a pedestal. Hold a mug under it — coffee. Buffs stamina. Occasionally pours something else. |
| 2 | **The Wrong Fridge** | Ordinary fridge. Inside is a corridor. |
| 3 | **The Complaining Door** | Locked, and it will explain at length why. |
| 4 | **Staircase to Nowhere** | Ends in air. Keep walking up anyway and something happens. |
| 5 | **The Payphone** | Rings when a player walks past. Someone is on the line. |
| 6 | **The Vending Machine** | Dispenses objects from other realities. Never the same twice. |
| 7 | **The Puddle** | Reflects a version of the reality that isn't this one. |
| 8 | **The Chair That Waits** | Moves closer whenever nobody is looking. |
| 9 | **The Mailbox** | Delivers notes other players left in this reality (§17). |
| 10 | **The Loud Painting** | Music, but only within two meters. |
| 11 | **The Chandelier** | Swings toward the nearest player. Points somewhere at night. |
| 12 | **The Bench of Agreement** | Two players sit — something opens. |
| 13 | **The Bureaucrat's Desk** | Stamp a form and a wall moves elsewhere in the level. |
| 14 | **The Fountain** | Drop an item in; get a different one back. |
| 15 | **The Elevator** | Six buttons. Four go to floors. |
| 16 | **The Telescope** | Shows other realities. Sometimes shows this street. |
| 17 | **The Cat** | Not a pet. Leads players somewhere if followed patiently. |
| 18 | **The Radio** | Tunes across stations; one is broadcasting from inside this building. |
| 19 | **The Broken Clock** | Correct twice a day, and *something* happens at those times. |
| 20 | **The Suggestion Box** | Player writes something. It shows up later, in the world. |

Each one should take a designer an afternoon and give players a story to tell.

---

## 47. IP compliance review of the concept art

§2 sets a hard rule: **The Reality Machine must be original IP.** Several
reference boards violate it. They are usable as *mood* — none of the following
may reach production, and none should be shown publicly as-is, including in
pitch decks.

| Board element | Problem | Replace with |
|---|---|---|
| "The Oasis," "The Stacks," "Key of Aech," "Ready Player One Challenge" | Names, setting and plot device from a copyrighted novel/film | An original hunt with original naming — see below |
| Pac-Man, Mario, Joust and other arcade characters on marquees, screens and streets | Third-party characters and game IP, reproduced recognizably | Original 8-bit games and mascots designed in-house |
| "Eye of Agamoto" | Marvel artifact | **The Eye of Reality** — already the GDD's own legendary artifact (§4) |
| Winged/armored hero figure | Reads as an existing character design | Original silhouette from the character creator (§34) |
| Real-world brand billboards | Trademark | Fictional in-world brands (one board already labels a billboard *"FICTIONAL PRODUCT"* — do that everywhere) |

**What is worth keeping from those boards**, restated as original design:

- A **neon arcade city** where the games are physically enterable — that concept
  is not owned by anyone, only its specific execution is. Build The Arcade with
  our own machines, our own mascots, our own 8-bit worlds.
- A **multi-part hunt** spanning several realities: collect three keys hidden in
  different worlds, each behind a different kind of challenge, to open something
  the community has to solve together. Give it original naming from our own
  fiction — the CORE (§32) is a natural anchor for it.
- The **HUD language** (§35) and the **mini-map** with reality hubs and zone
  links.
- **Battle-arena zones** inside a hub city — see §40's PvP zoning rule.

One practical note for asset generation: image tools reproduce recognizable
characters readily, so treat every generated board as reference only, and put an
explicit originality check into the art review before anything is modeled in
Blender. This applies to marquees, posters, screens and background signage — the
easiest place for third-party IP to survive unnoticed into a shipped build.

*This is a design constraint, not legal advice. Have counsel review the art
before anything ships publicly.*

---

## 48. Open design questions

Decisions the concept boards raise but do not settle. Each needs an answer
before the system it belongs to is built.

1. **Levels vs. §24.** Does a visible XP/level bar exist at all? §24 argues
   against numeric progression; the boards show a level readout. Pick one, and
   if levels stay, they may never gate a reality. (§35)
2. **PvP scope.** Opt-in, zoned, or event-only? And is loot ever at risk? The
   recommendation here is: zoned or opt-in, and **never** artifact loss. (§40)
3. **Does the portal hub replace the trailer's Machine, or sit beyond it?** The
   recommendation here is: beyond it. The trailer stays the front door, always.
   (§32)
4. **Real-money boundary.** Are Credits/Shards/Tokens purchasable, or earned
   only? This decision shapes the whole economy and cannot be reversed quietly
   after launch. (§38)
5. **Trade permissions.** Which artifacts are untradeable, and who decides — the
   item, or the reality it came from? (§39)
6. **Aether.** Is it a per-weapon resource, a character resource, or reality
   scenery? (§35)
7. **Do minigames need to exist before Reality #2?** §31 says expand to Reality
   #2 after polish; minigames are cheaper than a world and may be the better
   second content drop. Deliberate call, not a default.
