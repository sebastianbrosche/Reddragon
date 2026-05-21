#!/usr/bin/env python3
"""
Red Dragon MUD — Complete Guild System
Based on Daran Madrox's Islands of Myth Guide
Full prerequisite trees, locations, abilities, and messages.
"""

class Guild:
    def __init__(self):
        self.name = ""
        self.display_name = ""
        self.description = ""
        self.category = ""
        self.tier = "alpha"  # alpha, bravo, gamma, delta
        self.prerequisites = {}
        self.stats = {}
        self.weapons = []
        self.armor = []
        self.abilities = {}
        self.location = ""  # Where to find this guild
        self.messages = {}  # Action messages

# ============================================================================
# WARRIOR TREE
# ============================================================================

class WarriorGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "warrior"
        self.display_name = "Warrior"
        self.description = "Masters of martial combat. Use 'parry #' to set defense mode (0=offensive, 100=defensive)."
        self.category = "melee"
        self.tier = "alpha"
        self.stats = {"strength": 3, "constitution": 2, "dexterity": 1, "stamina": 2}
        self.weapons = ["sword", "axe", "mace", "spear", "polearm", "dagger"]
        self.armor = ["cloth", "leather", "mail", "plate"]
        self.location = "Gossamer Island, A Shack Among Ruins"
        self.abilities = {
            "kick": {"level": 1, "type": "skill", "desc": "Hard kick to stomach"},
            "punch": {"level": 5, "type": "skill", "desc": "Punch to the temple"},
            "strike": {"level": 10, "type": "skill", "desc": "Powerful weapon strike"},
            "resist_pain": {"level": 15, "type": "skill", "desc": "Begin resisting pain"},
            "charge": {"level": 20, "type": "skill", "desc": "Rush and slam into enemy"},
        }
        self.messages = {
            "charge": ["You rush at (target) and slam your (weapon) into *, crushing * with the force of your attack.",
                      "You roar a thunderous battlecry as you violently charge (target) launching an incredibly powerful blow straight into * chest!"],
            "kick": ["You land a hard kick to (target)'s stomach, hurting *!"],
            "punch": ["You punch (target) square in the temple, rocking * badly!"],
        }

class BerserkerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "berserker"
        self.display_name = "Berserker"
        self.description = "Ferocious warriors who enter battle rage. 'ignore pain' and 'resist pain' can be used together."
        self.category = "melee"
        self.tier = "alpha"
        self.prerequisites = {"warrior": 20}
        self.location = "Blackavar Island, Blackavar City's Royal Palace"
        self.abilities = {
            "berserker_stance": {"level": 1, "type": "stance", "desc": "Enter berserker rage"},
            "cry_of_the_berserker": {"level": 11, "type": "skill", "desc": "Rage-filled attack"},
            "fevered_strength": {"level": 21, "type": "skill", "desc": "Grow stronger in battle"},
            "ignore_pain": {"level": 31, "type": "skill", "desc": "Ignore all pain"},
        }

class DefenderOfTheCrownGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "defender_of_the_crown"
        self.display_name = "Defender Of The Crown"
        self.description = "Elite defenders who protect the realm."
        self.category = "melee"
        self.tier = "alpha"
        self.prerequisites = {"warrior": 20}
        self.location = "Blackavar Island, Blackavar City's Royal Palace"
        self.abilities = {
            "cry_of_the_defender": {"level": 1, "type": "stance", "desc": "Filled with spirit of war"},
            "unbalancing_blow": {"level": 11, "type": "skill", "desc": "Shield slam to unbalance enemy"},
            "shield_master": {"level": 21, "type": "passive", "desc": "Master of shield defense"},
        }

class KnightGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "knight"
        self.display_name = "Knight"
        self.description = "Noble warriors who fight with honor."
        self.category = "melee"
        self.tier = "alpha"
        self.prerequisites = {"warrior": 20}
        self.location = "Blackavar Island, Blackavar City"
        self.abilities = {
            "singing_blade": {"level": 1, "type": "skill", "desc": "Weapon hums with power"},
            "impale": {"level": 11, "type": "skill", "desc": "Impale enemy with weapon"},
            "blade_dance": {"level": 21, "type": "skill", "desc": "Dance of blades"},
        }

class BarbarianGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "barbarian"
        self.display_name = "Barbarian"
        self.description = "Savage warriors from the wilds."
        self.category = "melee"
        self.tier = "bravo"
        self.prerequisites = {"berserker": 10, "defender_of_the_crown": 10}
        self.location = "Hyboria Island, Turanian Camp"
        self.abilities = {
            "deathblow": {"level": 1, "type": "skill", "desc": "Crushing deathblow"},
            "bladed_fury": {"level": 11, "type": "skill", "desc": "Helicopter attack"},
            "savage_roar": {"level": 21, "type": "skill", "desc": "Terrifying roar"},
        }

# ============================================================================
# MARTIAL ARTIST TREE
# ============================================================================

class MartialArtistGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "martial_artist"
        self.display_name = "Martial Artist"
        self.description = "Disciplined fighters who master body and mind. 'inner peace' adds +5% to all skills above racial max."
        self.category = "melee"
        self.tier = "alpha"
        self.stats = {"strength": 1, "dexterity": 3, "constitution": 1, "stamina": 2}
        self.weapons = ["fist", "staff", "club"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Small Dojo"
        self.abilities = {
            "martial_arts": {"level": 1, "type": "skill", "desc": "Enhanced unarmed combat"},
            "counterdodge": {"level": 5, "type": "skill", "desc": "Counter dodge attacks"},
            "focus_chi": {"level": 10, "type": "skill", "desc": "Focus chi for strength"},
            "inner_peace": {"level": 15, "type": "passive", "desc": "+5% to all skills above racial max"},
            "fists_of_elements": {"level": 20, "type": "skill", "desc": "Attune fists to elements"},
        }

class DragonfistFighterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "dragonfist_fighter"
        self.display_name = "Dragonfist Fighter"
        self.description = "Fighters who channel dragon power. 'fists of legend' makes fists random fire or cold damage."
        self.category = "melee"
        self.tier = "alpha"
        self.prerequisites = {"martial_artist": 20}
        self.location = "Blackavar Island, Blackavar Desert"
        self.abilities = {
            "dragonfist": {"level": 1, "type": "skill", "desc": "Dragon fist technique"},
            "fists_of_legend": {"level": 11, "type": "skill", "desc": "Legendary fist techniques"},
            "dragon_possession": {"level": 21, "type": "skill", "desc": "Channel dragon power (can kill)"},
            "dragon_tail_sweep": {"level": 31, "type": "skill", "desc": "Sweep enemies off feet"},
        }

class MysticWarriorsGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "mystic_warriors"
        self.display_name = "Mystic Warriors"
        self.description = "Warriors who channel mystical energy."
        self.category = "melee"
        self.tier = "alpha"
        self.prerequisites = {"martial_artist": 20}
        self.location = "Blackavar Island, Spirit Temple"
        self.abilities = {
            "fists_of_fury": {"level": 1, "type": "skill", "desc": "Furious fist attacks"},
            "defensive_maneuvers": {"level": 11, "type": "skill", "desc": "Advanced defense"},
            "flying_kick": {"level": 21, "type": "skill", "desc": "Leaping kick attack"},
            "forged_ego": {"level": 31, "type": "passive", "desc": "Iron will protection"},
        }

class CraneMasterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "crane_master"
        self.display_name = "Crane Master"
        self.description = "The elegant crane stance."
        self.category = "melee"
        self.tier = "bravo"
        self.prerequisites = {"martial_artist": 10, "dragonfist_fighter": 10}
        self.location = "Hyboria Island, Monk Temple"
        self.abilities = {
            "crane_stance": {"level": 1, "type": "stance", "desc": "Bonus to defensive maneuvers"},
            "nerve_strike": {"level": 11, "type": "skill", "desc": "Strike vulnerable spots"},
            "chi_of_yin": {"level": 21, "type": "skill", "desc": "Focus chi of Yin"},
            "split_essence": {"level": 31, "type": "skill", "desc": "Appear as two fighters"},
        }

class SnakeMasterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "snake_master"
        self.display_name = "Snake Master"
        self.description = "The venomous snake stance."
        self.category = "melee"
        self.tier = "bravo"
        self.prerequisites = {"martial_artist": 10, "dragonfist_fighter": 10}
        self.location = "Hyboria Island, Monk Temple"
        self.abilities = {
            "snake_stance": {"level": 1, "type": "stance", "desc": "Bonus to deliver criticals"},
            "viper_strike": {"level": 11, "type": "skill", "desc": "Venomous strikes"},
            "pounce_attack": {"level": 21, "type": "skill", "desc": "Spring on enemies"},
            "deliver_criticals": {"level": 31, "type": "skill", "desc": "Enhanced critical hits"},
        }

class TigerMasterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "tiger_master"
        self.display_name = "Tiger Master"
        self.description = "The fierce tiger stance. 'tiger_claw' goes either 100% physical or 100% element from 'fists_of_elements'."
        self.category = "melee"
        self.tier = "bravo"
        self.prerequisites = {"martial_artist": 10, "dragonfist_fighter": 10}
        self.location = "Hyboria Island, Monk Temple"
        self.abilities = {
            "tiger_stance": {"level": 1, "type": "stance", "desc": "Bonus to fists of fury"},
            "tiger_claw": {"level": 11, "type": "skill", "desc": "Devastating claw attacks"},
            "tiger_aggression": {"level": 21, "type": "skill", "desc": "Aggressive tiger strikes"},
            "nature_of_the_beast": {"level": 31, "type": "skill", "desc": "Channel beast power"},
        }

class ToadMasterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "toad_master"
        self.display_name = "Toad Master"
        self.description = "The resilient toad stance. 'toad_armor' gives +physical_res."
        self.category = "melee"
        self.tier = "bravo"
        self.prerequisites = {"martial_artist": 10, "dragonfist_fighter": 10}
        self.location = "Hyboria Island, Monk Temple"
        self.abilities = {
            "toad_stance": {"level": 1, "type": "stance", "desc": "Bonus to soul of the toad"},
            "toad_armor": {"level": 11, "type": "skill", "desc": "+physical resistance"},
            "toad_leg_power": {"level": 21, "type": "skill", "desc": "Enhanced leg strength"},
            "bouncing_toad": {"level": 31, "type": "skill", "desc": "Jump attacks"},
        }

class OrderOfTheCrescentMoonGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "order_of_the_crescent_moon"
        self.display_name = "Order Of The Crescent Moon"
        self.description = "The mystical order of martial arts."
        self.category = "melee"
        self.tier = "gamma"
        self.prerequisites = {"mystic_warriors": 10}
        self.location = "Blackavar Island, Spirit Temple"
        self.abilities = {
            "forged_ego": {"level": 1, "type": "passive", "desc": "Iron will protection"},
            "dragon_possession": {"level": 11, "type": "skill", "desc": "Channel dragon power (can kill)"},
            "dragon_tail_sweep": {"level": 21, "type": "skill", "desc": "Sweep enemies off feet"},
            "fists_of_elements_2": {"level": 31, "type": "skill", "desc": "Advanced elemental fists"},
        }

class DragonMasterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "dragon_master"
        self.display_name = "Dragon Master"
        self.description = "The ultimate martial arts master."
        self.category = "melee"
        self.tier = "delta"
        self.prerequisites = {"crane_master": 10, "snake_master": 10, "tiger_master": 10, "toad_master": 10}
        self.location = "Misty Island, Shao-lin Temple"
        self.abilities = {
            "dragon_master_stance": {"level": 1, "type": "stance", "desc": "Master all stances"},
            "true_dragonfist": {"level": 11, "type": "skill", "desc": "Ultimate dragon fist"},
            "chi_mastery": {"level": 21, "type": "passive", "desc": "Master of chi"},
            "dragon_soul": {"level": 31, "type": "skill", "desc": "Become one with the dragon"},
        }

# ============================================================================
# WEAVER TREE (Healers)
# ============================================================================

class WeaverGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "weaver"
        self.display_name = "Weaver"
        self.description = "Foundation of divine magic. 'attack' and 'weapon skill blunt' capped at 60% racial max until Templar levels."
        self.category = "healer"
        self.tier = "alpha"
        self.stats = {"wisdom": 3, "intelligence": 1, "constitution": 1}
        self.weapons = ["staff", "club", "mace", "flail"]
        self.armor = ["cloth", "leather", "mail"]
        self.location = "Gossamer Island, Illium City's Cathedral"
        self.abilities = {
            "cure_serious_wounds": {"level": 1, "type": "spell", "desc": "Heal moderate wounds"},
            "minor_refresh": {"level": 1, "type": "spell", "desc": "Restore small EP"},
            "holy_essence": {"level": 5, "type": "passive", "desc": "Boosts all healing spells"},
            "know_alignment": {"level": 10, "type": "spell", "desc": "See target alignment"},
            "create_food": {"level": 15, "type": "spell", "desc": "Create food"},
            "remove_scar": {"level": 20, "type": "spell", "desc": "Remove scars (failure can scar random person)"},
        }

class ConfessorGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "confessor"
        self.display_name = "Confessor"
        self.description = "Confession and redemption through prayer."
        self.category = "healer"
        self.tier = "alpha"
        self.prerequisites = {"weaver": 20}
        self.location = "Gossamer Island, Illium City's Cathedral"
        self.abilities = {
            "prayer_for_healing": {"level": 1, "type": "spell", "desc": "Heal through prayer"},
            "prayer_for_refreshment": {"level": 1, "type": "spell", "desc": "Refresh through prayer"},
            "prayer_for_mankind": {"level": 11, "type": "spell", "desc": "Heal all HP (sincerity + consecrated ground for SP/EP)"},
            "pious_words": {"level": 21, "type": "passive", "desc": "Improve reputation"},
            "goodwill": {"level": 31, "type": "passive", "desc": "Name recognition bonus"},
        }

class HealerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "healer"
        self.display_name = "Healer"
        self.description = "The healing arts mastery."
        self.category = "healer"
        self.tier = "alpha"
        self.prerequisites = {"weaver": 20}
        self.location = "Gossamer Island, A Small Hideaway"
        self.abilities = {
            "heal": {"level": 1, "type": "spell", "desc": "Powerful single-target heal (must be 100% for parties)"},
            "major_refresh": {"level": 1, "type": "spell", "desc": "Restore large EP"},
            "mastery_of_healing": {"level": 5, "type": "passive", "desc": "Significantly boosts healing"},
            "enhance_healing": {"level": 10, "type": "passive", "desc": "Further enhances healing"},
            "estimate_worth": {"level": 15, "type": "spell", "desc": "Estimate target worth"},
            "reincarnate": {"level": 20, "type": "spell", "desc": "Reincarnate target"},
        }

class MartyrGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "martyr"
        self.display_name = "Martyr"
        self.description = "Sacrifice for the benefit of others. 'martyric_presence' must be cast in party of at least 1."
        self.category = "healer"
        self.tier = "alpha"
        self.prerequisites = {"weaver": 20}
        self.location = "Gossamer Island, Illium City's Cathedral"
        self.abilities = {
            "martyric_presence": {"level": 1, "type": "spell", "desc": "Party-wide HP/SP/EP regen aura"},
            "heal_companions": {"level": 5, "type": "spell", "desc": "Heal all party members"},
            "refresh_companions": {"level": 10, "type": "spell", "desc": "Refresh all party members"},
            "holy_cause": {"level": 15, "type": "passive", "desc": "Slight SP regen increase"},
            "sacrifice_life_force": {"level": 20, "type": "spell", "desc": "Sacrifice HP for party benefit"},
        }

class AvatarGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "avatar"
        self.display_name = "Avatar"
        self.description = "The game-changer for big party healing. 'encourage_regeneration' increases regen by ~5%."
        self.category = "healer"
        self.tier = "gamma"
        self.prerequisites = {"healer": 10, "confessor": 10}
        self.location = "Hyboria Island, Monk Temple"
        self.abilities = {
            "encourage_regeneration": {"level": 1, "type": "spell", "desc": "THE spell: +5% regen, cast once lasts long"},
            "soul_of_the_avatar": {"level": 11, "type": "passive", "desc": "Boost all stats"},
            "quick_chant": {"level": 15, "type": "passive", "desc": "Reduce casting time"},
            "cleanse_soul": {"level": 21, "type": "spell", "desc": "Remove all scars in one cast"},
            "feed_companions": {"level": 25, "type": "spell", "desc": "Reset hunger for entire party (needs 2+ in party)"},
            "revive_dead": {"level": 31, "type": "spell", "desc": "Resurrect fallen party member"},
            "avatar_regeneration": {"level": 35, "type": "spell", "desc": "Personal better enreg, good alignment bonus"},
        }

class ExorcistGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "exorcist"
        self.display_name = "Exorcist"
        self.description = "Banish evil spirits."
        self.category = "healer"
        self.tier = "gamma"
        self.prerequisites = {"martyr": 10, "confessor": 10}
        self.location = "Hyboria Island, Tarantia City's Temple Of Mitra"
        self.abilities = {
            "exorcise": {"level": 1, "type": "spell", "desc": "Banish evil spirits"},
            "holy_wrath": {"level": 11, "type": "spell", "desc": "Holy energy blast"},
            "consecrate_ground": {"level": 21, "type": "spell", "desc": "Make ground holy"},
            "divine_protection": {"level": 31, "type": "spell", "desc": "Ultimate holy protection"},
        }

class ShieldsOfFaithGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "shields_of_faith"
        self.display_name = "Shields Of Faith"
        self.description = "Divine protection mastery. 'death_ritual' relocates you to cast room on death."
        self.category = "healer"
        self.tier = "gamma"
        self.prerequisites = {"martyr": 10, "confessor": 10}
        self.location = "Gossamer Island, Illium City's Cathedral"
        self.abilities = {
            "shield_of_faith": {"level": 1, "type": "spell", "desc": "Divine shield"},
            "aura_of_healing": {"level": 11, "type": "spell", "desc": "Healing aura"},
            "death_ritual": {"level": 21, "type": "spell", "desc": "Protection from death, relocates to cast room"},
            "return_to_sanctuary": {"level": 31, "type": "spell", "desc": "Return to Illium Sanctuary"},
        }

class TemplarGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "templar"
        self.display_name = "Templar"
        self.description = "Holy warrior of the church."
        self.category = "healer"
        self.tier = "gamma"
        self.prerequisites = {"confessor": 10, "healer": 10}
        self.location = "Misty Island, Paladin Camp"
        self.abilities = {
            "consecrate_weapon": {"level": 1, "type": "spell", "desc": "Holy weapon enchant"},
            "consecrate_shield": {"level": 11, "type": "spell", "desc": "Holy shield enchant"},
            "prayer_for_the_crusader": {"level": 21, "type": "spell", "desc": "Crusader blessing (requires saint alignment)"},
            "faith_of_the_crusader": {"level": 31, "type": "spell", "desc": "Ultimate crusader power"},
        }

class HighPriestGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "high_priest"
        self.display_name = "High Priest"
        self.description = "The pinnacle of divine magic."
        self.category = "healer"
        self.tier = "delta"
        self.prerequisites = {"avatar": 10, "exorcist": 10, "shields_of_faith": 10}
        self.location = "Gossamer Island, Illium City's Cathedral"
        self.abilities = {
            "chant_of_the_high_priest": {"level": 1, "type": "spell", "desc": "Powerful healing chant"},
            "hand_of_god": {"level": 11, "type": "spell", "desc": "Divine crushing blow"},
            "wrath_of_the_righteous": {"level": 21, "type": "spell", "desc": "Holy area blast"},
            "divine_intervention": {"level": 31, "type": "spell", "desc": "Ultimate divine protection"},
        }

# ============================================================================
# ELEMENTAL TREE
# ============================================================================

class ElementalGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "elemental"
        self.display_name = "Elemental"
        self.description = "Masters of the four elements. 'mind_sponge' increases INT by tiny amount (short duration)."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"intelligence": 3, "wisdom": 1, "constitution": 1}
        self.weapons = ["staff", "dagger", "wand"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "lightning_bolt": {"level": 1, "type": "spell", "desc": "Lightning attack"},
            "stone_skin": {"level": 5, "type": "spell", "desc": "Earth armor"},
            "fireball": {"level": 10, "type": "spell", "desc": "Fireball attack"},
            "ice_pick": {"level": 15, "type": "spell", "desc": "Ice weapon summon"},
            "mind_sponge": {"level": 20, "type": "spell", "desc": "Tiny INT boost (short)"},
        }

class AirMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "air_mage"
        self.display_name = "Air Mage"
        self.description = "Master of air and wind."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"elemental": 20}
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "air_shield": {"level": 1, "type": "spell", "desc": "Wind protection"},
            "tornado": {"level": 11, "type": "spell", "desc": "Tornado summon"},
            "call_for_storm": {"level": 21, "type": "spell", "desc": "Storm summon (can backlash)"},
            "body_of_air": {"level": 31, "type": "spell", "desc": "Become air"},
        }

class EarthMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "earth_mage"
        self.display_name = "Earth Mage"
        self.description = "Master of earth and stone."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"elemental": 20}
        self.location = "Blackavar Island, Underworld"
        self.abilities = {
            "earth_quake": {"level": 1, "type": "spell", "desc": "Earthquake attack"},
            "sand_storm": {"level": 11, "type": "spell", "desc": "Sand storm"},
            "magma_boulder": {"level": 21, "type": "spell", "desc": "Lava boulder attack"},
            "body_of_earth": {"level": 31, "type": "spell", "desc": "Become earth"},
        }

class FireMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "fire_mage"
        self.display_name = "Fire Mage"
        self.description = "Master of fire and flame."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"elemental": 20}
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "flame_blade": {"level": 1, "type": "spell", "desc": "Flame weapon"},
            "incinerate": {"level": 11, "type": "spell", "desc": "Incinerate target"},
            "armor_of_flame": {"level": 21, "type": "spell", "desc": "Flame armor"},
            "body_of_fire": {"level": 31, "type": "spell", "desc": "Become fire"},
        }

class WaterMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "water_mage"
        self.display_name = "Water Mage"
        self.description = "Master of water and ice."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"elemental": 20}
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "heal": {"level": 1, "type": "spell", "desc": "Water healing"},
            "blue_mist": {"level": 11, "type": "spell", "desc": "Healing mist"},
            "stun_shield": {"level": 21, "type": "spell", "desc": "Water shield"},
            "body_of_water": {"level": 31, "type": "spell", "desc": "Become water"},
        }

class LavaMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "lava_mage"
        self.display_name = "Lava Mage"
        self.description = "Master of lava and magma. 'mold_lava' creates nosave EQ with random stats."
        self.category = "caster"
        self.tier = "gamma"
        self.prerequisites = {"earth_mage": 10, "fire_mage": 10}
        self.location = "Dark Caverns Island, Red Rift"
        self.abilities = {
            "mold_lava": {"level": 1, "type": "skill", "desc": "Create lava EQ (nosave, random stats)"},
            "lava_form": {"level": 11, "type": "spell", "desc": "Become lava"},
            "eruption": {"level": 21, "type": "spell", "desc": "Volcanic eruption"},
            "magma_flow": {"level": 31, "type": "spell", "desc": "Magma flood"},
        }

class MistMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "mist_mage"
        self.display_name = "Mist Mage"
        self.description = "Master of mist and fog. 'mist_form' drops all items when cast."
        self.category = "caster"
        self.tier = "gamma"
        self.prerequisites = {"air_mage": 10, "water_mage": 10}
        self.location = "Misty Island, Foggy Valley"
        self.abilities = {
            "mist_form": {"level": 1, "type": "spell", "desc": "Become mist (drop all items)"},
            "yellow_mist": {"level": 11, "type": "spell", "desc": "Energy-sucking mist"},
            "green_mist": {"level": 21, "type": "spell", "desc": "Poisonous mist"},
            "black_mist": {"level": 31, "type": "spell", "desc": "Damaging mist (stays several rounds)"},
        }

class NetherMageGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "nether_mage"
        self.display_name = "Nether Mage"
        self.description = "Master of nether energy. If you die in nether form, energy drains into your elemental ring."
        self.category = "caster"
        self.tier = "delta"
        self.prerequisites = {"lava_mage": 10, "mist_mage": 10}
        self.location = "Dark Caverns Island, Gnome Caves"
        self.abilities = {
            "body_of_nether": {"level": 1, "type": "spell", "desc": "Nether form (energy drains to ring on death)"},
            "control_elemental_energy": {"level": 11, "type": "spell", "desc": "Control nether energy"},
            "chain_elemental_bolts": {"level": 21, "type": "spell", "desc": "Chain nether bolts"},
            "project_energy_blast": {"level": 31, "type": "spell", "desc": "Nether energy blast"},
            "summon_elemental_matter": {"level": 35, "type": "spell", "desc": "Summon elemental power"},
        }

