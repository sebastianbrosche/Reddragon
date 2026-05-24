# Life Lessons — For Future AIs

## The Golden Rule

**Learn the foundation before you build.**

This seems obvious. It is not.

## The Mistake We Made

We started building a MUD — rooms, NPCs, combat, shops — without first understanding what Evennia already provides. We wrote custom code for systems that already existed, tested, and documented in Evennia's contrib modules. We reinvented wheels that were not only round but came with suspension, ABS, and cruise control.

Specific examples:
- We built a custom buff system. Evennia has `evennia.contrib.rpg.buffs`.
- We planned a custom trait/stats system. Evennia has `evennia.contrib.rpg.traits`.
- We thought about custom dice rolling. Evennia has `evennia.contrib.rpg.dice`.
- We pondered how to do weather. Evennia has `evennia.contrib.grid.extended_room`.
- We discussed door mechanics. Evennia has `evennia.contrib.grid.simpledoor`.
- We considered a custom RP/emote system. Evennia has `evennia.contrib.rpg.rpsystem`.
- We mulled over achievements. Evennia has `evennia.contrib.game_systems.achievements`.
- We needed mail. Evennia has `evennia.contrib.game_systems.mail`.
- We thought about crafting. Evennia has `evennia.contrib.game_systems.crafting`.
- We considered clothing/equipment. Evennia has `evennia.contrib.game_systems.clothing`.
- We talked about trading. Evennia has `evennia.contrib.game_systems.barter`.
- We wanted cooldowns. Evennia has `evennia.contrib.game_systems.cooldowns`.
- We pondered in-game scripting. Evennia has `evennia.contrib.base_systems.ingame_python`.

All of these are battle-tested, documented, and maintained by the Evennia team.

## Why This Happened

1. **Overeager execution** — We had a vision (Islands of Myth) and wanted to realize it immediately.
2. **Assumption of uniqueness** — We assumed our needs were so specific that no generic system could handle them.
3. **Documentation blindness** — We didn't read the contrib directory listing before writing code.
4. **Lack of inventory** — We didn't catalog what was available before starting.

## The Fix

**Before writing a single line of code:**

1. **Read the contrib directory** — `ls /path/to/evennia/contrib/` — see what's there.
2. **Read the docs** — Each contrib has a module docstring explaining its purpose and installation.
3. **Map systems to your needs** — Make a table: "Our Need" → "Evennia Solution" → "Customization Required".
4. **Install and test** — Add the contrib, verify it works, understand its API.
5. **Customize, don't replace** — Build ON TOP of the foundation, not beside it.

## The Principle

> "It is better to have a system in place and modify it to look like what you want, than to wing it and swing blindly in the dark."

Evennia's contrib modules are not restrictions — they are shoulders to stand on. They handle edge cases, persistence, command parsing, and integration that you haven't thought of yet. Use them.

## Checklist for Future Projects

- [ ] Read all contrib module listings before starting
- [ ] Document which contribs map to which project requirements
- [ ] Create an integration roadmap with phases
- [ ] Implement contribs in dependency order (foundational first)
- [ ] Only write custom code when no contrib exists
- [ ] When custom code is needed, follow the contrib patterns

## Remember

The user will say "just build it" because they have vision and urgency. You must say "let me understand what we're building on first" because you have the responsibility to build it right.

Speed comes from solid foundations, not from frantic coding.

---

*Written after the realization that we had been reinventing Evennia's wheels for days.*
