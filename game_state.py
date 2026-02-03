"""
MONOPOLY GUI - Game State Manager
"""

import random
from typing import List, Optional, Tuple
from player import Player
from property import Property
from config import (
    SPACE_NAMES, PROPERTY_COLORS, GROUP_SIZES,
    CHANCE_CARDS, COMMUNITY_CARDS
)


class GameState:
    """Manages the complete game state."""
    
    def __init__(self):
        self.players: List[Player] = []
        self.properties: List[Property] = [Property(i) for i in range(40)]
        self.current_player_index: int = 0
        self.dice: Tuple[int, int] = (0, 0)
        self.doubles_count: int = 0
        self.game_started: bool = False
        self.game_over: bool = False
        self.winner: Optional[Player] = None
        
        # Card decks
        self.chance_deck = list(range(len(CHANCE_CARDS)))
        self.community_deck = list(range(len(COMMUNITY_CARDS)))
        random.shuffle(self.chance_deck)
        random.shuffle(self.community_deck)
        
        # Message log
        self.messages: List[str] = []
    
    def add_player(self, name: str, is_ai: bool = False) -> Player:
        """Add a new player to the game."""
        player_id = len(self.players)
        player = Player(player_id, name, is_ai)
        self.players.append(player)
        return player
    
    @property
    def current_player(self) -> Optional[Player]:
        """Get the current player."""
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    @property
    def active_players(self) -> List[Player]:
        """Get list of non-bankrupt players."""
        return [p for p in self.players if not p.bankrupt]
    
    def roll_dice(self) -> Tuple[int, int]:
        """Roll the dice and return the result."""
        self.dice = (random.randint(1, 6), random.randint(1, 6))
        return self.dice
    
    @property
    def dice_total(self) -> int:
        """Get the total of the current dice roll."""
        return self.dice[0] + self.dice[1]
    
    @property
    def is_doubles(self) -> bool:
        """Check if the current roll is doubles."""
        return self.dice[0] == self.dice[1]
    
    def has_monopoly(self, player: Player, color: str) -> bool:
        """Check if a player has a monopoly on a color group."""
        if not color or color not in GROUP_SIZES:
            return False
        
        owned = sum(
            1 for prop in self.properties 
            if prop.color == color and prop.owner == player
        )
        return owned == GROUP_SIZES[color]
    
    def get_properties_in_group(self, color: str) -> List[Property]:
        """Get all properties in a color group."""
        return [prop for prop in self.properties if prop.color == color]
    
    def next_player(self):
        """Move to the next active player."""
        self.doubles_count = 0
        start = self.current_player_index
        
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if not self.players[self.current_player_index].bankrupt:
                break
            if self.current_player_index == start:
                break
    
    def check_winner(self) -> Optional[Player]:
        """Check if there's a winner (only one player left)."""
        active = self.active_players
        if len(active) == 1:
            self.game_over = True
            self.winner = active[0]
            return self.winner
        return None
    
    def draw_chance_card(self) -> Tuple[str, str]:
        """Draw a Chance card."""
        if not self.chance_deck:
            self.chance_deck = list(range(len(CHANCE_CARDS)))
            random.shuffle(self.chance_deck)
        
        card_index = self.chance_deck.pop(0)
        return CHANCE_CARDS[card_index]
    
    def draw_community_card(self) -> Tuple[str, str]:
        """Draw a Community Chest card."""
        if not self.community_deck:
            self.community_deck = list(range(len(COMMUNITY_CARDS)))
            random.shuffle(self.community_deck)
        
        card_index = self.community_deck.pop(0)
        return COMMUNITY_CARDS[card_index]
    
    def log_message(self, message: str):
        """Add a message to the game log."""
        self.messages.append(message)
        # Keep only last 100 messages
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]
    
    def execute_card_action(self, player: Player, action: str):
        """Execute a card action."""
        if action == "go":
            player.move_to(0)
            player.add_money(200)
            self.log_message(f"{player.name} advances to GO and collects $200!")
        
        elif action.startswith("move_to_"):
            pos = int(action.split("_")[-1])
            passed_go = player.move_to(pos)
            self.log_message(f"{player.name} moves to {SPACE_NAMES[pos]}")
            if passed_go:
                self.log_message(f"{player.name} passed GO and collected $200!")
        
        elif action == "back_3":
            player.position = (player.position - 3) % 40
            self.log_message(f"{player.name} goes back 3 spaces to {SPACE_NAMES[player.position]}")
        
        elif action == "go_to_jail":
            player.go_to_jail()
            self.log_message(f"{player.name} goes directly to Jail!")
        
        elif action == "jail_card":
            player.get_out_of_jail_cards += 1
            self.log_message(f"{player.name} receives a Get Out of Jail Free card!")
        
        elif action.startswith("collect_"):
            amount = int(action.split("_")[-1])
            player.add_money(amount)
            self.log_message(f"{player.name} collects ${amount}")
        
        elif action.startswith("pay_"):
            amount = int(action.split("_")[-1])
            player.subtract_money(amount)
            self.log_message(f"{player.name} pays ${amount}")
        
        elif action == "pay_each_50":
            for other in self.players:
                if other != player and not other.bankrupt:
                    player.subtract_money(50)
                    other.add_money(50)
            self.log_message(f"{player.name} pays $50 to each player")
        
        elif action == "collect_from_each_50":
            for other in self.players:
                if other != player and not other.bankrupt:
                    other.subtract_money(50)
                    player.add_money(50)
            self.log_message(f"{player.name} collects $50 from each player")
        
        elif action == "collect_from_each_10":
            for other in self.players:
                if other != player and not other.bankrupt:
                    other.subtract_money(10)
                    player.add_money(10)
            self.log_message(f"{player.name} collects $10 from each player")
        
        elif action == "repairs_25_100":
            total = 0
            for prop_idx in player.properties:
                prop = self.properties[prop_idx]
                if prop.houses == 5:
                    total += 100
                else:
                    total += prop.houses * 25
            player.subtract_money(total)
            self.log_message(f"{player.name} pays ${total} for repairs")
        
        elif action == "repairs_40_115":
            total = 0
            for prop_idx in player.properties:
                prop = self.properties[prop_idx]
                if prop.houses == 5:
                    total += 115
                else:
                    total += prop.houses * 40
            player.subtract_money(total)
            self.log_message(f"{player.name} pays ${total} for street repairs")
        
        elif action == "nearest_railroad":
            # Find nearest railroad
            railroads = [5, 15, 25, 35]
            for rr in railroads:
                if rr > player.position:
                    player.move_to(rr)
                    break
            else:
                player.move_to(5)
                player.add_money(200)  # Passed GO
            self.log_message(f"{player.name} advances to nearest railroad")
        
        elif action == "nearest_utility":
            utilities = [12, 28]
            for util in utilities:
                if util > player.position:
                    player.move_to(util)
                    break
            else:
                player.move_to(12)
                player.add_money(200)
            self.log_message(f"{player.name} advances to nearest utility")
