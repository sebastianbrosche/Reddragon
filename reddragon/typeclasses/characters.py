"""
Red Dragon MUD - Character Typeclass
Based on Islands of Myth reverse-engineering
Uses Evennia's TraitHandler, BuffHandler, and RP system.
"""

from evennia import DefaultCharacter
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler
from evennia.contrib.rpg.buffs import BuffHandler
from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPCharacter
from evennia.contrib.rpg.health_bar.health_bar import display_meter

# Stat tier mapping from IOM data
STAT_TIERS = {
    "Terrible": 1, "Bad": 2, "Poor": 3, "Below Ave": 4,
    "Average": 5, "Above Ave": 6, "Good": 7, "Very Good": 8,
    "Excellent": 9
}

# IOM racial stat bases (from captured data)
RACE_STAT_BASES = {
    "Human": {"str": 50, "dex": 50, "con": 50, "sta": 50, "int": 50, "wis": 50, "cha": 50},
    "Dwarf": {"str": 65, "dex": 40, "con": 70, "sta": 60, "int": 45, "wis": 55, "cha": 40},
    "Elf": {"str": 40, "dex": 65, "con": 35, "sta": 45, "int": 60, "wis": 60, "cha": 60},
    "Orc": {"str": 70, "dex": 45, "con": 65, "sta": 60, "int": 30, "wis": 30, "cha": 25},
    "Gnome": {"str": 35, "dex": 55, "con": 40, "sta": 40, "int": 70, "wis": 60, "cha": 50},
    "Halfling": {"str": 35, "dex": 70, "con": 40, "sta": 45, "int": 50, "wis": 50, "cha": 55},
    "Half-Orc": {"str": 60, "dex": 50, "con": 60, "sta": 55, "int": 35, "wis": 35, "cha": 30},
    "Half-Elf": {"str": 45, "dex": 60, "con": 45, "sta": 50, "int": 55, "wis": 55, "cha": 60},
    "Troll": {"str": 80, "dex": 30, "con": 80, "sta": 70, "int": 20, "wis": 20, "cha": 15},
    "Kobold": {"str": 30, "dex": 60, "con": 35, "sta": 40, "int": 45, "wis": 40, "cha": 30},
}

# Level advancement data from IOM
# Formula: 51500 * 1.122^(level/2)
# Level costs 1-148+

