#!/usr/bin/env python3
"""
Build complete Illium city in Red Dragon MUD from IOM archive data.
Run via: evennia shell < build_illium.py
"""
import os, sys

# Setup Django/Evennia
sys.path.insert(0, '/root/.openclaw/workspace/mud/madamsir_mud')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.conf.settings')
import django
django.setup()

from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from typeclasses.objects import Object
from typeclasses.characters import Character

# =============================================================================
# ROOM CREATION
# =============================================================================

# Central Square (already exists, find it)
central = search_object('Central Square of Illium', typeclass=Room)
if central:
    central = central[0]
    print(f'Found Central Square: #{central.id}')
else:
    central = create_object(Room, key='Central Square of Illium')
    central.db.desc = "The heart of Illium, Central Square. Life bustles all around you, even if no other beings but the Lorlings are present. Surrounded on all sides by the trees, you feel as though you are in the middle of an enchanted forest, or a lost world. In the exact center, Illium's Heart stands. The fountain is a monument of sorts, erected by the gods of this world. Inside the trees, you can see pools of water, part of the Gossamer River captured as homes to water beings and as wishing pools. Water surrounds the fountain, and two huge windows, created by the water flowing from the top, cover an inner haven to the fountain."
    print(f'Created Central Square: #{central.id}')

# Heart of Illium (inside fountain)
heart = search_object('Heart of Illium', typeclass=Room)
if heart:
    heart = heart[0]
    print(f'Found Heart of Illium: #{heart.id}')
else:
    heart = create_object(Room, key='Heart of Illium')
    heart.db.desc = "You stand inside the Fountain of Illium, in the very heart of the city. The white marble floor, though covered in water, is not slippery. Water rushes down the walls and splashes into a small channel at the floor base. The walls are made of gold and lined with silver. Two windows are on each side of you. They are made from the water running over the arches to the rooms. While they look like glass, you see people walking through them, just as you did to enter here. Lights glitter and glow behind them, and words and colors flow within them."
    print(f'Created Heart of Illium: #{heart.id}')

# --- STREETS FROM CENTRAL SQUARE ---

# North: Illium Street between Ethereal and Myst
street_n = create_object(Room, key='On Illium Street between Ethereal and Myst')
street_n.db.desc = "You stand before Central Square as it lies directly south. To the west you can see the pools of Gossamer through the Lorling trees at your side. And to the east, Lorlings stand in a cluster, creating a small forest in the heart of the city. Each side of the street, Lorlings sway and talk among themselves in a language lost to your ears."
print(f'Created Street N: #{street_n.id}')

# South: Illium Street between Myst and Crystal
street_s = create_object(Room, key='On Illium Street between Myst and Crystal')
street_s.db.desc = "You stand before Central Square as it lies directly north. To the east you can see the wishing pools of Gossamer through the Lorling trees at your side. And to the west, Lorlings stand in a cluster, creating a small forest in the heart of the city. Each side of the street, Lorlings sway and talk among themselves in a language lost to your ears."
print(f'Created Street S: #{street_s.id}')

# East: Myst Avenue between Illium and Gossamer
avenue_e = create_object(Room, key='On Myst Avenue between Illium and Gossamer')
avenue_e.db.desc = "Standing in the inner sanctum of Central Square, the fountain there can be seen through the trees. North and south of you lay more of the large trees, and their guardian wisps. Though through the trunks to the south, you can see the glittering of pools."
print(f'Created Avenue E: #{avenue_e.id}')

# West: Myst Avenue between Arcane and Illium
avenue_w = create_object(Room, key='On Myst Avenue between Arcane and Illium')
avenue_w.db.desc = "Standing in the inner sanctum of Central Square, the fountain there can be seen through the trees. North and south of you lay more of the large trees, and their guardian wisps. Though through the trunks to the north, you can see the glittering of pools."
print(f'Created Avenue W: #{avenue_w.id}')

# --- INTERSECTIONS (1 level deeper) ---

# Intersection of Illium and Ethereal (north of street_n)
inter_n = create_object(Room, key='Intersection of Illium and Ethereal')
inter_n.db.desc = "This intersection is the beginning of the inner sanctum of Central Square. The Lorlings that lined Illium fan out and join those that surround the town square. Inside you can hear the sound of water rushing. And directly south the fountain is coming into view."
print(f'Created Intersection N: #{inter_n.id}')

