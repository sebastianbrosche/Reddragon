"""
Red Dragon MUD - Shapeshifter Commands
All shapeshifter guild abilities and commands
"""

from evennia import Command

class CmdShapeShift(Command):
    """
    Transform into an animal or dragon form.
    
    Usage:
        shape_shift <form>
        shapeshift wolf
        shapeshift dragon
    """
    key = "shape_shift"
    aliases = ["shapeshift", "shift"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            # Show available forms
            current = getattr(caller.db, 'current_form', None)
            unlocked = getattr(caller.db, 'unlocked_forms', [])
            
            output = []
            output.append("-=-=-| Shapeshifter Forms |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            if current:
                output.append(f"Current form: {current}")
            output.append(f"Unlocked forms: {', '.join(unlocked) if unlocked else 'None'}")
            output.append("Available forms: dog, wolf, cat, leopard, tiger, falcon, vulture, owl, eagle,")
            output.append("  black bear, grizzly bear, polar bear, white dragon, green dragon,")
            output.append("  blue dragon, black dragon, red dragon")
            output.append("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            caller.msg("\n".join(output))
            return
        
        form = self.args.strip().lower()
        
        # Check if in shapeshifter guild
        guild = getattr(caller.db, 'guild', '').lower()
        if 'shapeshifter' not in guild and guild not in ['animal tamer', 'bestial seccedaneum', 'savager',
                                                          'animal healer', 'animal trainer', 'beast lord',
                                                          'dragon lord']:
            caller.msg("You must be in the shapeshifter guild to use this ability.")
            return
        
        # Check if form is unlocked
        unlocked = getattr(caller.db, 'unlocked_forms', [])
        if form not in unlocked:
            caller.msg(f"You have not unlocked the {form} form yet. Complete the quest to unlock it.")
            return
        
        # Check if already in that form
        current = getattr(caller.db, 'current_form', None)
        if current == form:
            caller.msg(f"You are already in {form} form.")
            return
        
        # Transform with pain messages
        pain_messages = [
            "You concentrate really, really hard, and begin to change shape.",
            "You begin to change before your very eyes.",
            "You scream in pain as your transformation continues.",
            "You scream in agony, as your transformation turns you into a quivering blob of goo.",
            "You whimper, and go silent as you black out from the pain.",
            "You lie there, slowly forming into a new form from the pile of goo you currently is.",
            "You finish your transformation.",
        ]
        
        for msg in pain_messages:
            caller.msg(msg)
            caller.location.msg_contents(
                f"{caller.key} {msg.lower()}",
                exclude=caller
            )
        
        # Apply form
        from world.guilds.shapeshifter import PLAYER_FORMS
        form_data = PLAYER_FORMS.get(form, {})
        
        # Store original form if not already stored
        if not getattr(caller.db, 'original_form', None):
            caller.db.original_form = 'natural'
        
        caller.db.current_form = form
        
        # Apply stat bonuses/penalties
        for stat, bonus in form_data.get('stat_bonuses', {}).items():
            caller.modify_stat(stat, bonus)
        for stat, penalty in form_data.get('stat_penalties', {}).items():
            caller.modify_stat(stat, -penalty)
        
        # Apply inventory restrictions
        can_hold = form_data.get('can_hold_inventory', True)
        if not can_hold:
            # Drop inventory to ground
            for obj in list(caller.contents):
                if hasattr(obj.db, 'is_equipped') and obj.db.is_equipped:
                    obj.db.is_equipped = False
                obj.move_to(caller.location, quiet=True)
                caller.msg(f"You drop {obj.key} as you can no longer hold it in this form.")
        
        # Recalculate stats
        if hasattr(caller, 'recalculate_stats'):
            caller.recalculate_stats()
        
        caller.msg(f"You have transformed into a {form}!")
        caller.location.msg_contents(
            f"{caller.key} transforms into a {form}!",
            exclude=caller
        )


class CmdReverseTransformation(Command):
    """
    Revert to your natural form.
    
    Usage:
        reverse_transformation
        revert
    """
    key = "reverse_transformation"
    aliases = ["revert", "unshift"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        current = getattr(caller.db, 'current_form', None)
        if not current:
            caller.msg("You are already in your natural form.")
            return
        
        # Revert
        from world.guilds.shapeshifter import PLAYER_FORMS
        form_data = PLAYER_FORMS.get(current, {})
        
        # Remove stat bonuses/penalties
        for stat, bonus in form_data.get('stat_bonuses', {}).items():
            caller.modify_stat(stat, -bonus)
        for stat, penalty in form_data.get('stat_penalties', {}).items():
            caller.modify_stat(stat, penalty)
        
        caller.db.current_form = None
        
        # Recalculate stats
        if hasattr(caller, 'recalculate_stats'):
            caller.recalculate_stats()
        
        caller.msg("You revert to your natural form.")
        caller.location.msg_contents(
            f"{caller.key} reverts to their natural form.",
            exclude=caller
        )


class CmdMigrate(Command):
    """
    Teleport to another island (bird/dragon forms only).
    
    Usage:
        migrate <island>
        migrate gossamer
    """
    key = "migrate"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        if not self.args:
            # Show migration destinations
            from world.guilds.shapeshifter import MIGRATE_DESTINATIONS
            caller.msg("-=-=-| Migrate Destinations |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            for island, bird in MIGRATE_DESTINATIONS.items():
                caller.msg(f"  {island.title()} - via {bird}")
            caller.msg("Usage: migrate <island_name>")
            return
        
        # Check if in bird or dragon form
        current = getattr(caller.db, 'current_form', '')
        from world.guilds.shapeshifter import PLAYER_FORMS
        form_data = PLAYER_FORMS.get(current, {})
        category = form_data.get('category', '')
        
        if category not in ['avian', 'dragon']:
            caller.msg("You must be in a bird or dragon form to migrate.")
            return
        
        island = self.args.strip().lower()
        from world.guilds.shapeshifter import MIGRATE_DESTINATIONS
        
        if island not in MIGRATE_DESTINATIONS:
            caller.msg(f"Unknown island: {island}")
            return
        
        bird = MIGRATE_DESTINATIONS[island]
        
        # Teleport to island hub
        from evennia import search_object
        hub = search_object(f"{island.title()} Island Hub")
        if hub:
            caller.msg(f"You take flight and soar toward {island.title()}, guided by the {bird}...")
            caller.location.msg_contents(
                f"{caller.key} takes flight and disappears into the sky.",
                exclude=caller
            )
            caller.move_to(hub[0], quiet=True)
            caller.msg(f"You arrive at {island.title()} Island.")
        else:
            caller.msg(f"You cannot find your way to {island.title()}.")


class CmdBite(Command):
    """
    Bite attack (shapeshifter forms).
    
    Usage:
        bite <target>
    """
    key = "bite"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        target_name = self.args.strip()
        
        if not target_name:
            caller.msg("Bite whom?")
            return
        
        # Check if in animal/dragon form
        current = getattr(caller.db, 'current_form', '')
        if not current:
            caller.msg("You must be in an animal form to bite.")
            return
        
        target = caller.search(target_name, location=caller.location)
        if not target:
            return
        
        # Bite attack message
        caller.msg(f"You decide {target.key} would look better as a fountain, and immediately turn your desire to reality. Blood sprays everywhere.")
        caller.location.msg_contents(
            f"{caller.key} bites {target.key} savagely!",
            exclude=caller
        )
        
        # Deal damage
        if hasattr(target.db, 'is_mob') and target.db.is_mob:
            damage = getattr(caller.db, 'level', 1) * 3
            target.db.hp -= damage
            if target.db.hp <= 0:
                target.db.ai_state = "dead"
                caller.msg(f"{target.key} is DEAD!")


class CmdClaw(Command):
    """
    Claw attack (shapeshifter forms).
    
    Usage:
        claw <target>
    """
    key = "claw"
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        target_name = self.args.strip()
        
        if not target_name:
            caller.msg("Claw whom?")
            return
        
        # Check if in animal/dragon form
        current = getattr(caller.db, 'current_form', '')
        if not current:
            caller.msg("You must be in an animal form to claw.")
            return
        
        target = caller.search(target_name, location=caller.location)
        if not target:
            return
        
        # Claw attack messages
        import random
        msgs = [
            f"You rip a hole in {target.key}'s side.",
            f"You tear {target.key}'s belly. Blood and guts scatter everywhere.",
        ]
        caller.msg(random.choice(msgs))
        
        # Deal damage
        if hasattr(target.db, 'is_mob') and target.db.is_mob:
            damage = getattr(caller.db, 'level', 1) * 2
            target.db.hp -= damage
            if target.db.hp <= 0:
                target.db.ai_state = "dead"
                caller.msg(f"{target.key} is DEAD!")


class CmdHerbGathering(Command):
    """
    Gather herbs for healing (shapeshifter skill).
    
    Usage:
        herb_gathering
        gather herbs
    """
    key = "herb_gathering"
    aliases = ["gather herbs", "gather_herbs"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if outdoors
        if caller.location and hasattr(caller.location.db, 'is_outdoors'):
            if not caller.location.db.is_outdoors:
                caller.msg("You need to be outside to gather herbs.")
                return
        
        import random
        herbs = ["green herb", "red herb", "brown herb", "white herb"]
        
        if random.random() < 0.7:
            herb = random.choice(herbs)
            from evennia import create_object
            obj = create_object("typeclasses.objects.Object", key=herb)
            obj.db.desc = f"A medicinal {herb} gathered from the wild."
            obj.db.edible = True
            obj.db.heal_hp = random.randint(10, 30)
            obj.move_to(caller, quiet=True)
            caller.msg(f"You spend some time examining the floor and finally pick up a {herb}.")
        else:
            caller.msg("You search around but fail to find any useful herb.")


class CmdMagicalGrowth(Command):
    """
    Grow magical plants for hunger (shapeshifter spell).
    
    Usage:
        magical_growth
        grow plants
    """
    key = "magical_growth"
    aliases = ["grow plants", "grow_plants"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        # Check if outdoors
        if caller.location and hasattr(caller.location.db, 'is_outdoors'):
            if not caller.location.db.is_outdoors:
                caller.msg("You must be outdoors to magically grow plants.")
                return
        
        import random
        plants = [
            ("green plant", "restores a small amount of hunger"),
            ("red and green plant", "restores twice as much as green"),
            ("brown plant", "restores three times as much as green"),
        ]
        
        if random.random() < 0.6:
            plant, desc = random.choice(plants)
            from evennia import create_object
            obj = create_object("typeclasses.objects.Object", key=plant)
            obj.db.desc = f"A magically grown {plant}. {desc}"
            obj.db.edible = True
            obj.db.heal_ep = random.randint(15, 50)
            obj.move_to(caller.location, quiet=True)
            caller.msg(f"You chant a simple incantation and bring your hands up slowly. Suddenly a small {plant} sprouts and grows beside your feet!")
            caller.location.msg_contents(
                f"A {plant} suddenly sprouts from the ground near {caller.key}.",
                exclude=caller
            )
        else:
            caller.msg("You chant the words to the spell and make lifting motions with your hands, but nothing happens.")


class CmdScavengeWood(Command):
    """
    Find firewood (shapeshifter skill).
    
    Usage:
        scavenge_wood
        scavenge wood
    """
    key = "scavenge_wood"
    aliases = ["scavenge wood"]
    locks = "cmd:all()"
    
    def func(self):
        caller = self.caller
        
        import random
        if random.random() < 0.6:
            from evennia import create_object
            wood = create_object("typeclasses.objects.Object", key="firewood")
            wood.db.desc = "A pile of firewood scavenged from the area."
            wood.move_to(caller, quiet=True)
            caller.msg("You find some firewood.")
        else:
            caller.msg("You search around but disappointingly find absolutely nothing.")
