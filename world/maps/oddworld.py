"""
Red Dragon MUD - Oddworld Domain Map
Generated from IOM ASCII map

Usage:
    @mapbuilder world.maps.oddworld.ODDWORLD_MAP world.maps.oddworld.ODDWORLD_LEGEND
"""

ODDWORLD_MAP = r'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~fffffffffffffffffffffffffffffffff?fffffffffffffffffffffffffffff~~~~~~~~~~~~
~~~~~ffffffffffffffffffff-------------+---------fffffffffffffff^^^fffffff~~~~~~~
~~~~~ffffffffffffffffffffffffffffffff/fffffffffffffffffffffffff^^^^ffffff~~~~~~~
~~~~~fffffffffffffffffffffffffffffff/ffffffffffffffffffffffffff^^fffffff~~~~~~~~
~~~~~ffffffffffffffffffffffffffffff/fffffffffffffffffffffffffff?^^^fffff~~~~~~~~
~~~~~ffffffffffffff~~~~?ffffffffff/fffffffffffffffffffffffffffffffff~~~~~~~~~~~~
~~~~~ffffffffffffff~~~~~~~fffffff+-----------------+fffffffffffffffffff~~~~~~~~~
~~~~~~~ffffffffffffff~~~~~fffffff|fffffffffffffffff|ffffffffffffffffffff~~~~~~~~
~~~~~~~~fffffffffffffffffffffffff|fffffffffffffffff|fffffffffffffffff~~~~~~~~~~~
~~~~~~~~fffffffffffffffffffffffff|ffffffff?ffffffff|ffffffffffffff~~~~~~~~~~~~~~
~~~~~~~~~ffffffffffffffffffffffff|fffffffffffffffff|fffffffffffff~~~~~~~~~~~~~~~
~~~~~~~~~~fffffffffffffffffffffff|fffffffffffffffff|ffffffffffffff~~~~~~~~~~~~~~
~~~~~~~~?------------------------+---------ffffffff|fffffffffffff~~~~~~~~~~~~~~~
~~~~~~~fffffffffffffffffffffffffff\ffffffffffffffff|fffffffffffffffff~~~~~~~~~~~
~~~~~~fffffffffffffffffffffffffffff\fffffffffffffff|ffffffffffffffffff~~~~~~~~~~
~~~~~fffffffffffffffffffffffffffffff\?fffffffffffff+------------ffffffff?~~~~~~~
~~~~~ffffffffffffffffffffffffffffffff\ffff~~~~~~fffffffffffffffffffffffff~~~~~~~
~~~~~ff^ffffffffffffffffffffffffffffff\fff~~~~~~ffffffffffffffffffffffffff~~~~~~
~~~~~fff^^^ffffffffffffffffffffffffffff\fff~~~~fffffffffffffffffffffffffff~~~~~~
~~~~~fffff^^ffffffffffffff?fffffffffffff\ff~~ffffffffffffffffffffffffffffff~~~~~
~~~~~fff^^^?fffffffffffffffffffffffffffff\fff~~ffffffppppppppffffffffffffff~~~~~
~~~~~fffff^^ffffffffffffffffffffffffffffff|ffffffffffpppppddppfffffffffffff~~~~~
~~~~~fff^^^^ffffffffffffffffffffffffffffff|ffffffffffffffdd?ddpppppffffffff~~~~~
~~~~~fffff^^ffffffffffffffffffffffffffffff|ffffffffffpppppdddpfffffffffffff~~~~~
~~~~~fff^^^^^^^fffffffffffffffffffffffffff|ffffffffffffpppddppppfffffffffff~~~~~
~~~~~ffff^^^^^ffffffffffffffffff?fffffffffffffffffffffffffffffffffffffff?~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from world.maps.terrain import (
    build_water, build_beach, build_forest, build_deep_forest,
    build_hills, build_mountains, build_desert, build_swamp,
    build_marsh, build_road, build_plains, build_city,
    build_building, build_lake, build_dungeon, build_crossing,
    build_valley
)

# Terrain character mapping for IOM ASCII maps
ODDWORLD_LEGEND = {
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

