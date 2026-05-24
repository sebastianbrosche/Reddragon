"""
Red Dragon MUD - Map Builder Integration
Uses Evennia's @mapbuilder contrib to build IOM worlds from ASCII maps

Usage in-game:
    @mapbuilder world.maps.blackavar.BLACKAVAR_MAP world.maps.blackavar.BLACKAVAR_LEGEND

Each domain has its own map file with MAP and LEGEND variables.
"""

from evennia import create_object
from typeclasses import rooms, exits
from world.maps.terrain import build_room

# Import all domain maps
from world.maps import (
    blackavar, gossamer, sombre, darkcaverns, hyboria,
    southcape, emerald, mists, twin_islands, everrest, oddworld
)

DOMAIN_MAPS = {
    "blackavar": (blackavar.BLACKAVAR_MAP, blackavar.BLACKAVAR_LEGEND),
    "gossamer": (gossamer.GOSSAMER_MAP, gossamer.GOSSAMER_LEGEND),
    "sombre": (sombre.SOMBRE_MAP, sombre.SOMBRE_LEGEND),
    "darkcaverns": (darkcaverns.DARKCAVERNS_MAP, darkcaverns.DARKCAVERNS_LEGEND),
    "hyboria": (hyboria.HYBORIA_MAP, hyboria.HYBORIA_LEGEND),
    "southcape": (southcape.SOUTHCAPE_MAP, southcape.SOUTHCAPE_LEGEND),
    "emerald": (emerald.EMERALD_MAP, emerald.EMERALD_LEGEND),
    "mists": (mists.MISTS_MAP, mists.MISTS_LEGEND),
    "twin_islands": (twin_islands.TWIN_ISLANDS_MAP, twin_islands.TWIN_ISLANDS_LEGEND),
    "everrest": (everrest.EVERREST_MAP, everrest.EVERREST_LEGEND),
    "oddworld": (oddworld.ODDWORLD_MAP, oddworld.ODDWORLD_LEGEND),
}

class DomainBuilder:
    """Builds an entire IOM domain from its ASCII map."""
    
    @staticmethod
    def build_domain(caller, domain_name):
        """Build a complete domain."""
        if domain_name not in DOMAIN_MAPS:
            caller.msg(f"Unknown domain: {domain_name}")
            caller.msg(f"Available: {', '.join(DOMAIN_MAPS.keys())}")
            return
        
        game_map, legend = DOMAIN_MAPS[domain_name]
        from evennia.contrib.grid.mapbuilder.mapbuilder import build_map
        build_map(caller, game_map, legend, iterations=1, build_exits=True)
        caller.msg(f"Domain '{domain_name}' built!")
    
    @staticmethod
    def build_all(caller):
        """Build all IOM domains."""
        for domain_name in DOMAIN_MAPS:
            caller.msg(f"\n{'='*40}")
            caller.msg(f"Building {domain_name}...")
            DomainBuilder.build_domain(caller, domain_name)
        caller.msg("\n" + "="*40)
        caller.msg("All IOM domains built!")
