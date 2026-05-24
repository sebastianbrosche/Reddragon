"""
Red Dragon MUD - Bot Admin Commands
Launch, stop, and monitor exploration bots.
"""

from evennia import Command

class CmdBots(Command):
    """
    Manage exploration bots.
    
    Usage:
        @bots launch [count]
        @bots stop
        @bots status
        @bots killall
    """
    key = "@bots"
    locks = "cmd:perm(Builder)"
    
    def func(self):
        caller = self.caller
        args = self.args.strip().split()
        
        if not args:
            caller.msg("Usage: @bots launch [count] | stop | status | killall")
            return
        
        action = args[0].lower()
        
        if action == "launch":
            count = 5
            if len(args) > 1:
                try:
                    count = int(args[1])
                except ValueError:
                    caller.msg("Invalid count. Using default 5.")
            
            from world.bots import launch_bots
            results = launch_bots(count)
            
            caller.msg(f"Launched {len(results)} bots:")
            for r in results:
                caller.msg(f"  {r}")
            
            # Start tick script
            from typeclasses.scripts.bot_tick import start_bot_tick
            script = start_bot_tick()
            if script:
                caller.msg("Bot exploration tick started (every 15s).")
            
        elif action == "stop":
            from world.bots import stop_bots
            stop_bots()
            
            from typeclasses.scripts.bot_tick import stop_bot_tick
            stop_bot_tick()
            
            caller.msg("All bots stopped.")
            
        elif action == "status":
            from world.bots import get_bot_stats
            stats = get_bot_stats()
            
            if not stats:
                caller.msg("No bots active.")
                return
            
            caller.msg("-=-=-| Bot Status |-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            for bot in stats:
                caller.msg(f"  {bot['name']}: Lv{bot['level']} {bot['guild'] or 'No Guild'} | "
                           f"Rooms: {bot['rooms']} | XP: {bot['xp']:,} | State: {bot['state']} | "
                           f"Loc: {bot['location']}")
            caller.msg(f"Total bots: {len(stats)}")
            caller.msg("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            
        elif action == "killall":
            from typeclasses.characters import Character
            from evennia.accounts.models import AccountDB
            
            killed = 0
            for char in Character.objects.all():
                if getattr(char.db, 'is_bot', False):
                    # Delete account too
                    if char.account:
                        char.account.delete()
                    char.delete()
                    killed += 1
            
            from typeclasses.scripts.bot_tick import stop_bot_tick
            stop_bot_tick()
            
            caller.msg(f"Killed {killed} bots and stopped tick.")
            
        else:
            caller.msg("Unknown action. Use: launch, stop, status, killall")
