"""
Red Dragon MUD - Twin_Islands Domain Map
Generated from IOM ASCII map

Usage:
    @mapbuilder world.maps.twin_islands.TWIN_ISLANDS_MAP world.maps.twin_islands.TWIN_ISLANDS_LEGEND
"""

TWIN_ISLANDS_MAP = r'''
Twin Islands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~bb~~~~~~bbb?ffffrr^^~~~~~~~~~~
~~~~~~~~~~bbbbb~~bbbbfffffrfff^^^~~~~~~~~
~~~~~~~~bbff?fbbbbfffffffffrffff^^^~~~~~~
~~~~~~~bfff/ffffffffffffffrfff^^?^~~~~~~~
~~~~~~bbff+ffffffffffffff?rffff^^^^~~~~~~
~~~~~bbfff|ffffffffffffffrRrffff^^^^~~~~~
~~~~~bbfff+--+ffffffffffrRRRrffff^^^~~~~~
~~~~~~bfff|fff\fffffffffrRRrffff^?^~~~~~~
~~~~~~~bff|ffff+-------+frrffff^^^~~~~~~~
~~~~~~~~bf+fffffffffffff\ffff^^^~~~~~~~~~
~~~~~~~bf/bbbbbfffffbbbbb?~~^^~~~~~~~~~~~
~~~~~~bf+fb~~~~bbbbbbbb~~~~~~~~~~~~~~~~~~
~~~~~~~b|b~~~~~~~bbbb~~~~~~~~~~~~~~~~~~~~
~~~~~~~~?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~bbbbb~~~~~~~~
~~~~~~~~~?~~~~~~~~~~~~~~~~~bpppppb~~~~~~~
~~~~~~~~bbb~~~~~~~~~~~~~~bbbpp?ppbb~~~~~~
~~~~~~~bbpb~~~~~~~~~~~~bbbpppppppbbb~~~~~
~~~~~~~bpppb~~~~~bbbbbbbppppppppppbb~~~~~
~~~~~~bbpppb~~~bbbbbbbbpppp?pppppppb~~~~~
~~~~~~~bpppbbbbpppppppppppppppppppb~~~~~~
~~~~~~~bpppppppppppppppppppppppv^^~~~~~~~
~~~~~~~~bbpppppppppppppppppppp^^~~~~~~~~~
~~~~~~~~~~bbpppprpppppppppppppp^^~~~~~~~~
~~~~~~~~~bbpppprrrppppppppppp^^^?^~~~~~~~
~~~~~~~~bbbbpppprppppppppppff^ff^^^~~~~~~
~~~~~~~bbb?bbbppppppppppppffff^^^^~~~~~~~
~~~~~~~~~bbbb~~bbppppppppfffff^^^~~~~~~~~
~~~~~~~~~~bb~~~~bbpppppfffffffff^^~~~~~~~
~~~~~~~~~~~b~~~~~bbbbbbbffffffff^^^~~~~~~
~~~~~~~~~~~~~~~~~~~~bbb~~bbffffff^^~~~~~~
~~~~~~~~~~~~~~~~~~~~~b~~~~bbbf^^^?^~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~bbff^~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bb~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from world.maps.terrain import (
    build_water, build_beach, build_forest, build_deep_forest,
    build_hills, build_mountains, build_desert, build_swamp,
    build_marsh, build_road, build_plains, build_city,
    build_building, build_lake, build_dungeon, build_crossing,
    build_valley
)

# Terrain character mapping for IOM ASCII maps
TWIN_ISLANDS_LEGEND = {
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