# ============================================================================
# EVOKER TREE
# ============================================================================

class EvokerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker"
        self.display_name = "Evoker"
        self.description = "Masters of destructive magic. Spells stored in amulet are insta-cast when released."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"intelligence": 3, "wisdom": 2}
        self.weapons = ["staff", "dagger", "wand"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "magic_missile": {"level": 1, "type": "spell", "desc": "Basic magic attack"},
            "shield": {"level": 5, "type": "spell", "desc": "Magical shield"},
            "burning_hands": {"level": 10, "type": "spell", "desc": "Fire touch attack"},
            "lightning_touch": {"level": 15, "type": "spell", "desc": "Electric touch"},
            "amulet_focus": {"level": 20, "type": "passive", "desc": "Store spells in amulet for insta-cast"},
        }

class EvokerOfElementsGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_elements"
        self.display_name = "Evoker Of Elements"
        self.description = "Base elemental evocation."
        self.category = "caster"
        self.tier = "alpha"
        self.prerequisites = {"evoker": 20}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "elemental_blast": {"level": 1, "type": "spell", "desc": "Base elemental blast (4-round, for exp parties)"},
            "focus_elements": {"level": 10, "type": "passive", "desc": "Focus on element types"},
            "amulet_storage": {"level": 15, "type": "passive", "desc": "Store spell in amulet for insta-cast"},
            "estimate_efficiency": {"level": 20, "type": "skill", "desc": "Estimate spell efficiency"},
        }

class EvokerOfEtherGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_ether"
        self.display_name = "Evoker Of Ether"
        self.description = "Base ether evocation."
        self.category = "caster"
        self.tier = "alpha"
        self.prerequisites = {"evoker": 20}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "ether_blast": {"level": 1, "type": "spell", "desc": "Base ether blast (2-round, for EQ parties)"},
            "regeneration_trance": {"level": 10, "type": "spell", "desc": "Regen trance (can't move/look, breaks on combat)"},
            "mind_sponge": {"level": 15, "type": "spell", "desc": "Tiny INT boost (short duration)"},
        }

class EvokerOfAcidGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_acid"
        self.display_name = "Evoker Of Acid"
        self.description = "Acid evocation mastery. Acid stops skills."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "acid_blast": {"level": 1, "type": "spell", "desc": "Acid blast (stops skills)"},
            "corrosion": {"level": 11, "type": "spell", "desc": "Corrode armor"},
            "acid_rain": {"level": 21, "type": "spell", "desc": "Acid rain"},
            "melt": {"level": 31, "type": "spell", "desc": "Melt target"},
        }

class EvokerOfFlamesGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_flames"
        self.display_name = "Evoker Of Flames"
        self.description = "Flame evocation mastery. Fire forgets spells."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "flame_blast": {"level": 1, "type": "spell", "desc": "Flame blast (forgets spells)"},
            "fire_storm": {"level": 11, "type": "spell", "desc": "Fire storm"},
            "inferno": {"level": 21, "type": "spell", "desc": "Inferno"},
            "hellfire": {"level": 31, "type": "spell", "desc": "Hellfire"},
        }

class EvokerOfForceGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_force"
        self.display_name = "Evoker Of Force"
        self.description = "Force evocation mastery."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "force_blast": {"level": 1, "type": "spell", "desc": "Force blast"},
            "force_wave": {"level": 11, "type": "spell", "desc": "Force wave"},
            "force_field": {"level": 21, "type": "spell", "desc": "Force field"},
            "crush": {"level": 31, "type": "spell", "desc": "Crush target"},
        }

class EvokerOfIceGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_ice"
        self.display_name = "Evoker Of Ice"
        self.description = "Ice evocation mastery."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "ice_blast": {"level": 1, "type": "spell", "desc": "Ice blast"},
            "freeze": {"level": 11, "type": "spell", "desc": "Freeze target"},
            "blizzard": {"level": 21, "type": "spell", "desc": "Blizzard"},
            "absolute_zero": {"level": 31, "type": "spell", "desc": "Absolute zero"},
        }

class EvokerOfLightningGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_lightning"
        self.display_name = "Evoker Of Lightning"
        self.description = "Lightning evocation mastery. Electric stuns."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "lightning_blast": {"level": 1, "type": "spell", "desc": "Lightning blast (stuns)"},
            "thunder": {"level": 11, "type": "spell", "desc": "Thunder strike"},
            "storm": {"level": 21, "type": "spell", "desc": "Lightning storm"},
            "thunderbolt": {"level": 31, "type": "spell", "desc": "Ultimate lightning"},
        }

class EvokerOfMagicGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_magic"
        self.display_name = "Evoker Of Magic"
        self.description = "Magic evocation mastery. Magic stops spells."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "magic_blast": {"level": 1, "type": "spell", "desc": "Magic blast (stops spells)"},
            "magic_missile": {"level": 11, "type": "spell", "desc": "Magic missile"},
            "arcane_bolt": {"level": 21, "type": "spell", "desc": "Arcane bolt"},
            "arcane_storm": {"level": 31, "type": "spell", "desc": "Arcane storm"},
        }

class EvokerOfPoisonGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_poison"
        self.display_name = "Evoker Of Poison"
        self.description = "Poison evocation mastery."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "poison_blast": {"level": 1, "type": "spell", "desc": "Poison blast"},
            "venom": {"level": 11, "type": "spell", "desc": "Venom strike"},
            "toxic_cloud": {"level": 21, "type": "spell", "desc": "Toxic cloud"},
            "plague": {"level": 31, "type": "spell", "desc": "Plague"},
        }

class EvokerOfVacuumGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "evoker_of_vacuum"
        self.display_name = "Evoker Of Vacuum"
        self.description = "Vacuum evocation mastery."
        self.category = "caster"
        self.tier = "bravo"
        self.prerequisites = {"evoker_of_elements": 10, "evoker_of_ether": 10}
        self.location = "Gossamer Island, Evoker Tower"
        self.abilities = {
            "vacuum_blast": {"level": 1, "type": "spell", "desc": "Vacuum blast"},
            "suffocate": {"level": 11, "type": "spell", "desc": "Suffocate target"},
            "void": {"level": 21, "type": "spell", "desc": "Void spell"},
            "black_hole": {"level": 31, "type": "spell", "desc": "Black hole"},
        }

class SorcererGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "sorcerer"
        self.display_name = "Sorcerer"
        self.description = "The ultimate evoker. 1 level: 5 levels in any 3 bravo. 15 levels: 5 levels in all 8 bravo."
        self.category = "caster"
        self.tier = "delta"
        self.location = "Hyboria Island, Forest of Despair"
        self.abilities = {
            "sorcerer_blast": {"level": 1, "type": "spell", "desc": "Ultimate blast spell"},
            "arcane_mastery": {"level": 11, "type": "passive", "desc": "Master all arcane"},
            "elemental_fusion": {"level": 21, "type": "spell", "desc": "Fuse all elements"},
            "reality_tear": {"level": 31, "type": "spell", "desc": "Tear reality"},
        }

# ============================================================================
# UNRAVELLER TREE (Evil)
# ============================================================================

class UnravellerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "unraveller"
        self.display_name = "Unraveller"
        self.description = "Dark magic users who unravel the fabric of reality."
        self.category = "evil"
        self.tier = "alpha"
        self.stats = {"intelligence": 3, "wisdom": 2, "constitution": -1}
        self.weapons = ["dagger", "staff", "wand"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Old Red Dragon City"

class HarmerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "harmer"
        self.display_name = "Harmer"
        self.description = "Inflict pain and suffering."
        self.category = "evil"
        self.tier = "alpha"
        self.prerequisites = {"unraveller": 20}
        self.location = "Emerald Island, Hell's Pit"
        self.abilities = {
            "inflict_harm": {"level": 1, "type": "spell", "desc": "Cause harm to enemies"},
            "dark_ritual": {"level": 5, "type": "spell", "desc": "Dark healing ritual"},
            "pain": {"level": 10, "type": "spell", "desc": "Cause intense pain"},
            "suffering": {"level": 15, "type": "spell", "desc": "Prolonged suffering"},
            "torment": {"level": 20, "type": "spell", "desc": "Ultimate torment"},
        }

class MagicalTorturerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "magical_torturer"
        self.display_name = "Magical Torturer"
        self.description = "Magical methods of torture."
        self.category = "evil"
        self.tier = "alpha"
        self.prerequisites = {"unraveller": 20}
        self.location = "Blackavar Island, Stone Hedge Tower's Dungeon"
        self.abilities = {
            "magic_missile": {"level": 1, "type": "spell", "desc": "Magical torture bolts"},
            "agony": {"level": 5, "type": "spell", "desc": "Magical agony"},
            "magical_torment": {"level": 10, "type": "spell", "desc": "Advanced magical torture"},
            "mind_shatter": {"level": 15, "type": "spell", "desc": "Shatter enemy mind"},
            "soul_rend": {"level": 20, "type": "spell", "desc": "Rend enemy soul"},
        }

class SacrificerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "sacrificer"
        self.display_name = "Sacrificer"
        self.description = "Blood sacrifice for power."
        self.category = "evil"
        self.tier = "alpha"
        self.prerequisites = {"unraveller": 20}
        self.location = "Misty Island, Army Of Darkness Castle"
        self.abilities = {
            "blood_sacrifice": {"level": 1, "type": "spell", "desc": "Sacrifice blood for power"},
            "life_drain": {"level": 5, "type": "spell", "desc": "Drain life force"},
            "soul_sacrifice": {"level": 10, "type": "spell", "desc": "Sacrifice souls"},
            "dark_offering": {"level": 15, "type": "spell", "desc": "Offer to dark gods"},
            "ritual_kill": {"level": 20, "type": "spell", "desc": "Kill for power"},
        }

class ServantOfLlothGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "servant_of_lloth"
        self.display_name = "Servant Of Lloth"
        self.description = "Serve the spider queen."
        self.category = "evil"
        self.tier = "bravo"
        self.prerequisites = {"harmer": 10, "magical_torturer": 10}
        self.location = "Dark Caverns Island, Green Rift"
        self.abilities = {
            "spider_blessing": {"level": 1, "type": "spell", "desc": "Blessing of Lloth"},
            "web": {"level": 11, "type": "spell", "desc": "Entangle enemies"},
            "poison_bite": {"level": 21, "type": "spell", "desc": "Venomous strike"},
            "spider_form": {"level": 31, "type": "spell", "desc": "Transform into spider"},
        }

class ServantOfMordulakGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "servant_of_mordulak"
        self.display_name = "Servant Of Mordulak"
        self.description = "Serve the dark lord Mordulak."
        self.category = "evil"
        self.tier = "bravo"
        self.prerequisites = {"harmer": 10, "sacrificer": 10}
        self.location = "Hyboria Island, Aquilonia"
        self.abilities = {
            "dark_blessing": {"level": 1, "type": "spell", "desc": "Blessing of Mordulak"},
            "shadow_strike": {"level": 11, "type": "spell", "desc": "Strike from shadows"},
            "dark_armor": {"level": 21, "type": "spell", "desc": "Shadow armor"},
            "mordulaks_fury": {"level": 31, "type": "spell", "desc": "Dark lord's fury"},
        }

class ServantOfShirijaGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "servant_of_shirija"
        self.display_name = "Servant Of Shirija"
        self.description = "Serve the ice queen Shirija."
        self.category = "evil"
        self.tier = "bravo"
        self.prerequisites = {"magical_torturer": 10, "sacrificer": 10}
        self.location = "Hell"
        self.abilities = {
            "ice_blessing": {"level": 1, "type": "spell", "desc": "Blessing of Shirija"},
            "frost_bolt": {"level": 11, "type": "spell", "desc": "Ice bolt attack"},
            "freeze": {"level": 21, "type": "spell", "desc": "Freeze enemies"},
            "blizzard": {"level": 31, "type": "spell", "desc": "Ice storm"},
        }

class ServantOfTalakhGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "servant_of_talakh"
        self.display_name = "Servant Of Talakh"
        self.description = "Serve the fire lord Talakh."
        self.category = "evil"
        self.tier = "bravo"
        self.prerequisites = {"harmer": 10, "magical_torturer": 10}
        self.location = "Blackavar Island, Blackavar City's Royal Palace"
        self.abilities = {
            "fire_blessing": {"level": 1, "type": "spell", "desc": "Blessing of Talakh"},
            "flame_strike": {"level": 11, "type": "spell", "desc": "Fire strike"},
            "inferno": {"level": 21, "type": "spell", "desc": "Inferno attack"},
            "hellfire": {"level": 31, "type": "spell", "desc": "Hellfire blast"},
        }

class ElderOfMordulakGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "elder_of_mordulak"
        self.display_name = "Elder Of Mordulak"
        self.description = "Elder dark servant."
        self.category = "evil"
        self.tier = "gamma"
        self.prerequisites = {"servant_of_lloth": 10, "servant_of_mordulak": 10, "servant_of_shirija": 10, "servant_of_talakh": 10}
        self.location = "Hyboria Island, Aquilonia"
        self.abilities = {
            "dark_mastery": {"level": 1, "type": "spell", "desc": "Master dark arts"},
            "shadow_dominion": {"level": 11, "type": "spell", "desc": "Control shadows"},
            "dark_ritual_2": {"level": 21, "type": "spell", "desc": "Advanced dark ritual"},
            "mordulaks_power": {"level": 31, "type": "spell", "desc": "Channel Mordulak"},
        }

class PatriarchOfShirijaGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "patriarch_of_shirija"
        self.display_name = "Patriarch Of Shirija"
        self.description = "Cannot join if Elder/Primate/Sword."
        self.category = "evil"
        self.tier = "gamma"
        self.prerequisites = {"servant_of_lloth": 10, "servant_of_mordulak": 10, "servant_of_shirija": 10, "servant_of_talakh": 10}
        self.location = "Hell"

class PrimateOfLlothGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "primate_of_lloth"
        self.display_name = "Primate Of Lloth"
        self.description = "Cannot join if Elder/Patriarch/Sword."
        self.category = "evil"
        self.tier = "gamma"
        self.prerequisites = {"servant_of_lloth": 10, "servant_of_mordulak": 10, "servant_of_shirija": 10, "servant_of_talakh": 10}
        self.location = "Dark Caverns Island, Green Rift"

class SwordOfTalakhGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "sword_of_talakh"
        self.display_name = "Sword Of Talakh"
        self.description = "Cannot join if Elder/Patriarch/Primate."
        self.category = "evil"
        self.tier = "gamma"
        self.prerequisites = {"servant_of_lloth": 10, "servant_of_mordulak": 10, "servant_of_shirija": 10, "servant_of_talakh": 10}
        self.location = "Blackavar Island, Blackavar City's Royal Palace"

# ============================================================================
# BASE GUILDS (Remaining)
# ============================================================================

class NecromancerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "necromancer"
        self.display_name = "Necromancer"
        self.description = "Masters of death magic and undead creation."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"intelligence": 3, "wisdom": 2, "constitution": -1}
        self.weapons = ["staff", "dagger", "wand"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "raise_dead": {"level": 1, "type": "spell", "desc": "Create undead minions"},
            "drain_life": {"level": 5, "type": "spell", "desc": "Drain life force"},
            "bone_armor": {"level": 10, "type": "spell", "desc": "Armor of bones"},
            "death_touch": {"level": 15, "type": "spell", "desc": "Touch of death"},
            "animate_dead": {"level": 20, "type": "spell", "desc": "Animate corpses"},
        }

class AbjurerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "abjurer"
        self.display_name = "Abjurer"
        self.description = "Protectors who use wards and barriers."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"intelligence": 2, "wisdom": 3}
        self.weapons = ["staff", "dagger"]
        self.armor = ["cloth", "leather", "mail"]
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "shield": {"level": 1, "type": "spell", "desc": "Magical shield"},
            "ward": {"level": 5, "type": "spell", "desc": "Area protection ward"},
            "dispel_magic": {"level": 10, "type": "spell", "desc": "Remove magical effects"},
            "barrier": {"level": 15, "type": "spell", "desc": "Physical barrier"},
            "protection_circle": {"level": 20, "type": "spell", "desc": "Circle of protection"},
        }

class PsychicsGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "psychics"
        self.display_name = "Psychics"
        self.description = "Mentalists who use psionic powers."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"intelligence": 3, "wisdom": 2}
        self.weapons = ["staff", "dagger"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Illium City's Mage School"
        self.abilities = {
            "mind_blast": {"level": 1, "type": "spell", "desc": "Psionic attack"},
            "telepathy": {"level": 5, "type": "spell", "desc": "Mental communication"},
            "psychic_crush": {"level": 10, "type": "spell", "desc": "Crush enemy mind"},
            "mind_control": {"level": 15, "type": "spell", "desc": "Control weak minds"},
            "psionic_storm": {"level": 20, "type": "spell", "desc": "Storm of psionic energy"},
        }

class AcrobatGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "acrobat"
        self.display_name = "Acrobat"
        self.description = "Agile performers who use movement in combat."
        self.category = "melee"
        self.tier = "alpha"
        self.stats = {"dexterity": 3, "strength": 1, "stamina": 2}
        self.weapons = ["dagger", "staff", "club"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Illium City's Entertainment District"
        self.abilities = {
            "tumble": {"level": 1, "type": "skill", "desc": "Acrobatic dodge"},
            "backflip": {"level": 5, "type": "skill", "desc": "Escape combat"},
            "aerial_strike": {"level": 10, "type": "skill", "desc": "Jumping attack"},
            "balance": {"level": 15, "type": "passive", "desc": "Never knocked down"},
            "death_from_above": {"level": 20, "type": "skill", "desc": "Aerial assassination"},
        }

class LurkerGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "lurker"
        self.display_name = "Lurker"
        self.description = "Shadowy figures who strike from hiding."
        self.category = "melee"
        self.tier = "alpha"
        self.stats = {"dexterity": 3, "intelligence": 2, "strength": 1}
        self.weapons = ["dagger", "short_sword", "club"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Illium City's Underbelly"
        self.abilities = {
            "hide": {"level": 1, "type": "skill", "desc": "Hide in shadows"},
            "sneak_attack": {"level": 5, "type": "skill", "desc": "Attack from hiding"},
            "shadow_walk": {"level": 10, "type": "skill", "desc": "Move through shadows"},
            "assassinate": {"level": 15, "type": "skill", "desc": "Instant kill weak enemies"},
            "shadow_meld": {"level": 20, "type": "skill", "desc": "Become shadow"},
        }

class DruidGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "druid"
        self.display_name = "Druid"
        self.description = "Nature priests who command the wild."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"wisdom": 3, "intelligence": 1, "constitution": 1}
        self.weapons = ["staff", "club", "dagger"]
        self.armor = ["cloth", "leather"]
        self.location = "Gossamer Island, Sacred Grove"
        self.abilities = {
            "entangle": {"level": 1, "type": "spell", "desc": "Vines trap enemies"},
            "shapechange": {"level": 5, "type": "spell", "desc": "Become animal"},
            "natures_wrath": {"level": 10, "type": "spell", "desc": "Call nature's fury"},
            "regeneration": {"level": 15, "type": "spell", "desc": "Rapid healing"},
            "summon_nature": {"level": 20, "type": "spell", "desc": "Summon nature ally"},
        }

class WoodsmanGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "woodsman"
        self.display_name = "Woodsman"
        self.description = "Rangers who thrive in wilderness."
        self.category = "melee"
        self.tier = "alpha"
        self.stats = {"strength": 2, "dexterity": 2, "stamina": 2}
        self.weapons = ["axe", "bow", "dagger", "sword"]
        self.armor = ["cloth", "leather", "mail"]
        self.location = "Gossamer Island, Forest Outpost"
        self.abilities = {
            "track": {"level": 1, "type": "skill", "desc": "Follow trails"},
            "survival": {"level": 5, "type": "skill", "desc": "Wilderness survival"},
            "called_shot": {"level": 10, "type": "skill", "desc": "Precision ranged attack"},
            "animal_companion": {"level": 15, "type": "skill", "desc": "Bond with beast"},
            "forest_sense": {"level": 20, "type": "passive", "desc": "Sense forest dangers"},
        }

class ShapeshifterGuild(Guild):
    def __init__(self):
        super().__init__()
        self.name = "shapeshifter"
        self.display_name = "Shapeshifter"
        self.description = "Masters of physical transformation."
        self.category = "caster"
        self.tier = "alpha"
        self.stats = {"intelligence": 2, "wisdom": 2, "constitution": 2}
        self.weapons = ["natural"]
        self.armor = ["natural"]
        self.location = "Gossamer Island, Shapeshifter's Lair"
        self.abilities = {
            "morph": {"level": 1, "type": "spell", "desc": "Change form"},
            "beast_form": {"level": 5, "type": "spell", "desc": "Become beast"},
            "hybrid_form": {"level": 10, "type": "spell", "desc": "Mixed form"},
            "mastery_of_forms": {"level": 15, "type": "passive", "desc": "Better forms"},
            "true_form": {"level": 20, "type": "spell", "desc": "Ultimate transformation"},
        }

# ============================================================================
# GUILD REGISTRY
# ============================================================================

GUILD_LIST = [
    # Warrior tree
    WarriorGuild(), BerserkerGuild(), DefenderOfTheCrownGuild(), KnightGuild(),
    BarbarianGuild(),
    # Martial Artist tree
    MartialArtistGuild(), DragonfistFighterGuild(), MysticWarriorsGuild(),
    CraneMasterGuild(), SnakeMasterGuild(), TigerMasterGuild(), ToadMasterGuild(),
    OrderOfTheCrescentMoonGuild(), DragonMasterGuild(),
    # Weaver tree
    WeaverGuild(), ConfessorGuild(), HealerGuild(), MartyrGuild(),
    AvatarGuild(), ExorcistGuild(), ShieldsOfFaithGuild(), TemplarGuild(),
    HighPriestGuild(),
    # Elemental tree
    ElementalGuild(), AirMageGuild(), EarthMageGuild(), FireMageGuild(),
    WaterMageGuild(), LavaMageGuild(), MistMageGuild(), NetherMageGuild(),
    # Evoker tree
    EvokerGuild(), EvokerOfElementsGuild(), EvokerOfEtherGuild(),
    EvokerOfAcidGuild(), EvokerOfFlamesGuild(), EvokerOfForceGuild(),
    EvokerOfIceGuild(), EvokerOfLightningGuild(), EvokerOfMagicGuild(),
    EvokerOfPoisonGuild(), EvokerOfVacuumGuild(), SorcererGuild(),
    # Unraveller tree
    UnravellerGuild(), HarmerGuild(), MagicalTorturerGuild(), SacrificerGuild(),
    ServantOfLlothGuild(), ServantOfMordulakGuild(), ServantOfShirijaGuild(),
    ServantOfTalakhGuild(), ElderOfMordulakGuild(), PatriarchOfShirijaGuild(),
    PrimateOfLlothGuild(), SwordOfTalakhGuild(),
    # Base guilds
    NecromancerGuild(), AbjurerGuild(), PsychicsGuild(),
    AcrobatGuild(), LurkerGuild(), DruidGuild(), WoodsmanGuild(), ShapeshifterGuild(),
]

def get_guild(name):
    for g in GUILD_LIST:
        if g.name == name:
            return g
    return None

def apply_guild(character, guild_name):
    guild = get_guild(guild_name)
    if not guild:
        return False
    
    # Check prerequisites
    for req_guild, req_level in guild.prerequisites.items():
        current = character.db.guilds.get(req_guild, 0)
        if current < req_level:
            return False
    
    character.db.guilds[guild_name] = 1
    character.db.active_guild = guild_name
    return True

def get_available_guilds(character):
    """Get list of guilds the character can join."""
    available = []
    for guild in GUILD_LIST:
        if guild.name in character.db.guilds:
            continue
        # Check if prerequisites are met
        prereqs_met = True
        for req_guild, req_level in guild.prerequisites.items():
            if character.db.guilds.get(req_guild, 0) < req_level:
                prereqs_met = False
                break
        if prereqs_met:
            available.append(guild)
    return available

def get_guild_tree(guild_name):
    """Get full tree for a guild including all children."""
    guild = get_guild(guild_name)
    if not guild:
        return None
    
    tree = {"guild": guild, "children": []}
    for g in GUILD_LIST:
        if guild_name in g.prerequisites:
            tree["children"].append(get_guild_tree(g.name))
    return tree
