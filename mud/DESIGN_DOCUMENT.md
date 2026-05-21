# Red Dragon MUD — Complete Design Document
## Based on Islands of Myth content (placeholder data)

---

## 27 Playable Races

| Race | STR | CON | DEX | STA | INT | WIS | Special |
|------|-----|-----|-----|-----|-----|-----|---------|
| Cromagnon | +2 | +2 | +1 | +1 | -2 | -2 | Berserker Rage |
| Drow | 0 | -1 | +2 | -1 | +1 | +2 | Shadow Dance |
| Dwarf | +2 | +3 | -1 | +2 | 0 | +1 | Stoneform |
| Elf | -1 | -1 | +1 | -2 | 0 | +3 | Nature Walk |
| Ent | +3 | +4 | -3 | -1 | +1 | +3 | Ent Root |
| Faerie | -3 | -2 | +3 | -2 | +2 | +2 | Pixie Dust |
| Gargoyle | +2 | +3 | 0 | +1 | -1 | 0 | Stone Skin |
| Giant | +4 | +3 | -2 | +2 | -2 | -1 | Colossal Slam |
| Gnome | -2 | -1 | +1 | 0 | +3 | +1 | Illusion Break |
| Goblin | -2 | -1 | +2 | +1 | 0 | -1 | Sneak Attack |
| Grorrark | +2 | +2 | +1 | +1 | -2 | -1 | Savage Bite |
| Half-Elf | 0 | 0 | +1 | 0 | 0 | +1 | Adaptability |
| Hobbit | -2 | +1 | +1 | 0 | 0 | +1 | Second Breakfast |
| Human | 0 | 0 | 0 | 0 | 0 | 0 | Versatility |
| Kobold | -2 | -1 | +2 | +1 | 0 | -1 | Trap Sense |
| Leprechaun | -3 | -2 | +3 | -2 | +2 | +1 | Rainbow Step |
| Lizardman | +1 | +2 | +1 | +1 | -1 | 0 | Swamp Dweller |
| Mindflayer | -1 | -1 | 0 | -1 | +4 | +3 | Mind Blast |
| Minotaur | +3 | +2 | -1 | +2 | -2 | -1 | Bull Rush |
| Ogier | +3 | +2 | -2 | +1 | +1 | +2 | Stonewright |
| Phoenix | +1 | +1 | +2 | +1 | +2 | +2 | Rebirth |
| Snakeman | 0 | +1 | +2 | 0 | +1 | 0 | Serpent Strike |
| Thrikhren | 0 | +1 | +2 | +1 | +1 | 0 | Hive Link |
| Troll | +3 | +3 | -2 | +2 | -3 | -2 | Regeneration |
| Vampire | +2 | +2 | +2 | +2 | +1 | +1 | Blood Drain |
| Vinnipier | +1 | +1 | +1 | +2 | 0 | +1 | Tidal Surge |
| Xorn | +2 | +3 | -1 | +2 | 0 | 0 | Earth Glide |

---

## 14 Guilds with Skill Trees

### 1. Warrior
**Branches:** Knight → Blade/Shield Master | Berserker → Barbarian/Flogger | Traveler → Dancer/Thruster

### 2. Martial Artist
**Branches:** Dragonfist → Toad/Tiger Master | Mystic → Crane/Snake Master | Warriors → Order of Crescent Moon

### 3. Acrobat
**Branches:** Street Juggler → Minstrel/Gleeman | Bard → Bartender/Troubadour | Brawler → Bannerman

### 4. Abjurer
**Branches:** Protector → Master of Energy | Irrifletta → Harbinger | Navigator → Enchanter Navigators

### 5. Elemental
**Branches:** Fire Mage → Nether Mage | Earth Mage → Lava Master | Air Mage → Mist Mage | Water Mage → Enchanter

### 6. Psychics
**Branches:** Mystics → Master/Talisman | Witch → Cauldron/Oneiromancers | Telekinetics → Watchers of Magic

### 7. Evoker
**Branches:** Evoker of Elements → Flames/Ice/Lightning/Acid/Poison/Force/Vacuum/Magic | Evoker of Ether | Traveler

### 8. Necromancer
**Branches:** Necroscope → Stygian Sorcerer | Voodooist → Embalmer | Bone Mage → Scourge

### 9. Weaver
**Branches:** Healer → Avatar | Martyr → Exorcist/Templar | Confessor → Shields

### 10. Unraveller
**Branches:** Harmer → Servant of Mordulak | Sacrificer → Servant of Shirija | Magical Navigator → Servant of Lloth

### 11. Druid
**Branches:** Weather Watcher → Adept of Stones | Animal Tamer → Shaman of Soil | Herbalist → Chanter of Deep Earth

### 12. Shapeshifter
**Branches:** Bestial → Beast Lord | Savager → Animal Trainer | Seccedaneum → Dragon Lord

### 13. Woodsman
**Branches:** Sylvan Guard → Sylvan Scout | Sylvan Ward → Animal Tamer | Herbalist → Sylvan Woodlord

