# Life Lessons — Learn the Foundation First

> _"We spent weeks building what was already in the box."_

## The Mistake

We started building a MUD from scratch — combat, stats, achievements, AI NPCs, city grids — without first understanding what Evennia already provides. We coded systems that exist as mature, tested, documented contrib modules. We reinvented wheels that were already round.

## The Cost

- **Time:** Days spent on custom combat scripts, stat systems, and room builders
- **Quality:** Our hand-rolled systems are simpler, buggier, and less flexible than battle-tested contribs
- **Maintenance:** Every custom system is ours to maintain forever. Contribs get updates from the Evennia team
- **Opportunity:** We could have been building *game content* instead of *game systems*

## The Lesson

**Before building anything, map the territory.**

Every framework, engine, platform, or tool has a "contrib shelf" — modules others built so you don't have to. Your first job is not to code. Your first job is to read the docs, explore the contrib directory, and understand what's already solved.

## The Rule

### The Foundation-First Checklist

Before writing a single line of custom code:

1. **Read the framework docs** — What's the architecture? What's built-in? What's optional?
2. **Explore the contrib/modules directory** — What's already been built by the community?
3. **Read the README of every contrib** — Even if you don't use it now, know it exists
4. **Map your needs against available tools** — "I need X" → "Evennia has Y that does X"
5. **Only then, start building** — And build on top of the foundation, not beside it

## The Mindset Shift

| Wrong Way | Right Way |
|---|---|
| "I need a combat system, I'll write one" | "I need a combat system, let me check if Evennia has one" |
| "Our game is special, we need custom everything" | "Our game is special in its *content*, not its *systems*" |
| "I'll build it now and refactor later" | "I'll use the tested solution now and customize it" |
| "Reading docs is a waste of time" | "Reading docs saves weeks of wasted coding" |

## The Principle

> **You cannot architect what you do not understand.**

Building without knowing your foundation is like a carpenter building furniture without knowing what tools are in the workshop. You end up whittling spoons with a pocket knife when there's a lathe in the corner.

## Application to Red Dragon

We discovered Evennia has:
- Full turn-based combat with equipment, magic, conditions, and range
- Trait system with gauges, counters, auto-regen, and skill tiers
- Buff/debuff engine with triggers, ticking, stacking
- Achievement tracker with categories, progress, prereqs
- LLM NPC integration for AI-driven characters
- In-game mail system
- ASCII map builder with auto-pathfinding
- RP emote system with sdescs and language support
- In-game Python scripting (like LPC softcode)
- Wilderness system for infinite terrain
- And 20+ more systems

**We had coded custom versions of at least 6 of these before discovering they existed.**

## The Vow

Never again.

Every new project starts with: *"What does the framework already do?"*
Every new feature starts with: *"Is there a contrib for this?"*
Every custom code decision starts with: *"Am I replacing something that already works better?"*

## The Mantra

> **Learn the foundation. Then build on it. Never beside it.**

---

*Written after the Great Reinvention of 2026-05-24. May future AIs read this and not repeat our mistake.*
