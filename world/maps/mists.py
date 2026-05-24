"""
Red Dragon MUD - Mists Domain Map
Generated from IOM ASCII map

Usage:
    @mapbuilder world.maps.mists.MISTS_MAP world.maps.mists.MISTS_LEGEND
"""

MISTS_MAP = r'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~bbbbbbbbbbbbbbbbbbbbb~~~~~~~~~~~~~~~~~bbbbbbbbbbbbbbbbb~~~~~~~~~~~~~~~~~
~~~~~bbb?ppfffffffffffpppffffff~~~~~~~~fffffffffffffffff?ffffbbbbbbb~~~~~~~~~~~~
~~~~~bbbbbbbffffffffffffpppffffff~~~~~fffffffffffffffff^^^fffffffbbbbbbbf~~~~~~~
~~~~~bb~~~~bbbbffffffffffffffffff?--------+ffffffffffr^^^^^fffffffffffbbb~~~~~~~
~~~~~~~~~~bbbfff~~~~~ffffffffffffffffffffff\ffffffffrfff?ffffffffffffbbb~~~~~~~~
~~~~~bbbffffff~~~~~ffffffFFFFfffffffffffffff\ffffffrffffffffffffffffbbbb~~~~~~~~
~~~~~bbbbfff~~~~fffffffFFFFFffffffffffffffff|ffrrrrfffffffffffffffbb~~~~~~~~~~~~
~~~~~~~~~~~~~~~~ffffffffffFFFfffffffRRRrrrrr=rrrfffffffffffffffffffbbb~~~~~~~~~~
~~~~~~~bbbfff?ffffffffffffffffffRRRRffffffff|fffffffffff?ffffffffffbbbb~~~~~~~~~
~~~~~~~~~~bbbffffffffLLfffffRRRRffffffffffff|fffffffffff|f?ffffffffb~~~~~~~~~~~~
~~~~~~~~~~~bbbffffffLLLLRRRRffffffffffff?fff|fffffffffff|f|fff?ff~~~~~~~~~~~~~~~
~~~~~~~~~bbbbffffffLLLLLLfffffffffffffff+---+-----------+-+-+--?~~~~~~~~~~~~~~~~
~~~~~~~~bbbfffffffffLLLLLffffffffffffff/ffffffffffffffffff|f|fffb~~~~~~~~~~~~~~~
~~~~~~bbbffffffffffffLLLLfffffffffffff/fffffffffffffffffff/f|ffffff~~~~~~~~~~~~~
~~~~~bbbfffffffffffffffffffffffffffff/ffffFFF?fffffffffff/ff?fffffff~~~~~~~~~~~~
~~~~~~bbbfffffffffff^^ffffffffffff+-+ffffffFFFFfffffffff/ffffffffffff~~~~~~~~~~~
~~~~~~~bbbffffffff^^^ffffffffffff/fffffffffFFFfffffffff/ffffffffffffffff~~~~~~~~
~~~~~bbbfffffffff^^^ffffffffffff/fffffffffffffffffffff/fffffffffffffffff~~~~~~~~
~~~~~~~ffffff?fffffffffffffffff/fffffffffffffffffffff/fffffffffffffffffff~~~~~~~
~~~~~~~~~fffffffffffffffffffff?fffffffffffff--------+ffffffff^^^fffffffff~~~~~~~
~~~~~~~~~ffffffffffffffffffffffffffffffffffffffffffff\fffffff?^^^fffffffff~~~~~~
~~~~~~~~~~~~~~~~~~ffffffffffPfffffffffffffffffffffffff\fffff^^^fffffffffff~~~~~~
~~~~~~~~~~~~~fffffffffffffppPPPffffffffffffffffffffffff\fffffff?fffffffffff~~~~~
~~~~~~~~~~ffffffffffffffffpppPPfffffffffffffffffffffffff+-----------fffffff~~~~~
~~~~~~~~fffffxx?fffffffffffpppffffffffffffffffffffffffffffffffffffffffffff~~~~~~
~~~~~~ffffffxxxxxxfffffffffffffffff?~~~~~~ffffffffffffffffffffffffffffffff~~~~~~
~~~~~~~fffffxxxxxffffffffffffffff~~~~~~~~~~~~ffffffffffffff?ffffffffffff~~~~~~~~
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
MISTS_LEGEND = {
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

