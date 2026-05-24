"""
Red Dragon MUD - Gossamer Domain Map
Generated from IOM ASCII map

Usage:
    @mapbuilder world.maps.gossamer.GOSSAMER_MAP world.maps.gossamer.GOSSAMER_LEGEND
"""

GOSSAMER_MAP = r'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~bbb?bbb?~~~bbb?b?bb?bbb?bbbbbbbbbbbbbbb~~~~bbbbbbbb~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~?fffffffbb?---------+--?fffff?fpppppppppppppppppppppbbb?~~~~~~~~~~~~
~~~~~~~~~~~~bbbffffffffffffffffffff|fffffffffffppppppppp?ppppppppppppppbbb~~~~~~~~~
~~~~~~~~~~bbfffffffffffffffffffffff=fffff?fff?RRpppppp/pppppppppppppppppppbbb~~~~~~
~~~~~~~~~bfffffff?fffffffffffffff#####fppppppppRppppp/pppppppppppppppppppppp?~~~~~~
~~~~~~~bbffffffff+--------------=#####=--+-----?RRRR?pppppppppppppppppppppppb~~~~~~
~~~~~~bfffffffff/ffffffffffffffff#####fpp|pppppRccccRpppppppppppppp?ppppppb~~~~~~~~
~~~~~~bf?ffffff/ffffffff?ffffffffff=fffpp|pppppRccccRpppppppppppppppppppppb~~~~~~~~
~~~~~~?fffffff/ffffffffffffffffffff|ffffp+-cccpRccccRppppppppppppppppppppppb~~~~~~~
~~~~~~~bfffff/fffffffffffffffffff?f|ffffffpcccpRccccRpppppppppppppp?ppppppppb~~~~~~
~~~~~~bfffff+ffffff?fffffffffffffff|fff?ffpcccp?RRRR?ppppppppppppppppppppppf?~~~~~~
~~~~~~bfffff|ffffffffffffffffffffff|fffffffppp/?ppppp\ppppppppppppppppppfffb~~~~~~~
~~~~~~bfffff|ffffffffffffffffffffff+---------+--------?pppppppppppppffffffffb~~~~~~
~~~~~bffffff|ffffffffff^^^fff^^^?fffffffffffffffpppppppppppfffppppffffffffffb~~~~~~
~~~~~bf?ffff|fffffffff^^^^^^^^^^^^^fffffffffffffffffffffffffffffppffffffffffb~~~~~~
~~~~~~bfffff#ffffffff^^^^^^^^^^^^^^^^^fffffffffffffffff?fffffffffffffff?fffb~~~~~~~
~~~~~~~bfff#?#fffffff^^^^FFF?FFFffff^^f^^fffffffffffffffffffffffffffffffffffbb~~~~~
~~~~~~~~bfff#fffffff^^FFFFFFFFFFFffff^^^ffffff?fffffffffffffffffffffffxxxxffb~~~~~~
~~~~~~bbffffffffff^^^FFFFFFFFFFFFFFffff^^ffffffffffffffffbbbbbbbbbbfxxxssxxxb?~~~~~
~~~~~~bfffffffff^^^?FFFFFFFFFb?bFFFFFFFF^^^^ffffffffffffbb~~~~~~~~~bsssssssb~~~~~~~
~~~~~~bffffffffff^^ffFFFFFFbb~~~bbbFFFFFFF^^fffffffffffb~~~~~~~~~bbsssssssssb~~~~~~
~~~~~~~~bfffffffff^^bb~~~~~~~~~~~~~~~~~~~~bbb^^ffffffffbbb~~~~~~~bss?sssxxsssb~~~~~
~~~~~~~~bf?fffffff^^bb~~~~~~~~~~~~~~~~~~~~bbb^^ffffffffbbb~~~~~~~bssssss?xsssb~~~~~
~~~~~~~~~bbfffffff?^^~~~~~~~~ff~~~~~~~~~~~~~^^^ff?fffbbb~~~~~~~~~~bsssssssssb~~~~~~
~~~~~~~~~~~bbbbbbbb~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^bbbb~~~~~~~~~~~~bssssssssbb~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bbbbbbbb~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Thieves Network
'''

from world.maps.terrain import (
    build_water, build_beach, build_forest, build_deep_forest,
    build_hills, build_mountains, build_desert, build_swamp,
    build_marsh, build_road, build_plains, build_city,
    build_building, build_lake, build_dungeon, build_crossing,
    build_valley
)

# Terrain character mapping for IOM ASCII maps
GOSSAMER_LEGEND = {
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