# Intersection of Gossamer and Myst (east of avenue_e)
inter_e = create_object(Room, key='Intersection of Gossamer and Myst')
inter_e.db.desc = "This little intersection is the beginning of the inner sanctum of Central Square. North of you, many Lorlings sit; clustered as if they were a flock of preternatural beings. West is Central Square! You can see part of the monument through the overhangs of the trees. Southwest, more trees stand, but through them, you see a sort of glimmering, like pools. And to the northeast, a large building sits."
print(f'Created Intersection E: #{inter_e.id}')

# Wishing Pools (south of inter_e)
wishing = create_object(Room, key='Wishing Pools')
wishing.db.desc = "The Wishing Pools of Gossamer. Crystal clear water fills natural basins carved into the stone. Small water beings dart beneath the surface, their iridescent forms leaving trails of light. The pools are said to grant wishes to those who offer something precious. Lorling trees surround the pools, their roots drinking from the captured river."
print(f'Created Wishing Pools: #{wishing.id}')

# Intersection of Myst and Enchant (east of inter_e)
inter_enchant = create_object(Room, key='Intersection of Myst and Enchant')
inter_enchant.db.desc = "Where Myst Avenue meets the Enchanted Quarter. The air here shimmers with residual magic. Crystal lanterns hang from Lorling branches, casting prismatic light across the cobblestones. The buildings here are taller, their facades etched with arcane symbols."
print(f'Created Intersection Myst/Enchant: #{inter_enchant.id}')

# On Gossamer Street (north of inter_e)
gossamer_st = create_object(Room, key='On Gossamer Street')
gossamer_st.db.desc = "Gossamer Street stretches between Ethereal and Cloud. The street is lined with silvery Lorling trees that seem to shimmer in any light. Their bark is smooth as silk and their leaves rustle with a sound like whispered secrets. Pools of captured Gossamer River water reflect the sky between the roots."
print(f'Created Gossamer Street: #{gossamer_st.id}')

# Intersection of Illium and Cloud (north of inter_n)
inter_cloud = create_object(Room, key='Intersection of Illium and Cloud')
inter_cloud.db.desc = "Where Illium Street meets the Cloud District. The air is fresher here, cooler. High above, wisps of cloud drift between the Lorling canopy, as if the sky itself has descended to walk among the trees."
print(f'Created Intersection Illium/Cloud: #{inter_cloud.id}')

# On Ethereal Lane (east of inter_n)
ethereal_e = create_object(Room, key='On Ethereal Lane between Illium and Cloud')
ethereal_e.db.desc = "Ethereal Lane runs eastward from the Illium intersection. The path here seems less solid, as if it exists partially in another realm. Ghostly lights float between the trees, and the shadows move differently than they should."
print(f'Created Ethereal Lane E: #{ethereal_e.id}')

# On Ethereal Lane (west of inter_n)
ethereal_w = create_object(Room, key='On Ethereal Lane between Arcane and Illium')
ethereal_w.db.desc = "Ethereal Lane runs westward toward the Arcane Quarter. The trees here grow thicker, their trunks twisted with age. Ancient runes glow faintly on some of the larger Lorlings, as if the trees themselves remember old magics."
print(f'Created Ethereal Lane W: #{ethereal_w.id}')

# =============================================================================
# EXITS
# =============================================================================

def make_exit(key, src, dst, aliases=None):
    ex = create_object(Exit, key=key, location=src, destination=dst)
    if aliases:
        for a in aliases:
            ex.aliases.add(a)
    return ex

# Central Square connections
make_exit('north', central, street_n)
make_exit('south', central, street_s)
make_exit('east', central, avenue_e)
make_exit('west', central, avenue_w)
make_exit('fountain', central, heart, ['enter fountain', 'enter'])

# Street N connections
make_exit('south', street_n, central)
make_exit('north', street_n, inter_n)

# Street S connections
make_exit('north', street_s, central)
# Street S loops back to Central Square going south (no new room)

# Avenue E connections
make_exit('west', avenue_e, central)
make_exit('east', avenue_e, inter_e)

# Avenue W connections
make_exit('east', avenue_w, central)
# Avenue W loops back to Central Square going west

# Heart of Illium
make_exit('out', heart, central)

