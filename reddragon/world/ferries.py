"""
Red Dragon MUD - Ferry Route Builder
Connects island docks with ferry routes after map generation
"""

from typeclasses.ferry import create_ferry_route, Dock
from evennia import search_object

def find_docks_by_domain(domain_prefix):
    """Find all dock rooms for a given domain."""
    docks = []
    for obj in search_object(domain_prefix):
        if isinstance(obj, Dock) or getattr(obj.db, 'is_dock', False):
            docks.append(obj)
    return docks

def setup_island_ferries():
    """
    Setup ferry routes between all islands.
    Call this after all domains are built with @mapbuilder.
    """
    from typeclasses.ferry import ISLAND_FERRY_ROUTES
    
    # Find primary dock for each island
    island_docks = {}
    
    # Search by domain prefixes
    domain_names = ["blackavar", "gossamer", "sombre", "darkcaverns", 
                    "hyboria", "southcape", "emerald", "mists", 
                    "twin_islands", "everrest", "oddworld"]
    
    for domain in domain_names:
        # Find rooms tagged as docks in this domain
        docks = [obj for obj in search_object(domain) 
                 if hasattr(obj.db, 'is_dock') and obj.db.is_dock]
        
        if docks:
            # Use the first dock as the primary
            island_docks[domain] = docks[0]
            print(f"Found dock for {domain}: {docks[0].key}")
    
    # Create ferry routes
    for from_domain, to_domain, cost, duration in ISLAND_FERRY_ROUTES:
        if from_domain in island_docks and to_domain in island_docks:
            create_ferry_route(
                island_docks[from_domain],
                island_docks[to_domain],
                cost=cost,
                duration=duration
            )
            print(f"Created ferry: {from_domain} <-> {to_domain}")

# Module-level function for easy importing
__all__ = ['setup_island_ferries', 'find_docks_by_domain']
