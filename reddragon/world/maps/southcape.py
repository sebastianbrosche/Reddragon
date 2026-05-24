"""
Red Dragon MUD - Southcape Domain Map
Generated from IOM ASCII map

Usage:
    @mapbuilder world.maps.southcape.SOUTHCAPE_MAP world.maps.southcape.SOUTHCAPE_LEGEND
"""

SOUTHCAPE_MAP = r'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~ffff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~ffFFFFFff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~b~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~ffFFFFFFFFFFff^^~~~~~~~~~~~~~~~~~~~~~~~~~~~bbb~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~ffFFFFFF?FFFFFFf?^^bbb~~~~~~~~~~~~~~~~~~~~bbbpppbb~~~~~~~~~~~~~~dd~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~fFFFFFFFFFFff^^^b?~~~~~~~~~~~~~bbbbbbbbppppppppbbb~~~~~~~~~ddddddd~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~FFFFFFFff^^^hpp|bbb~~~~~~bbbbppppppppppppppppppbbb~~~~~ddddd?dddd~~~~~~~~~~~~~~~~~
~~~~~~~~~ffFFFFFFff^^hhppp|ppbbbbbbbbppppppppppppppppppppppbbbbbbbbdddddd~~~~~~~~~~~~~~~~~~~~
~~~~~~~~ffffFFFfff^^hhhppp|ppppppppppppppppppppppppppppppppppppppppppddddd~~~~~~~~~~~~~~~~~~~
~~~~~~ffffffffff^^^hhppppp|ppppppppppppppppppppppppppppppppprppppppppppffffbbb~~~~~~~~~~~~~~~
~~~~~~ffffffff^^^^^^hhpppp|pppppppppppppppppppppppppppppppprRrppppppppfff?fffb^~~~~~~~~~~~~~~
~~~~~~~fffffff?^^^?-------+------+pppppppppppppppppppppppprRRRrppppppppppfff^^^^~~~~~~~~~~~~~
~~~~~~~~fFFFFF^^^^^pppppppppppppp|pppppppppppppppppppppppprRRRrpppppppppfff^^^^^?~~~~~~~~~~~~
~~~~~~~~fFFFFFF^^^hhhpfffpppppppW|WpppppppppppppppppppppppprRrppppppprrrff^^^^^^^^~~~~~~~~~~~
~~~~~~~fffFFFFff^^hhfff?ffpppbbbW?Wbbbbbbbpppppppppppppppppprrppppprrppprrr^^^^~~~~~~~~~~~~~~
~~~~~~fffFFFFFfff^^hhfffffbbb~~~~~~~~~~~bbbppppppppppppppppppprppprppppff^^^~~~~~~^^~~~~~~~~~
~~~~~fffffffFfFFff^^hhhfbb~~~~~~~~~~~~~~~~~bbbbpppppppppppppppprrrppppffff?^^^^~~^^^^~~~~~~~~
~~~~~~fffffffFFFFFF^^^^b~~~~~~~~~~~~~~~~~~~~~~bbpppppppppppppppppppppffff^^^^^^^^^~~~~~~~~~~~
~~~~~~~~ff?^^^FFFF^vvv^^^~~~~~~~~~~~~~~~~~~~~xxxxxxpppppppppppppppppppf^^^~~~~~~^^^^~~~~~~~~~
~~~~~~~~~~^vvvvvFvvvvvvvvv~~~~~~~~~~~~~~~~~~ssssssxxxxxxpppppppppppppp^~~~~~~~~~~^^?ff~~~~~~~
~~~~~~~~~~~vvvvvvFFF?vvvvvvv~~~~~~~~~~~~~~sssssssssssssxxxxppppppppp~~~~~~~~~~~~^ffFFFff~~~~~
~~~~~~~~~~~~~~~vvvvvvvvvvv~~~~~~~~~~~~~~sssssss?sssssssssssx~~~~~~~~~~~~~~~~~~~~~ffF?Ff~~~~~~
~~~~~~~~~~~~~~~~~vvvvvvv~~~~~~~~~~~~~~~~~~~sssssssssss~~~~~~~~~~~~~~~~~~~~~~~~~~~~fFFFf~~~~~~
~~~~~~~~~~~~~~~~~~~vv~~~~~~~~~~~~~~~~~~~~~~~ssssss~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~fff~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from world.maps.terrain import (
    build_water, build_beach, build_forest, build_deep_forest,
    build_hills, build_mountains, build_desert, build_swamp,
    build_marsh, build_road, build_plains, build_city,
    build_building, build_lake, build_dungeon, build_crossing,
    build_valley
)

# Terrain character mapping for IOM ASCII maps
SOUTHCAPE_LEGEND = {
    "W": build_water,       # Ocean
    "~": build_water,       # Ocean (alternative)
    "b": build_beach,       # Beach/Coast
    "f": build_forest,      # Forest
    "F": build_deep_forest, # Deep Forest
    "h": build_hills,       # Hills
    "H": build_hills,       # Hills (alternative)
    "M": build_mountains,   # Mountains
    "d": build_desert,      # Desert
    "s": build_swamp,       # Swamp
    "S": build_swamp,       # Swamp (alternative)
    "m": build_marsh,       # Marsh
    "R": build_road,        # Road
    "p": build_plains,      # Plains/Path
    "P": build_plains,      # Plains (alternative)
    "c": build_city,        # City
    "C": build_city,        # City (alternative)
    "B": build_building,    # Building/Castle
    "L": build_lake,        # Lake
    "#": build_dungeon,     # Dungeon/Tower
    "+": build_crossing,    # Crossing/Intersection
    "|": build_road,        # Road vertical
    "-": build_road,        # Road horizontal
    "=": build_road,        # Bridge/Road special
    "\\": build_road,      # Road diagonal
    "/": build_road,        # Road diagonal
    "^": build_mountains,  # Mountain peak
    "v": build_valley,     # Valley
    "V": build_valley,     # Valley (alternative)
}

