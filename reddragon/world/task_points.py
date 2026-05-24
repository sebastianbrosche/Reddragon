"""
Red Dragon MUD - Task Points / Wishing Pond System
Based on Islands of Myth task point data
Task points awarded by quests, spent at wishing pond east of Central Square.
"""

# =============================================================================
# TASK POINTS DATA
# =============================================================================

TASK_POINTS_DATA = {
    "awarded_by": "quests",
    "spending_location": "Wishing Pond (east of Central Square)",
    "reference_url": "http://daranmadrox.batcave.net/games/iom/guide/character/wishes.html",
}

# =============================================================================
# WISHING POND
# =============================================================================

WISHING_POND_LOCATION = {
    "area": "Illium City",
    "direction": "east of Central Square",
    "name": "Wishing Pond",
}

# =============================================================================
# WISH TYPES (from IOM reference)
# =============================================================================
# Based on the reference URL, common wish types include:

WISH_CATEGORIES = {
    "stats": [
        "Increase basic stats",
        "Increase stat regen rates",
    ],
    "resistances": [
        "Increase resistance to damage types",
    ],
    "skills_spells": [
        "Increase spell knowledge",
        "Increase skill knowledge",
    ],
    "utility": [
        "Various utility wishes",
    ],
}

# =============================================================================
# TASK POINT NOTES
# =============================================================================

TASK_POINTS_NOTES = {
    "source": "Task points are awarded by completing quests.",
    "location": "The wishing pond is located east of Central Square in Illium City.",
    "reference": "See http://daranmadrox.batcave.net/games/iom/guide/character/wishes.html for full wish list.",
}
