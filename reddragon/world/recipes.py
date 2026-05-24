"""
IOM Crafting Recipes

Recipe module for Evennia's crafting contrib.
IOM has "Formula" items that are blueprints for creating objects.
These recipes convert Evennia's crafting system to IOM-style formula crafting.
"""

from evennia.contrib.game_systems.crafting.crafting import CraftingRecipe

class FormulaPotionRecipe(CraftingRecipe):
    """
    Base class for IOM formula-based crafting.
    
    In IOM, you find "Formula" items that teach you recipes.
    Once learned, you can craft the item using the formula.
    """
    name = "formula_potion"
    tool_tags = ["mortar"]
    consumable_tags = ["herb", "water", "formula_potion"]
    output_prototypes = [
        {
            "key": "Healing Potion",
            "desc": "A red liquid that restores health when consumed.",
            "tags": [("potion", "crafting_material")]
        }
    ]
    success_message = "You carefully mix the ingredients following the formula and create {outputs}!"

class FormulaWeaponRecipe(CraftingRecipe):
    """Craft a weapon using a weapon formula."""
    name = "formula_weapon"
    tool_tags = ["forge", "hammer"]
    consumable_tags = ["iron_ore", "wood", "formula_weapon"]
    output_prototypes = [
        {
            "key": "Crafted Sword",
            "desc": "A serviceable blade forged by hand.",
            "tags": [("weapon", "crafting_material")]
        }
    ]

class FormulaArmorRecipe(CraftingRecipe):
    """Craft armor using an armor formula."""
    name = "formula_armor"
    tool_tags = ["anvil", "hammer"]
    consumable_tags = ["leather", "iron_ore", "formula_armor"]
    output_prototypes = [
        {
            "key": "Crafted Leather Armor",
            "desc": "Tough leather armor that offers decent protection.",
            "tags": [("armor", "crafting_material")]
        }
    ]

class SimplePotionRecipe(CraftingRecipe):
    """Simple potion without formula (basic alchemy)."""
    name = "simple_potion"
    tool_tags = ["mortar"]
    consumable_tags = ["herb", "water"]
    output_prototypes = [
        {
            "key": "Minor Healing Potion",
            "desc": "A weak healing potion.",
            "tags": [("potion", "crafting_material")]
        }
    ]

class ScrollRecipe(CraftingRecipe):
    """Craft a magical scroll."""
    name = "scroll"
    tool_tags = ["quill", "ink"]
    consumable_tags = ["blank_scroll", "magic_essence"]
    output_prototypes = [
        {
            "key": "Magic Scroll",
            "desc": "A scroll inscribed with magical runes.",
            "tags": [("scroll", "crafting_material")]
        }
    ]
