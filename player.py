"""
MONOPOLY GUI - Player Class
"""

from config import STARTING_MONEY, TOKENS, COLORS


class Player:
    """Represents a player in the game."""
    
    def __init__(self, player_id: int, name: str, is_ai: bool = False):
        self.id = player_id
        self.name = name
        self.is_ai = is_ai
        self.money = STARTING_MONEY
        self.position = 0
        self.token = TOKENS[player_id]
        self.color = COLORS['player_colors'][player_id]
        self.in_jail = False
        self.jail_turns = 0
        self.bankrupt = False
        self.get_out_of_jail_cards = 0
        self.properties = []  # List of property indices owned
    
    def add_money(self, amount: int):
        """Add money to player's balance."""
        self.money += amount
    
    def subtract_money(self, amount: int) -> bool:
        """
        Subtract money from player's balance.
        Returns True if successful, False if not enough money.
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def move_to(self, position: int, collect_go: bool = True) -> bool:
        """
        Move player to a specific position.
        Returns True if player passed GO.
        """
        passed_go = False
        if collect_go and position < self.position and position != 0:
            self.add_money(200)
            passed_go = True
        self.position = position
        return passed_go
    
    def move_forward(self, spaces: int) -> bool:
        """
        Move player forward by a number of spaces.
        Returns True if player passed GO.
        """
        old_position = self.position
        self.position = (self.position + spaces) % 40
        passed_go = self.position < old_position
        if passed_go:
            self.add_money(200)
        return passed_go
    
    def go_to_jail(self):
        """Send player to jail."""
        self.position = 10
        self.in_jail = True
        self.jail_turns = 0
    
    def release_from_jail(self):
        """Release player from jail."""
        self.in_jail = False
        self.jail_turns = 0
    
    def add_property(self, property_index: int):
        """Add a property to player's portfolio."""
        if property_index not in self.properties:
            self.properties.append(property_index)
    
    def remove_property(self, property_index: int):
        """Remove a property from player's portfolio."""
        if property_index in self.properties:
            self.properties.remove(property_index)
    
    def get_net_worth(self, game_state) -> int:
        """Calculate total net worth including properties."""
        total = self.money
        for prop_idx in self.properties:
            prop = game_state.properties[prop_idx]
            if prop.mortgaged:
                total += prop.price // 2
            else:
                total += prop.price
                total += prop.houses * prop.house_price
        return total
    
    def declare_bankruptcy(self, game_state, creditor=None):
        """Handle bankruptcy - transfer assets to creditor or bank."""
        self.bankrupt = True
        
        for prop_idx in self.properties[:]:  # Copy list to avoid modification during iteration
            prop = game_state.properties[prop_idx]
            if creditor:
                prop.owner = creditor
                creditor.add_property(prop_idx)
            else:
                prop.owner = None
                prop.houses = 0
                prop.mortgaged = False
            self.remove_property(prop_idx)
        
        if creditor:
            creditor.add_money(self.money)
        
        self.money = 0
    
    def __str__(self):
        ai_tag = " (AI)" if self.is_ai else ""
        return f"{self.token} {self.name}{ai_tag}: ${self.money}"