### 14. Lurker
**Branches:** Street Poison Brewer → Bartender/Assassin | Trickster → Traveler/Master | Brawler → Silent Hand

---

## Weapon Mastery System

### Tiers
| Level | Name | Damage | Crit | Parry | Special |
|-------|------|--------|------|-------|---------|
| 0-20 | Novice | +0% | +0% | +0% | — |
| 21-40 | Apprentice | +5% | +0% | +0% | — |
| 41-60 | Journeyman | +10% | +5% | +0% | — |
| 61-80 | Expert | +15% | +10% | +5% | — |
| 81-95 | Master | +20% | +15% | +10% | Special Move |
| 96-100 | Grandmaster | +25% | +20% | +15% | Legendary Move |

### Gaining Mastery XP
- Hit enemy: +1 XP
- Critical hit: +3 XP
- Kill enemy: +10 XP
- Guild training: +20 XP
- Racial weapon bonus: +50% XP

---

## Damage Formula

```
Damage = (Weapon_Base + Stat_Mod) × Mastery_Multiplier
         × Race_Multiplier × Guild_Multiplier
         × Critical_Multiplier × Position_Multiplier
         × Random_Variance (0.9 - 1.1)
```

### Modifiers
- **Stat Mod:** STR × 0.5 (melee) | DEX × 0.5 (ranged)
- **Mastery:** 1.0 + (mastery × 0.0025)
- **Race:** Dwarves +10% axe/hammer, Elves +15% bow, Giants +20% 2H, etc.
- **Guild:** Warriors +1%/level, Martial Artists +2%/level unarmed, Lurkers +3%/level stealth
- **Critical:** 1.5× normal | 2.0× master | 2.5× legendary
- **Position:** Front 1.0× | Flank 1.5× | Behind 2.0× | Stealth opener 1.5×

### Race Combat Bonuses
| Race | Weapon Bonus | Combat Trait |
|------|-------------|-------------|
| Dwarf | Axe/Hammer +10% | +15% physical DR |
| Elf | Bow +15% | +10% dodge |
| Giant | 2H weapons +20% | Can wield 2H in 1H |
| Minotaur | Axe/Spear +10% | Charge first attack +50% |
| Troll | — | Regen 5% HP/round in combat |
| Vampire | — | Drain 50% damage as HP (unarmed) |
| Thrikhren | Polearm +10% | Extra off-hand attack |
| Hobbit | Thrown +10% | Lucky reroll 1/day |
| Phoenix | Fire +20% | Immune to fire |

### Guild Combat Bonuses
| Guild | Combat Bonus |
|-------|-------------|
| Warrior | +1% weapon damage/level |
| Martial Artist | +2% unarmed/level, chi abilities |
| Acrobat | +1.5% dodge/level, tumble |
| Lurker | +3% stealth damage/level, poison |
| Woodsman | +2% bow/level, tracking |
| Evoker | +2% spell/level, overcharge +30% |
| Necromancer | +2% drain/level, +1 undead/5 levels |

---

## Commands

| Command | Description |
|---------|-------------|
| `race` | List all races |
| `race <name>` | View race details |
| `race select <name>` | Choose race (one-time) |
| `guild` | List all guilds |
| `guild <name>` | View guild details |
| `guild join <name>` | Join guild (one-time) |
| `score` / `sc` / `stats` | View character sheet |
| `combat` / `profile` / `mastery` | View combat profile |
| `mastery` | List weapon masteries |
| `mastery <weapon>` | View specific mastery |
| `attack <target>` / `kill` | Attack a target |
| `equip <weapon>` / `wield` | Equip weapon type |
| `rest` / `sleep` | Recover resources |
| `ability` / `special` | Use racial/guild abilities |

---

## In-Game Example

```
> race select dwarf
You have chosen the Dwarf race!

> guild join warrior
You have joined the Warrior guild!

> equip axe
You ready your axe.

> attack goblin
You attack the goblin with your axe!
You deal 12 damage. [Dwarf axe +10%, Warrior Lv1 +1%]

> mastery
Weapon Mastery
---------------------------------------------
axe              [█░░░░░░░░░░░░░░░░░░░] 3/100 Novice

> score
==================================================
Durin the Dwarf Warrior
==================================================
  Race:  Dwarf
  Guild: Warrior (Level 1)

  Attributes:
    Strength     12
    Constitution 13
    Dexterity    9
    Stamina      12
    Intelligence 10
    Wisdom       11

  Resources:
    HP: 45/50
    EP: 30/30
    SP: 10/10

  XP Rate: 98%
  Skill Cap: 95%
  Spell Cap: 85%

  Racial Traits:
    • See in the dark (infravision)
    • Resistant to poison (+25%)
    • Resistant to physical damage (+15% DR)
    • Bonus to axe and hammer weapon mastery (+10%)
==================================================
```

---

## Server
- **Web Client:** http://47.237.80.25:3000
- **Telnet:** 47.237.80.25:3001
- **Admin:** http://47.237.80.25:4001 (admin / madamsir123)
