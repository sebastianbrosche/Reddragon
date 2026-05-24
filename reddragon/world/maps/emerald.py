"""
Red Dragon MUD - Emerald Domain Map
Generated from IOM ASCII map

Usage:
    @mapbuilder world.maps.emerald.EMERALD_MAP world.maps.emerald.EMERALD_LEGEND
"""

EMERALD_MAP = r'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~bbbbbbbb~~~bbbbbbbbbbbbbbbbbbbbbbbbbbbb~~~~bbbbbbbb~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~bfffffff~~~~~ffffffffffffffffffppppp?pppppppppppppppbbbb~~~~~~~~~~~~
~~~~~~~~~~~~bbbffffff~~~~~~~~~fffffffffffffffffppppppppppppppppppppppppbbb~~~~~~~~~
~~~~~~~~~~bbfffffff?~~~~~~~~~~~fffffff?fffffffppppppppppppppppppppppppppppbbb~~~~~~
~~~~~~~~~bffffffff/ff~~~?m~~~ffffffffffffffffffffppppppppppppppp?pppppppppppb~~~~~~
~~~~~~~bbffffffff/fffff~~~~cfffffffffffffffffffffffffpppppppppppppppppppppppb~~~~~~
~~~~~~bfffffffff/fffffffffffffffppppppppppppfffffffppppppppppppppppppppppb~~~~~~~~~
~~~~~~bffffffff/ffffffffff?fffffppppppppppppppfffpppppppppppppppppppppppb~~~~~~~~~~
~~~~~~bfffffff/fffffffffffffffffffffppppppppppppppppppppppppppppppppppppb~~~~~~~~~~
~~~~~~~bfffff/ffffffffffffffffffffffffffffppppppppppppppppppppppppppppppppb~~~~~~~~
~~~~~~bfffff+-----------------------+fffffpppppppppppppppppppppppppppppppppfb~~~~~~
~~~~~~bfff?ffffffffffffffffffffffffff\fffffppppppppFFFFFpppppppppppppppfffb~~~~~~~~
~~~~~~bfff^^^^^^^^^^fffffffffffffffFFF\FFFFFFFFFFFFFFFFFppppppppp?ppffffffb~~~~~~~~
~~~~~^^^^^^^^^^^^^^^^^^^^^fff^^^ff?ffff\f?ffffffpppppppppppfffpppffffffffb~~~~~~~~~
~~~~~^^^^f?fffff^^?^^^^^^^^^^^^^^^^fffff\fffffffffffffffffffffffppffffffffb~~~~~~~~
~~~~~~?fffffffffff|ff^^^^^^FFF?FF^^^^^fff\fffffffffffffffffffffffffffffffffb~~~~~~~
~~~~~~~\bfffff?fff|ffFFFFFFFFF|Fffff^^f^^f\fffffffffffffffffffffffffffff?fffbb~~~~~
~~~~~~~b+---------+------+----+-----?^^^?--+fffffffff?ffffffffffffffffffffffb~~~~~~
~~~~~~~~~~bbffffff?FFFF?F|FFFFFFFFFffff^^ffffffffffffffffbbbbbbbbbbfffffffffbb~~~~~
~~~~~~~~~~~~?bbbffFFFFFFF|FF?bbbFFFFFFFF^^^^ffffffffffffbb~~~~~~~~~bffsss?sb~~~~~~~
~~~~~~~~~~~~~~~bbbbbbbbbb|bbbbbbbbbbbbbbbb^^bbbbbbbbbbbbb~~~~~~~~~~~bbbbbbbbb~~~~~~
~~~~~~~~~~~~~~~~~~~~~~bbb?bbbb~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from world.maps.terrain import (
    build_water, build_beach, build_forest, build_deep_forest,
    build_hills, build_mountains, build_desert, build_swamp,
    build_marsh, build_road, build_plains, build_city,
    build_building, build_lake, build_dungeon, build_crossing,
    build_valley
)

# Terrain character mapping for IOM ASCII maps
EMERALD_LEGEND = {
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

