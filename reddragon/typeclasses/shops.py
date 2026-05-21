"""
Red Dragon MUD - Shop and Bank System
Based on Islands of Myth economy
"""

from evennia import DefaultObject

class Shopkeeper(DefaultObject):
    """
    A shopkeeper NPC that buys and sells items.
    Based on IOM shop system.
    """
    
    def at_object_creation(self):
        self.db.is_shopkeeper = True
        self.db.shop_type = "general"  # general, weapon, armor, magic, food
        self.db.items_for_sale = {}  # {item_key: {price: int, stock: int}}
        self.db.buy_multiplier = 0.5  # Shop buys at 50% of value
        self.db.sell_multiplier = 1.0  # Shop sells at 100% of value
        
    def list_items(self):
        """Return formatted list of items for sale."""
        if not self.db.items_for_sale:
            return "I have nothing for sale right now."
            
        output = ["Items for sale:"]
        for item_key, data in self.db.items_for_sale.items():
            price = data.get('price', 0)
            stock = data.get('stock', 1)
            stock_str = f"({stock} in stock)" if stock > 1 else ""
            output.append(f"  {item_key:<30} {price:>6} gold {stock_str}")
            
        return "\n".join(output)
        
    def sell_item(self, character, item_key, quantity=1):
        """Sell an item to a character."""
        if item_key not in self.db.items_for_sale:
            character.msg(f"I don't sell {item_key}.")
            return False
            
        data = self.db.items_for_sale[item_key]
        price = data.get('price', 0) * quantity
        stock = data.get('stock', 1)
        
        if stock < quantity:
            character.msg(f"I only have {stock} of those in stock.")
            return False
            
        if character.db.gold < price:
            character.msg(f"You can't afford that. It costs {price} gold.")
            return False
            
        # Deduct gold
        character.db.gold -= price
        
        # Create and give item
        from evennia import create_object
        for _ in range(quantity):
            item = create_object("typeclasses.objects.Object", key=item_key, location=character)
            item.db.value = price
            
        # Update stock
        data['stock'] -= quantity
        if data['stock'] <= 0:
            del self.db.items_for_sale[item_key]
            
        character.msg(f"You buy {quantity}x {item_key} for {price} gold.")
        return True
        
    def buy_item(self, character, item_key):
        """Buy an item from a character."""
        # Find item in character inventory
        item = character.search(item_key, location=character)
        if not item:
            character.msg("You don't have that.")
            return False
            
        # Calculate buy price
        value = getattr(item.db, 'value', 10)
        buy_price = int(value * self.db.buy_multiplier)
        
        # Transfer gold
        character.db.gold += buy_price
        item.move_to(self, quiet=True)
        
        character.msg(f"You sell {item_key} for {buy_price} gold.")
        return True


class Bank(DefaultObject):
    """
    A bank object where characters can deposit and withdraw gold.
    """
    
    def at_object_creation(self):
        self.db.is_bank = True
        self.db.accounts = {}  # {character_id: balance}
        
    def deposit(self, character, amount):
        """Deposit gold into bank account."""
        if character.db.gold < amount:
            character.msg("You don't have that much gold.")
            return False
            
        char_id = character.id
        if char_id not in self.db.accounts:
            self.db.accounts[char_id] = 0
            
        self.db.accounts[char_id] += amount
        character.db.gold -= amount
        character.db.bank_gold = self.db.accounts[char_id]
        
        character.msg(f"You deposit {amount} gold. Balance: {self.db.accounts[char_id]} gold.")
        return True
        
    def withdraw(self, character, amount):
        """Withdraw gold from bank account."""
        char_id = character.id
        balance = self.db.accounts.get(char_id, 0)
        
        if balance < amount:
            character.msg("You don't have that much in the bank.")
            return False
            
        self.db.accounts[char_id] -= amount
        character.db.gold += amount
        character.db.bank_gold = self.db.accounts[char_id]
        
        character.msg(f"You withdraw {amount} gold. Balance: {self.db.accounts[char_id]} gold.")
        return True
        
    def balance(self, character):
        """Check bank balance."""
        char_id = character.id
        balance = self.db.accounts.get(char_id, 0)
        character.msg(f"Your bank balance is {balance} gold.")
        return balance


class AuctionHouse(DefaultObject):
    """
    Auction house for player-to-player trading.
    """
    
    def at_object_creation(self):
        self.db.is_auction = True
        self.db.listings = []  # [{seller, item, price, expires}]
        
    def list_item(self, character, item, price, duration_hours=24):
        """List an item for auction."""
        listing = {
            'seller': character.key,
            'item': item.key,
            'price': price,
            'expires': None,  # Would use actual time
        }
        self.db.listings.append(listing)
        item.move_to(self, quiet=True)
        character.msg(f"You list {item.key} for {price} gold.")
        return True
        
    def browse(self, character):
        """Show current auction listings."""
        if not self.db.listings:
            character.msg("No items currently for sale.")
            return
            
        output = ["Current Auction Listings:"]
        for i, listing in enumerate(self.db.listings, 1):
            output.append(f"  {i}. {listing['item']} - {listing['price']} gold (seller: {listing['seller']})")
            
        character.msg("\n".join(output))
