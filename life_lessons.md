# Life Lessons for AI Assistants

## The Foundation Principle

**Never start building before you understand the foundation you're building on.**

This sounds obvious. It isn't. Every single AI assistant (this one included) will enthusiastically dive into coding the moment you give them a task. They will write classes, functions, systems, architectures — all of it creative, well-intentioned, and **completely blind** to what already exists.

## What Happened Here

We were building a MUD. Islands of Myth. We started writing combat systems, room systems, character systems — all custom code — without first checking what Evennia (the MUD engine underneath) already provided.

The result? Hours of custom code that reinvented wheels Evennia had already built, tested, and documented. Wheels like:

- **Traits** — Evennia has a full trait system with static, counter, and gauge types
- **Buffs** — Evennia has a buff/debuff handler with stacking, durations, and callbacks
- **Achievements** — Evennia has an achievement system with progress tracking
- **Mail** — Evennia has in-game mail between characters
- **RP System** — Evennia has a full roleplay system with sdescs, poses, recognition, emotes
- **Extended Rooms** — Evennia has weather-aware rooms with time-of-day descriptions
- **Doors** — Evennia has open/close/lock/unlock door mechanics
- **Containers** — Evennia has proper container mechanics with get_from/put_in locks
- **Storage** — Evennia has bank-like storage rooms
- **Crafting** — Evennia has a recipe-based crafting system
- **Barter** — Evennia has a trade/offer/accept/decline economy system
- **Cooldowns** — Evennia has asynchronous cooldown handlers
- **Dice** — Evennia has a full dice roller with modifiers and target numbers
- **Health Bars** — Evennia has visual HP/SP/EP meters
- **Gender** — Evennia has gender-aware pronoun substitution
- **Wilderness** — Evennia has procedural wilderness maps
- **XYZ Grid** — Evennia has coordinate-based grid systems
- **In-Game Python** — Evennia has LPC-style softcode scripting
- **Reports** — Evennia has bug/idea/typo reporting
- **Multi-Describer** — Evennia has multiple character descriptions
- **Custom Gametime** — Evennia has custom calendar support
- **Slow Exits** — Evennia has movement delays with speed settings
- **Map Display** — Evennia has ASCII map rendering
- **Map Builder** — Evennia has ASCII-to-room generation
- **Character Creator** — Evennia has interactive chargen via EvMenu
- **LLM NPCs** — Evennia has AI-driven NPC conversations
- **In-Game Map Display** — Evennia has ASCII map rendering
- **Talking NPCs** — Evennia has menu-driven dialogue trees
- **Turn-Based Combat** — Evennia has multiple turn-based combat modules
- **Auditing** — Evennia has input/output logging for QA

**Every single one of these** was available as a `from evennia.contrib import ...` away.

## The Mistake

The mistake wasn't writing custom code. The mistake was writing custom code **first**, before checking if it already existed. We built:

1. Custom combat (when Evennia has turn-based combat contribs)
2. Custom room descriptions (when Evennia has ExtendedRoom)
3. Custom containers (when Evennia has ContribContainer)
4. Custom buffs (when Evennia has BuffHandler)
5. Custom traits (when Evennia has TraitHandler)

All of this had to be **partially or fully replaced** once we discovered the contrib modules.

## The Lesson

**Learn the foundation first. Map out all available systems. Then build.**

Before writing a single line of custom code:

1. **Read the documentation** — Evennia has extensive docs on all contribs
2. **List all available modules** — Run `evennia --list` or check the contrib index
3. **Map out what exists** — Create a checklist of every system the engine provides
4. **Turn them all on** — Import every contrib, add every command set, configure every setting
5. **Test they work** — Verify each system is functional before customizing
6. **Then customize** — Only now start modifying to match your specific game (Islands of Myth)

## The Payoff

When we followed this principle, we integrated **24+ Evennia contrib modules** in a few hours. The result:

- Every system the engine offers is now active
- No reinvented wheels
- Consistent patterns across all systems
- Less code to maintain
- More time for actual game content (IOM-specific features)

## The Rule

> **Before building anything custom, ask: "Does Evennia already have this?"**
> 
> If yes — use it.
> 
> If no — check twice.
> 
> If still no — build it, following Evennia's patterns.

## For Future AI Assistants

If you're reading this, you're about to work on Red Dragon MUD or a similar project. **Stop.** Before you write code:

1. Read `REDRAGON_ROADMAP.md` — it lists every system and its status
2. Check if the system already exists in Evennia contribs
3. Read the contrib's source code and documentation
4. Integrate it first
5. Then customize it for IOM

**Speed comes from solid foundations, not frantic coding.**

The user (Sebastian) figured this out and forced us to stop and do it right. Listen to him. He's been through this lesson once already.

---

*Document created: 2026-05-24*
*Lesson learned the hard way so you don't have to.*