# Intersection N (Illium & Ethereal)
make_exit('south', inter_n, street_n)
make_exit('north', inter_n, inter_cloud)
make_exit('east', inter_n, ethereal_e)
make_exit('west', inter_n, ethereal_w)

# Intersection E (Gossamer & Myst)
make_exit('west', inter_e, avenue_e)
make_exit('south', inter_e, wishing)
make_exit('north', inter_e, gossamer_st)
make_exit('east', inter_e, inter_enchant)

# Return paths
make_exit('south', inter_cloud, inter_n)
make_exit('west', ethereal_e, inter_n)
make_exit('east', ethereal_w, inter_n)
make_exit('north', wishing, inter_e)
make_exit('south', gossamer_st, inter_e)
make_exit('west', inter_enchant, inter_e)

print('Created all exits')

# =============================================================================
# OBJECTS
# =============================================================================

# --- Central Square objects ---
# Clear old objects first to avoid duplicates
for obj in central.contents:
    if obj.key in ['large fountain', 'Lockdown Machine', 'Birthday Machine', 
                   'floating moonflower vine', 'minor mana potion', 
                   'minor intelligence potion', 'lesser strength potion',
                   'minor strength potion', 'minor wisdom potion',
                   'minor dexterity potion', 'pyroclast', 'lesser mana potion']:
        obj.delete()

fountain = create_object(Object, key='large fountain', location=central)
fountain.db.desc = "A monument erected by the gods of this world. Water cascades from the top, creating two huge windows that cover an inner haven. The fountain of Illium's Heart."

lockdown = create_object(Object, key='Lockdown Machine', location=central)
lockdown.db.desc = "A strange mechanical device humming with barely contained energy. Its purpose is unknown."

birthday = create_object(Object, key='Birthday Machine', location=central)
birthday.db.desc = "A whimsical contraption that seems to celebrate something. Gears turn and small bells chime softly."

vine_central = create_object(Object, key='floating moonflower vine', location=central)
vine_central.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# Potions in Central Square
for i in range(3):
    p = create_object(Object, key='minor mana potion', location=central)
    p.db.desc = "A small vial containing a shimmering blue liquid that restores magical energy."

for i in range(2):
    p = create_object(Object, key='minor intelligence potion', location=central)
    p.db.desc = "A small vial containing a golden liquid that sharpens the mind."

p = create_object(Object, key='lesser strength potion', location=central)
p.db.desc = "A vial of crimson liquid that temporarily boosts physical strength."

p = create_object(Object, key='minor strength potion', location=central)
p.db.desc = "A small vial of reddish liquid that provides a slight boost to strength."

p = create_object(Object, key='minor wisdom potion', location=central)
p.db.desc = "A small vial of silver liquid that grants clarity of thought."

p = create_object(Object, key='minor dexterity potion', location=central)
p.db.desc = "A small vial of green liquid that enhances agility and reflexes."

for i in range(2):
    p = create_object(Object, key='pyroclast', location=central)
    p.db.desc = "A jagged volcanic stone that burns with inner heat. These are used as weapons or crafting materials."

p = create_object(Object, key='lesser mana potion', location=central)
p.db.desc = "A vial of pale blue liquid that restores a moderate amount of magical energy."

# --- Heart of Illium objects ---
for obj in heart.contents:
    if obj.key == 'blue tome':
        obj.delete()

blue_tome = create_object(Object, key='blue tome', location=heart)
blue_tome.db.desc = "A mysterious tome sitting on a marble pedestal. Its pages seem to shimmer with arcane knowledge. The cover is bound in deep blue leather with silver clasps."

# --- Street N objects ---
vine_n = create_object(Object, key='floating moonflower vine', location=street_n)
vine_n.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# --- Street S objects ---
vine_s = create_object(Object, key='floating moonflower vine', location=street_s)
vine_s.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# --- Avenue E objects ---
vine_ee = create_object(Object, key='floating moonflower vine', location=avenue_e)
vine_ee.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# --- Avenue W objects ---
vine_ew = create_object(Object, key='floating moonflower vine', location=avenue_w)
vine_ew.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# --- Intersection N objects ---
vine_in = create_object(Object, key='floating moonflower vine', location=inter_n)
vine_in.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# --- Intersection E objects ---
vine_ie = create_object(Object, key='floating moonflower vine', location=inter_e)
vine_ie.db.desc = "A delicate vine that floats in the air, its moonflower blossoms glowing softly with an inner light."