PLAYER_LEVEL_COSTS = {
    1: {"adv_level": 0, "guild_level": 9, "sub_total": 9, "grand_total": 9},
    2: {"adv_level": 27, "guild_level": 9, "sub_total": 54, "grand_total": 63},
    3: {"adv_level": 103, "guild_level": 9, "sub_total": 206, "grand_total": 269},
    4: {"adv_level": 289, "guild_level": 9, "sub_total": 578, "grand_total": 847},
    5: {"adv_level": 645, "guild_level": 9, "sub_total": 1290, "grand_total": 2137},
    6: {"adv_level": 1232, "guild_level": 9, "sub_total": 2464, "grand_total": 4601},
    7: {"adv_level": 2118, "guild_level": 9, "sub_total": 4236, "grand_total": 8837},
    8: {"adv_level": 3373, "guild_level": 9, "sub_total": 6746, "grand_total": 15583},
    9: {"adv_level": 5071, "guild_level": 9, "sub_total": 10142, "grand_total": 25725},
    10: {"adv_level": 7285, "guild_level": 9, "sub_total": 14570, "grand_total": 40295},
    11: {"adv_level": 10094, "guild_level": 9, "sub_total": 20188, "grand_total": 60483},
    12: {"adv_level": 13578, "guild_level": 9, "sub_total": 27156, "grand_total": 87639},
    13: {"adv_level": 17816, "guild_level": 9, "sub_total": 35632, "grand_total": 123271},
    14: {"adv_level": 22892, "guild_level": 9, "sub_total": 45784, "grand_total": 169055},
    15: {"adv_level": 28890, "guild_level": 9, "sub_total": 57780, "grand_total": 226835},
    16: {"adv_level": 35896, "guild_level": 9, "sub_total": 71792, "grand_total": 298627},
    17: {"adv_level": 43995, "guild_level": 9, "sub_total": 87990, "grand_total": 386617},
    18: {"adv_level": 53276, "guild_level": 9, "sub_total": 106552, "grand_total": 493169},
    19: {"adv_level": 63828, "guild_level": 9, "sub_total": 127656, "grand_total": 620825},
    20: {"adv_level": 75741, "guild_level": 9, "sub_total": 151482, "grand_total": 772307},
    21: {"adv_level": 89106, "guild_level": 9, "sub_total": 178212, "grand_total": 950519},
    22: {"adv_level": 104015, "guild_level": 9, "sub_total": 208030, "grand_total": 1158549},
    23: {"adv_level": 120562, "guild_level": 9, "sub_total": 241124, "grand_total": 1399673},
    24: {"adv_level": 138839, "guild_level": 9, "sub_total": 277678, "grand_total": 1677351},
    25: {"adv_level": 158941, "guild_level": 9, "sub_total": 317882, "grand_total": 1995233},
    26: {"adv_level": 180964, "guild_level": 9, "sub_total": 361928, "grand_total": 2357161},
    27: {"adv_level": 205004, "guild_level": 9, "sub_total": 410008, "grand_total": 2767169},
    28: {"adv_level": 231158, "guild_level": 9, "sub_total": 462316, "grand_total": 3229485},
    29: {"adv_level": 259524, "guild_level": 9, "sub_total": 519048, "grand_total": 3748533},
    30: {"adv_level": 290199, "guild_level": 9, "sub_total": 580398, "grand_total": 4328931},
    31: {"adv_level": 323283, "guild_level": 9, "sub_total": 646566, "grand_total": 4975497},
    32: {"adv_level": 358875, "guild_level": 9, "sub_total": 717750, "grand_total": 5693247},
    33: {"adv_level": 397076, "guild_level": 9, "sub_total": 794152, "grand_total": 6487399},
    34: {"adv_level": 437985, "guild_level": 9, "sub_total": 875970, "grand_total": 7363369},
    35: {"adv_level": 481705, "guild_level": 9, "sub_total": 963410, "grand_total": 8326779},
    36: {"adv_level": 528338, "guild_level": 9, "sub_total": 1056676, "grand_total": 9383455},
    37: {"adv_level": 577985, "guild_level": 9, "sub_total": 1155970, "grand_total": 10539425},
    38: {"adv_level": 630750, "guild_level": 9, "sub_total": 1261500, "grand_total": 11800925},
    39: {"adv_level": 686736, "guild_level": 9, "sub_total": 1373472, "grand_total": 13174397},
    40: {"adv_level": 746048, "guild_level": 9, "sub_total": 1492096, "grand_total": 14666493},
    41: {"adv_level": 808789, "guild_level": 9, "sub_total": 1617578, "grand_total": 16284071},
    42: {"adv_level": 875065, "guild_level": 9, "sub_total": 1750130, "grand_total": 18034201},
    43: {"adv_level": 944981, "guild_level": 9, "sub_total": 1889962, "grand_total": 19924163},
    44: {"adv_level": 1018643, "guild_level": 9, "sub_total": 2037286, "grand_total": 21961449},
    45: {"adv_level": 1096156, "guild_level": 9, "sub_total": 2192312, "grand_total": 24153761},
    46: {"adv_level": 1177629, "guild_level": 9, "sub_total": 2355258, "grand_total": 26509019},
    47: {"adv_level": 1263168, "guild_level": 9, "sub_total": 2526336, "grand_total": 29035355},
    48: {"adv_level": 1352880, "guild_level": 9, "sub_total": 2705760, "grand_total": 31741115},
    49: {"adv_level": 1446874, "guild_level": 9, "sub_total": 2893748, "grand_total": 34634863},
    50: {"adv_level": 1545258, "guild_level": 9, "sub_total": 3090516, "grand_total": 37725379},
    51: {"adv_level": 1648140, "guild_level": 9, "sub_total": 3296280, "grand_total": 41021659},
    52: {"adv_level": 1755631, "guild_level": 9, "sub_total": 3511262, "grand_total": 44532921},
    53: {"adv_level": 1867838, "guild_level": 9, "sub_total": 3735676, "grand_total": 48268597},
    54: {"adv_level": 1984873, "guild_level": 9, "sub_total": 3969746, "grand_total": 52238343},
    55: {"adv_level": 2106844, "guild_level": 9, "sub_total": 4213688, "grand_total": 56545201},
    56: {"adv_level": 2232384, "guild_level": 9, "sub_total": 4464768, "grand_total": 60948799},
    57: {"adv_level": 2366901, "guild_level": 9, "sub_total": 4733802, "grand_total": 65742601},
    58: {"adv_level": 2507527, "guild_level": 9, "sub_total": 5015054, "grand_total": 70747855},
    59: {"adv_level": 2651799, "guild_level": 9, "sub_total": 5303598, "grand_total": 76079453},
    60: {"adv_level": 2810659, "guild_level": 9, "sub_total": 5621318, "grand_total": 81705271},
    61: {"adv_level": 2968454, "guild_level": 9, "sub_total": 5936908, "grand_total": 87643679},
    62: {"adv_level": 3132434, "guild_level": 9, "sub_total": 6264868, "grand_total": 93888547},
    63: {"adv_level": 3303857, "guild_level": 9, "sub_total": 6607714, "grand_total": 100484261},
    64: {"adv_level": 3481984, "guild_level": 9, "sub_total": 6963968, "grand_total": 107448229},
    65: {"adv_level": 3658082, "guild_level": 9, "sub_total": 7316164, "grand_total": 114764393},
    66: {"adv_level": 3843425, "guild_level": 9, "sub_total": 7686850, "grand_total": 122451243},
    67: {"adv_level": 4035288, "guild_level": 9, "sub_total": 8070576, "grand_total": 130521819},
    68: {"adv_level": 4232954, "guild_level": 9, "sub_total": 8465908, "grand_total": 138987727},
    69: {"adv_level": 4437713, "guild_level": 9, "sub_total": 8875426, "grand_total": 147863153},
    70: {"adv_level": 4650858, "guild_level": 9, "sub_total": 9301716, "grand_total": 157164869},
    71: {"adv_level": 4873690, "guild_level": 9, "sub_total": 9747380, "grand_total": 166912249},
    72: {"adv_level": 5103512, "guild_level": 9, "sub_total": 10207024, "grand_total": 177119273},
    73: {"adv_level": 5338637, "guild_level": 9, "sub_total": 10677274, "grand_total": 187796547},
    74: {"adv_level": 5581381, "guild_level": 9, "sub_total": 11162762, "grand_total": 198959309},
    75: {"adv_level": 5832067, "guild_level": 9, "sub_total": 11664134, "grand_total": 210623443},
    76: {"adv_level": 6091026, "guild_level": 9, "sub_total": 12182052, "grand_total": 222805495},
    77: {"adv_level": 6358590, "guild_level": 9, "sub_total": 12717180, "grand_total": 235522675},
    78: {"adv_level": 6635105, "guild_level": 9, "sub_total": 13270210, "grand_total": 248792885},
    79: {"adv_level": 6920913, "guild_level": 9, "sub_total": 13841826, "grand_total": 262634711},
    80: {"adv_level": 7216373, "guild_level": 9, "sub_total": 14432746, "grand_total": 277067457},
    81: {"adv_level": 7521845, "guild_level": 9, "sub_total": 15043690, "grand_total": 292111147},
    82: {"adv_level": 7837693, "guild_level": 9, "sub_total": 15675386, "grand_total": 307786533},
    83: {"adv_level": 8164295, "guild_level": 9, "sub_total": 16328590, "grand_total": 324115123},
    84: {"adv_level": 8502030, "guild_level": 9, "sub_total": 17004060, "grand_total": 341119183},
    85: {"adv_level": 8851286, "guild_level": 9, "sub_total": 17702572, "grand_total": 358821755},
    86: {"adv_level": 9212454, "guild_level": 9, "sub_total": 18424908, "grand_total": 377246663},
    87: {"adv_level": 9585943, "guild_level": 9, "sub_total": 19171886, "grand_total": 396418549},
    88: {"adv_level": 9972158, "guild_level": 9, "sub_total": 19944316, "grand_total": 416362865},
    89: {"adv_level": 10371513, "guild_level": 9, "sub_total": 20743026, "grand_total": 437105891},
    90: {"adv_level": 10780434, "guild_level": 9, "sub_total": 21560868, "grand_total": 458666759},
    91: {"adv_level": 11196353, "guild_level": 9, "sub_total": 22392706, "grand_total": 481059465},
    92: {"adv_level": 11619705, "guild_level": 9, "sub_total": 23239410, "grand_total": 504298875},
    93: {"adv_level": 12050939, "guild_level": 9, "sub_total": 24101878, "grand_total": 528400753},
    94: {"adv_level": 12490309, "guild_level": 9, "sub_total": 24980618, "grand_total": 553381371},
    95: {"adv_level": 12938077, "guild_level": 9, "sub_total": 25876154, "grand_total": 579257525},
    96: {"adv_level": 13394509, "guild_level": 9, "sub_total": 26789018, "grand_total": 606046543},
    97: {"adv_level": 13859886, "guild_level": 9, "sub_total": 27719772, "grand_total": 633766315},
    98: {"adv_level": 14334548, "guild_level": 9, "sub_total": 28669096, "grand_total": 662435311},
    99: {"adv_level": 14818832, "guild_level": 9, "sub_total": 29637664, "grand_total": 692072975},
    100: {"adv_level": 15313042, "guild_level": 9, "sub_total": 30626084, "grand_total": 722699059},
    101: {"adv_level": 15817286, "guild_level": 9, "sub_total": 31634572, "grand_total": 754333631},
    102: {"adv_level": 16331824, "guild_level": 9, "sub_total": 32663648, "grand_total": 786997279},
    103: {"adv_level": 16856952, "guild_level": 9, "sub_total": 33713904, "grand_total": 820711183},
    104: {"adv_level": 17392928, "guild_level": 9, "sub_total": 34785856, "grand_total": 855497039},
    105: {"adv_level": 17940032, "guild_level": 9, "sub_total": 35880064, "grand_total": 891377103},
    106: {"adv_level": 18498484, "guild_level": 9, "sub_total": 36996968, "grand_total": 928374071},
    107: {"adv_level": 19068648, "guild_level": 9, "sub_total": 38137296, "grand_total": 966511367},
    108: {"adv_level": 19650824, "guild_level": 9, "sub_total": 39301648, "grand_total": 1005813015},
    109: {"adv_level": 20245252, "guild_level": 9, "sub_total": 40490504, "grand_total": 1046303519},
    110: {"adv_level": 20852228, "guild_level": 9, "sub_total": 41704456, "grand_total": 1088007975},
    111: {"adv_level": 21472084, "guild_level": 9, "sub_total": 42944168, "grand_total": 1130952143},
    112: {"adv_level": 22105088, "guild_level": 9, "sub_total": 44210176, "grand_total": 1175162319},
    113: {"adv_level": 22751552, "guild_level": 9, "sub_total": 45503104, "grand_total": 1220665423},
    114: {"adv_level": 23411724, "guild_level": 9, "sub_total": 46823448, "grand_total": 1267488871},
    115: {"adv_level": 24085896, "guild_level": 9, "sub_total": 48171792, "grand_total": 1315660663},
    116: {"adv_level": 24774400, "guild_level": 9, "sub_total": 49548800, "grand_total": 1365209463},
    117: {"adv_level": 25477596, "guild_level": 9, "sub_total": 50955192, "grand_total": 1416164655},
    118: {"adv_level": 26195804, "guild_level": 9, "sub_total": 52391608, "grand_total": 1468556263},
    119: {"adv_level": 26929392, "guild_level": 9, "sub_total": 53858784, "grand_total": 1522415047},
    120: {"adv_level": 27678744, "guild_level": 9, "sub_total": 55357488, "grand_total": 1577772535},
    121: {"adv_level": 28444280, "guild_level": 9, "sub_total": 56888560, "grand_total": 1634661095},
    122: {"adv_level": 29226448, "guild_level": 9, "sub_total": 58452896, "grand_total": 1693113991},
    123: {"adv_level": 30025636, "guild_level": 9, "sub_total": 60051272, "grand_total": 1753165263},
    124: {"adv_level": 30842268, "guild_level": 9, "sub_total": 61684536, "grand_total": 1814849799},
    125: {"adv_level": 31676704, "guild_level": 9, "sub_total": 63353408, "grand_total": 1878203207},
    126: {"adv_level": 32529356, "guild_level": 9, "sub_total": 65058712, "grand_total": 1943261919},
    127: {"adv_level": 33400680, "guild_level": 9, "sub_total": 66801360, "grand_total": 2010063279},
    128: {"adv_level": 34291176, "guild_level": 9, "sub_total": 68582352, "grand_total": 2078645631},
    129: {"adv_level": 35201388, "guild_level": 9, "sub_total": 70402776, "grand_total": 2149048407},
    130: {"adv_level": 36131800, "guild_level": 9, "sub_total": 72263600, "grand_total": 2221312007},
    131: {"adv_level": 37082944, "guild_level": 9, "sub_total": 74165888, "grand_total": 2295477895},
    132: {"adv_level": 38055272, "guild_level": 9, "sub_total": 76110544, "grand_total": 2371588439},
    133: {"adv_level": 39049372, "guild_level": 9, "sub_total": 78098744, "grand_total": 2449687183},
    134: {"adv_level": 40065772, "guild_level": 9, "sub_total": 80131544, "grand_total": 2529818727},
    135: {"adv_level": 41105024, "guild_level": 9, "sub_total": 82210048, "grand_total": 2612028775},
    136: {"adv_level": 42167636, "guild_level": 9, "sub_total": 84335272, "grand_total": 2696364047},
    137: {"adv_level": 43254152, "guild_level": 9, "sub_total": 86508304, "grand_total": 2782872351},
    138: {"adv_level": 44365064, "guild_level": 9, "sub_total": 88730128, "grand_total": 2871602479},
    139: {"adv_level": 45500900, "guild_level": 9, "sub_total": 91001800, "grand_total": 2962604279},
    140: {"adv_level": 46662124, "guild_level": 9, "sub_total": 93324248, "grand_total": 3055928527},
    141: {"adv_level": 47849244, "guild_level": 9, "sub_total": 95698488, "grand_total": 3151627015},
    142: {"adv_level": 49062716, "guild_level": 9, "sub_total": 98125432, "grand_total": 3249752447},
    143: {"adv_level": 50303044, "guild_level": 9, "sub_total": 100606088, "grand_total": 3350358535},
    144: {"adv_level": 51570664, "guild_level": 9, "sub_total": 103141328, "grand_total": 3453499863},
    145: {"adv_level": 52866156, "guild_level": 9, "sub_total": 105732312, "grand_total": 3559232175},
    146: {"adv_level": 54189952, "guild_level": 9, "sub_total": 108379904, "grand_total": 3667612079},
    147: {"adv_level": 55542528, "guild_level": 9, "sub_total": 111085056, "grand_total": 3778697135},
    148: {"adv_level": 56924408, "guild_level": 9, "sub_total": 113848816, "grand_total": 3892545951},
}

