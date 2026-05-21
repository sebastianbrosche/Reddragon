"""
Red Dragon MUD - Economy Commands
Buy, sell, deposit, withdraw, auction
"""

from evennia import Command

class CmdBuy(Command):
    """
    Buy an item from a shopkeeper.
    
    Usage:
        buy <item>
        buy <quantity> <item>
    """
    key = "buy"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Buy what?")
            return
            
        # Find shopkeeper in room
        shopkeeper = None
        for obj in self.caller.location.contents:
            if hasattr(obj.db, 'is_shopkeeper') and obj.db.is_shopkeeper:
                shopkeeper = obj
                break
                
        if not shopkeeper:
            self.caller.msg("There is no shopkeeper here.")
            return
            
        args = self.args.strip().split()
        
        # Check for quantity prefix
        if len(args) > 1 and args[0].isdigit():
            quantity = int(args[0])
            item_key = " ".join(args[1:])
        else:
            quantity = 1
            item_key = self.args.strip()
            
        shopkeeper.sell_item(self.caller, item_key, quantity)


class CmdSell(Command):
    """
    Sell an item to a shopkeeper.
    
    Usage:
        sell <item>
    """
    key = "sell"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Sell what?")
            return
            
        # Find shopkeeper in room
        shopkeeper = None
        for obj in self.caller.location.contents:
            if hasattr(obj.db, 'is_shopkeeper') and obj.db.is_shopkeeper:
                shopkeeper = obj
                break
                
        if not shopkeeper:
            self.caller.msg("There is no shopkeeper here.")
            return
            
        shopkeeper.buy_item(self.caller, self.args.strip())


class CmdList(Command):
    """
    List items for sale at a shop.
    
    Usage:
        list
    """
    key = "list"
    locks = "cmd:all()"
    
    def func(self):
        # Find shopkeeper in room
        shopkeeper = None
        for obj in self.caller.location.contents:
            if hasattr(obj.db, 'is_shopkeeper') and obj.db.is_shopkeeper:
                shopkeeper = obj
                break
                
        if not shopkeeper:
            self.caller.msg("There is no shopkeeper here.")
            return
            
        self.caller.msg(shopkeeper.list_items())


class CmdDeposit(Command):
    """
    Deposit gold at the bank.
    
    Usage:
        deposit <amount>
        deposit all
    """
    key = "deposit"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Deposit how much?")
            return
            
        # Find bank in room
        bank = None
        for obj in self.caller.location.contents:
            if hasattr(obj.db, 'is_bank') and obj.db.is_bank:
                bank = obj
                break
                
        if not bank:
            self.caller.msg("There is no bank here.")
            return
            
        args = self.args.strip().lower()
        if args == "all":
            amount = self.caller.db.gold
        else:
            try:
                amount = int(args)
            except ValueError:
                self.caller.msg("Deposit how much?")
                return
                
        bank.deposit(self.caller, amount)


class CmdWithdraw(Command):
    """
    Withdraw gold from the bank.
    
    Usage:
        withdraw <amount>
        withdraw all
    """
    key = "withdraw"
    locks = "cmd:all()"
    
    def func(self):
        if not self.args:
            self.caller.msg("Withdraw how much?")
            return
            
        # Find bank in room
        bank = None
        for obj in self.caller.location.contents:
            if hasattr(obj.db, 'is_bank') and obj.db.is_bank:
                bank = obj
                break
                
        if not bank:
            self.caller.msg("There is no bank here.")
            return
            
        args = self.args.strip().lower()
        if args == "all":
            char_id = self.caller.id
            amount = bank.db.accounts.get(char_id, 0)
        else:
            try:
                amount = int(args)
            except ValueError:
                self.caller.msg("Withdraw how much?")
                return
                
        bank.withdraw(self.caller, amount)


class CmdBalance(Command):
    """
    Check bank balance.
    
    Usage:
        balance
    """
    key = "balance"
    locks = "cmd:all()"
    
    def func(self):
        # Find bank in room
        bank = None
        for obj in self.caller.location.contents:
            if hasattr(obj.db, 'is_bank') and obj.db.is_bank:
                bank = obj
                break
                
        if not bank:
            self.caller.msg("There is no bank here.")
            return
            
        bank.balance(self.caller)