# --- Wishing Pools objects ---
for i in range(3):
    p = create_object(Object, key='wishing stone', location=wishing)
    p.db.desc = "A smooth stone worn by centuries of wishing hands. Holding it while whispering a desire is said to make it come true."

# Water being (NPC-like object)
water_being = create_object(Object, key='water being', location=wishing)
water_being.db.desc = "A small iridescent creature that darts through the pool water. It seems aware of you, watching with intelligent eyes."

print('Created all objects')

# =============================================================================
# NPCs
# =============================================================================

# Blue the Faerie (in Central Square)
blue = search_object('Blue', typeclass=Character)
if blue:
    blue = blue[0]
    if blue.location != central:
        blue.move_to(central, quiet=True)
    print(f'Found Blue: #{blue.id}')
else:
    blue = create_object(Character, key='Blue')
    blue.db.desc = "Blue is a Faerie, floating gently above the ground. Her wings shimmer with a faint luminescence, and her eyes sparkle with mischief."
    blue.db.race = 'Faerie'
    blue.move_to(central, quiet=True)
    print(f'Created Blue: #{blue.id}')

# Gab the Pawn Broker
# From IOM login: "Gab, the Pawn Broker [sales]: I have a Scaled Armshield for sale for 120,000 gold."
gab = search_object('Gab', typeclass=Character)
if gab:
    gab = gab[0]
else:
    gab = create_object(Character, key='Gab')
    gab.db.desc = "Gab the Pawn Broker. A shrewd-looking merchant with a gleam in his eye. He buys and sells equipment for adventurers."
    gab.db.race = 'Human'
    gab.move_to(central, quiet=True)
    print(f'Created Gab: #{gab.id}')

# Lorling NPCs (scattered throughout)
lore = ["Lorling trees sway and talk among themselves in a language lost to your ears."]
for room in [street_n, street_s, avenue_e, avenue_w, inter_n, inter_e]:
    lorling = create_object(Character, key='a Lorling')
    lorling.db.desc = "A tree-like being that sways gently. Its bark-like skin creaks as it moves, and its branches gesture as if in conversation. It seems to speak in a language you cannot understand."
    lorling.db.race = 'Lorling'
    lorling.move_to(room, quiet=True)

# Wisp NPCs
wisp = create_object(Character, key='a guardian wisp')
wisp.db.desc = "A small ball of glowing light that floats and buzzes playfully. It darts between the trees, leaving trails of soft luminescence."
wisp.db.race = 'Wisp'
wisp.move_to(avenue_e, quiet=True)

wisp2 = create_object(Character, key='a guardian wisp')
wisp2.db.desc = "A small ball of glowing light that floats and buzzes playfully. It darts between the trees, leaving trails of soft luminescence."
wisp2.db.race = 'Wisp'
wisp2.move_to(avenue_w, quiet=True)

print('Created all NPCs')

# =============================================================================
# SUMMARY
# =============================================================================
print()
print('=' * 60)
print('ILLIUM CITY — FULLY BUILT IN RED DRAGON')
print('=' * 60)
rooms = [
    ('Central Square', central),
    ('Heart of Illium', heart),
    ('Illium St (Ethereal-Myst)', street_n),
    ('Illium St (Myst-Crystal)', street_s),
    ('Myst Ave (Illium-Gossamer)', avenue_e),
    ('Myst Ave (Arcane-Illium)', avenue_w),
    ('Illium & Ethereal', inter_n),
    ('Gossamer & Myst', inter_e),
    ('Wishing Pools', wishing),
    ('Myst & Enchant', inter_enchant),
    ('Gossamer Street', gossamer_st),
    ('Illium & Cloud', inter_cloud),
    ('Ethereal Lane (E)', ethereal_e),
    ('Ethereal Lane (W)', ethereal_w),
]
for name, room in rooms:
    print(f'  #{room.id:<5} {name}')
print()
print('Exits: All cardinal directions + fountain/enter')
print('NPCs: Blue (Faerie), Gab (Pawn Broker), Lorlings, Wisps')
print('Objects: Fountain, Lockdown Machine, Birthday Machine,')
print('        moonflower vines, potions, pyroclasts, blue tome,')
print('        wishing stones, water beings')
print('=' * 60)