def calculate_player_level_cost(level):
    """
    Calculate player level cost using IOM formula:
    51500 * 1.122^(level/2)
    Returns the advance level cost for that level.
    """
    if level < 1:
        return 0
    return int(51500 * (1.122 ** (level / 2)))

def calculate_guild_level(player_level):
    """
    Calculate guild level based on player level.
    At L1: guild_level = 9
    Scales up with player level.
    """
    base = 9
    if player_level <= 1:
        return base
    # Scale up: roughly 9 + (level * 0.5)
    return int(base + (player_level * 0.5))

def get_level_cost_data(level):
    """Get the full cost data for a player level (1-148)."""
    return PLAYER_LEVEL_COSTS.get(level, None)

class Character(ContribRPCharacter):
    """
    Custom character typeclass for Red Dragon.
    Uses Evennia's TraitHandler for stats, BuffHandler for effects,
    and RP system for sdescs, poses, and recognition.
    """

    @lazy_property
    def traits(self):
        return TraitHandler(self)

    @lazy_property
    def buffs(self):
        return BuffHandler(self)

    @lazy_property
    def cooldowns(self):
        from evennia.contrib.game_systems.cooldowns.cooldowns import CooldownHandler
        return CooldownHandler(self)

    def _setup_traits(self):
        """Initialize all IOM traits for this character."""
        race = getattr(self.db, "race", "Human")
        bases = RACE_STAT_BASES.get(race, RACE_STAT_BASES["Human"])

        # Static traits: core stats
        self.traits.add("str", "Strength", trait_type="static", base=bases["str"], mod=0)
        self.traits.add("dex", "Dexterity", trait_type="static", base=bases["dex"], mod=0)
        self.traits.add("con", "Constitution", trait_type="static", base=bases["con"], mod=0)
        self.traits.add("sta", "Stamina", trait_type="static", base=bases["sta"], mod=0)
        self.traits.add("int", "Intelligence", trait_type="static", base=bases["int"], mod=0)
        self.traits.add("wis", "Wisdom", trait_type="static", base=bases["wis"], mod=0)
        self.traits.add("cha", "Charisma", trait_type="static", base=bases["cha"], mod=0)

        # Gauge traits: HP, SP, EP
        con_bonus = self.traits.con.value // 10
        self.traits.add("hp", "Hit Points", trait_type="gauge", base=100 + con_bonus * 5, mod=0)
        self.traits.add("sp", "Spell Points", trait_type="gauge", base=100, mod=0)
        self.traits.add("ep", "Endurance Points", trait_type="gauge", base=100, mod=0)

        # Counter traits: guild skills
        self.traits.add("warrior", "Warrior Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("thief", "Thief Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("cleric", "Cleric Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("mage", "Mage Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("ranger", "Ranger Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("bard", "Bard Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("monk", "Monk Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("cavalier", "Cavalier Skill", trait_type="counter", base=0, mod=0, min=0, max=100)
        self.traits.add("necromancer", "Necromancer Skill", trait_type="counter", base=0, mod=0, min=0, max=100)

    def at_object_creation(self):
        super().at_object_creation()

        # Set up RP sdesc based on race
        race = getattr(self.db, "race", "Human")
        if hasattr(self, 'sdesc'):
            self.sdesc.add(f"a {race.lower()} adventurer")

        # Set up traits via Evennia's TraitHandler
        self._setup_traits()

        # Keep legacy db attributes for backward compat until full migration
        # These will be removed once all commands use traits
        self.db.strength = self.traits.str.value
        self.db.dexterity = self.traits.dex.value
        self.db.constitution = self.traits.con.value
        self.db.stamina = self.traits.sta.value
        self.db.intelligence = self.traits.int.value
        self.db.wisdom = self.traits.wis.value
        self.db.charisma = self.traits.cha.value
        self.db.hp = self.traits.hp.value
        self.db.hp_max = self.traits.hp.base
        self.db.sp = self.traits.sp.value
        self.db.sp_max = self.traits.sp.base
        self.db.ep = self.traits.ep.value
        self.db.ep_max = self.traits.ep.base

        # Progression
        self.db.level = 1
        self.db.experience = 0
        self.db.next_level = 1000
        self.db.guild = None
        self.db.guild_level = 0
        self.db.guild_xp = 0
        self.db.guild_next = 500

        # Exploration
        self.db.rooms_explored = set()
        self.db.exploration_pct = 0.0

        # State
        self.db.alignment = "Neutral"
        self.db.hunger = "Satisfied"
        self.db.poisoned = False
        self.db.wimpy = 0
        self.db.stealth = 0
        self.db.hiding = False
        self.db.growth = "Growing"
        self.db.task_points = 0

        # Combat
        self.db.ac = "VLow"
        self.db.kills = 0
        self.db.deaths = 0

        # Size/Physical
        self.db.height = "5'8\""
        self.db.weight = 176
        self.db.size = "Medium"
        self.db.race = "Human"

        # Economy
        self.db.gold = 100
        self.db.bank_gold = 0
        self.db.gender = "ambiguous"

        # Legacy skills dict (will migrate to traits)
        self.db.skills = {
            "attack": 20,
            "flesh of stone": 20,
            "honor of the gods": 20,
            "tanking": 20,
            "weapon skill blunt": 20,
        }

        # Regeneration stats
        self.db.hp_regen = 10
        self.db.sp_regen = 5
        self.db.ep_regen = 5

        # Mail system
        self.db.mail_count = 0
        self.db.mail_unread = 0

        # Race selection flag
        self.db.needs_race_selection = True
        self.db.race = "Human"
        self.db.race_key = "human"

        # Spawn location
        from evennia.utils import search
        start_room = search.search_object("Adventurer Guild Entrance", typeclass="typeclasses.rooms.Room")
        if start_room:
            self.home = start_room[0]
            self.location = start_room[0]

        # AI DM data
        self.db.titles = []
        self.db.chat_enabled = True
    
    def at_post_puppet(self, **kwargs):
        """
        Called just after puppeting (after account has connected).
        IOM-style greeting.
        """
        super().at_post_puppet(**kwargs)
        
        # Show version info
        from commands.utility import VERSION
        self.msg(f"|bWelcome to {VERSION['name']}|n |y(v{VERSION['version']})|n")
        
        # Initialize session statistics
        from commands.summary import init_session_stats
        init_session_stats(self)
        
        # Initialize AI DM if not already running
        from typeclasses.scripts.ai_dm import get_ai_dm
        get_ai_dm()
        
        # Show score on login
        self.msg(self.get_score_display())
        
        # Show room description
        if self.location:
            self.msg(self.location.return_appearance(self))
            
    def at_post_unpuppet(self, account=None, **kwargs):
        """Called just after un-puppeting."""
        super().at_post_unpuppet(**kwargs)
        
        
    def get_stat_modifier(self, stat_name):
        """Return stat value as modifier for calculations."""
        trait = self.traits.get(stat_name.lower(), None)
        if trait:
            return trait.value
        return getattr(self.db, stat_name, 50)
        
    def modify_stat(self, stat, delta):
        """Adjust a stat by delta, bounded 1-100."""
        trait = self.traits.get(stat.lower(), None)
        if trait:
            trait.base = max(1, min(100, trait.base + delta))
            # Sync legacy db for backward compat
            stat_map = {"str": "strength", "dex": "dexterity", "con": "constitution", 
                       "sta": "stamina", "int": "intelligence", "wis": "wisdom", "cha": "charisma",
                       "hp": "hp", "sp": "sp", "ep": "ep"}
            db_key = stat_map.get(stat.lower())
            if db_key:
                setattr(self.db, db_key, trait.value)
            return trait.value
        return getattr(self.db, stat, 50)
        
    def add_experience(self, amount):
        """Add XP and check for level up."""
        self.db.experience += amount
        if self.db.experience >= self.db.next_level:
            self.level_up()
            
    def level_up(self):
        """Handle level advancement (IOM formula) using traits."""
        self.db.level += 1
        
        # IOM stat gains per level - modify traits
        self.modify_stat("str", 2)
        self.modify_stat("dex", 2)
        self.modify_stat("con", 1)
        self.modify_stat("int", 1)
        self.modify_stat("wis", 1)
        self.modify_stat("sta", 2)
        
        # Regeneration increases
        self.db.hp_regen = getattr(self.db, 'hp_regen', 10) + 2
        self.db.sp_regen = getattr(self.db, 'sp_regen', 5) + 1
        self.db.ep_regen = getattr(self.db, 'ep_regen', 5) + 1
        
        # Increase max resources based on CON/STA via traits
        con_bonus = self.traits.con.value // 10
        sta_bonus = self.traits.sta.value // 10
        self.traits.hp.base += 20 + con_bonus * 5
        self.traits.ep.base += 15 + sta_bonus * 3
        self.traits.sp.base += 10 + (self.traits.int.value // 10) * 3
        
        # Sync legacy db attributes
        self.db.hp_max = self.traits.hp.base
        self.db.ep_max = self.traits.ep.base
        self.db.sp_max = self.traits.sp.base
        
        # Full heal on level up
        self.traits.hp.current = self.traits.hp.base
        self.traits.ep.current = self.traits.ep.base
        self.traits.sp.current = self.traits.sp.base
        self.db.hp = self.traits.hp.value
        self.db.ep = self.traits.ep.value
        self.db.sp = self.traits.sp.value
        
        # Increase next level threshold (exponential)
        self.db.next_level = int(self.db.next_level * 1.5)
        
        self.msg(f"You have advanced to level {self.db.level}!")
        
    def explore_room(self, room):
        """Mark a room as explored."""
        if room.id not in self.db.rooms_explored:
            self.db.rooms_explored.add(room.id)
            return True
        return False
        
    def get_score_display(self):
        """Return formatted score sheet (IOM-style) using traits."""
        race_name = self.db.race if hasattr(self.db, "race") else "Unknown"
        guild_name = self.db.guild if self.db.guild else "None"
        guild_lvl = self.db.guild_level
        
        total_rooms = 17750
        explored = len(self.db.rooms_explored)
        pct = (explored / total_rooms) * 100 if total_rooms > 0 else 0
        
        # Pull values from traits (fallback to db for backward compat)
        str_val = getattr(self.traits, 'str', None) and self.traits.str.value or self.db.strength
        dex_val = getattr(self.traits, 'dex', None) and self.traits.dex.value or self.db.dexterity
        con_val = getattr(self.traits, 'con', None) and self.traits.con.value or self.db.constitution
        sta_val = getattr(self.traits, 'sta', None) and self.traits.sta.value or self.db.stamina
        int_val = getattr(self.traits, 'int', None) and self.traits.int.value or self.db.intelligence
        wis_val = getattr(self.traits, 'wis', None) and self.traits.wis.value or self.db.wisdom
        cha_val = getattr(self.traits, 'cha', None) and self.traits.cha.value or self.db.charisma
        hp_cur = getattr(self.traits, 'hp', None) and self.traits.hp.value or self.db.hp
        hp_max = getattr(self.traits, 'hp', None) and self.traits.hp.base or self.db.hp_max
        sp_cur = getattr(self.traits, 'sp', None) and self.traits.sp.value or self.db.sp
        sp_max = getattr(self.traits, 'sp', None) and self.traits.sp.base or self.db.sp_max
        ep_cur = getattr(self.traits, 'ep', None) and self.traits.ep.value or self.db.ep
        ep_max = getattr(self.traits, 'ep', None) and self.traits.ep.base or self.db.ep_max
        
        return f"""
,----------------------------------------------------------------------------.
| {self.key} the {race_name}
| Level          : {self.db.level:>4}                Open Guild Levels : {guild_lvl:>4}              |
|                                                                            |
| Experience     : {self.db.experience:>14}     Explored          : {pct:>5.2f}% ({pct * 8.57:.2f}%)     |
| Next level     : {self.db.next_level:>14}     Rooms Explored    : {explored:>14}     |
| Guild Level    : {self.db.guild_level:>14}     Gold on hand      : {self.db.gold:>14}     |
| To Next Level  : {self.db.next_level - self.db.experience:>14}     Gold in bank      : {self.db.bank_gold:>14}     |
| To Guild Level : {self.db.guild_next - self.db.guild_xp if self.db.guild else 0:>14}                                            |
|----------------------------------------------------------------------------|
| Strength     : {str_val:>3} | Hit Points     : {hp_cur:>4} ({hp_max:>4}) | AC       : {self.db.ac}
| Dexterity    : {dex_val:>3} | Spell Points   : {sp_cur:>4} ({sp_max:>4}) | Size     : {self.db.size}
| Constitution : {con_val:>3} | Endurance Pts. : {ep_cur:>4} ({ep_max:>4}) | Weight   : {self.db.weight} lb
| Stamina      : {sta_val:>3} | Hunger         : {self.db.hunger}       | Stealth  : {self.db.stealth}%
| Intelligence : {int_val:>3} | Wimpy          : {self.db.wimpy}%            | Hiding   : {'Yes' if self.db.hiding else 'No'}
| Wisdom       : {wis_val:>3} | Alignment      : {self.db.alignment}       | Poisoned : {'Yes' if self.db.poisoned else 'No'}
| Charisma     : {cha_val:>3} | TaskPts. : {self.db.task_points}        
|----------------------------------------------------------------------------|
| HP  : {display_meter(hp_cur, hp_max, length=30, pre_text='HP  ')} |
| SP  : {display_meter(sp_cur, sp_max, length=30, pre_text='SP  ', fill_color=['B','C','W'])} |
| EP  : {display_meter(ep_cur, ep_max, length=30, pre_text='EP  ', fill_color=['Y','G','G'])} |
|----------------------------------------------------------------------------|
| alpha   : {guild_name} ({guild_lvl})                      | Mail          : {self.db.mail_unread}/{self.db.mail_count}           |
|                                            | Kills         : {self.db.kills}             |
`----------------------------------------------------------------------------'
hp({hp_cur}/{hp_max}) sp({sp_cur}/{sp_max}) ep({ep_cur}/{ep_max}) >"""
