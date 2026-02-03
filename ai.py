"""
MONOPOLY GUI - AI Player Logic
"""

import random
from typing import Optional, List, Tuple
from config import PROPERTY_COLORS, HOUSE_PRICES, GROUP_SIZES


class AIPlayer:
    """AI decision-making logic for computer players."""
    
    # Difficulty levels
    EASY = 1
    MEDIUM = 2
    HARD = 3
    
    def __init__(self, difficulty: int = MEDIUM):
        self.difficulty = difficulty
    
    def property_value_score(self, prop_idx: int, player, game_state) -> int:
        """Calculate a value score for a property (higher = more valuable)."""
        prop = game_state.properties[prop_idx]
        score = 50  # Base score
        
        if prop.is_railroad:
            rr_owned = sum(1 for i in [5, 15, 25, 35] 
                         if game_state.properties[i].owner == player)
            score += 20 + rr_owned * 15
        
        elif prop.is_utility:
            score += 10
        
        elif prop.color:
            # Count owned in group
            owned = sum(1 for p in game_state.properties 
                       if p.color == prop.color and p.owner == player)
            needed = GROUP_SIZES.get(prop.color, 3) - owned
            
            # Huge bonus if this completes a monopoly
            if needed == 1:
                score += 100
            elif owned > 0:
                score += 40
            
            # Check if opponent wants this color
            for other in game_state.players:
                if other != player and not other.bankrupt:
                    other_owned = sum(1 for p in game_state.properties 
                                     if p.color == prop.color and p.owner == other)
                    if other_owned > 0:
                        score += 30
                        break
            
            # Premium color groups
            if prop.color in ["orange", "red"]:
                score += 25
            elif prop.color in ["yellow", "green"]:
                score += 15
            elif prop.color in ["lightblue", "pink"]:
                score += 10
        
        # Prefer cheaper properties when low on money
        if player.money < 800:
            if prop.price <= 150:
                score += 20
            elif prop.price >= 300:
                score -= 15
        
        return score
    
    def decide_buy_property(self, player, prop_idx: int, game_state) -> bool:
        """Decide whether to buy a property."""
        prop = game_state.properties[prop_idx]
        
        if player.money < prop.price:
            return False
        
        score = self.property_value_score(prop_idx, player, game_state)
        money_after = player.money - prop.price
        
        if self.difficulty == self.EASY:
            return random.random() < 0.6
        
        elif self.difficulty == self.MEDIUM:
            if score >= 150:
                return True
            if money_after >= 150 and score >= 50:
                return True
            if prop.price <= 150 and money_after >= 50:
                return True
            return False
        
        else:  # HARD
            if prop.is_railroad and money_after >= 100:
                return True
            if score >= 150 and money_after >= 50:
                return True
            if score >= 80 and money_after >= 200:
                return True
            if score >= 70 and money_after >= 150:
                return True
            return False
    
    def decide_build_house(self, player, game_state) -> Optional[int]:
        """Decide which property to build a house on. Returns property index or None."""
        min_buffer = {self.EASY: 200, self.MEDIUM: 150, self.HARD: 100}[self.difficulty]
        
        best_property = None
        best_score = 0
        
        for prop_idx in player.properties:
            prop = game_state.properties[prop_idx]
            
            if not prop.can_build(game_state):
                continue
            
            if player.money - prop.house_price < min_buffer:
                continue
            
            # Calculate building score
            score = 100 - prop.houses * 20  # Prefer even building
            
            if prop.house_price <= 100:
                score += 20
            
            score += prop.base_rent // 2
            
            if score > best_score:
                best_score = score
                best_property = prop_idx
        
        # Easy AI builds less often
        if self.difficulty == self.EASY and random.random() < 0.4:
            return None
        
        return best_property
    
    def decide_mortgage(self, player, game_state, needed: int) -> Optional[int]:
        """Decide which property to mortgage. Returns property index or None."""
        if player.money >= needed:
            return None
        
        best_property = None
        best_score = float('inf')
        
        for prop_idx in player.properties:
            prop = game_state.properties[prop_idx]
            
            if prop.mortgaged or prop.houses > 0:
                continue
            
            score = self.property_value_score(prop_idx, player, game_state)
            
            if score < best_score:
                best_score = score
                best_property = prop_idx
        
        return best_property
    
    def decide_unmortgage(self, player, game_state) -> Optional[int]:
        """Decide which property to unmortgage. Returns property index or None."""
        min_buffer = {self.EASY: 500, self.MEDIUM: 300, self.HARD: 200}[self.difficulty]
        
        best_property = None
        best_score = 0
        
        for prop_idx in player.properties:
            prop = game_state.properties[prop_idx]
            
            if not prop.mortgaged:
                continue
            
            if player.money - prop.unmortgage_cost < min_buffer:
                continue
            
            score = self.property_value_score(prop_idx, player, game_state)
            
            if score > best_score:
                best_score = score
                best_property = prop_idx
        
        return best_property
    
    def decide_jail_strategy(self, player, game_state) -> str:
        """Decide jail strategy. Returns 'pay', 'card', or 'roll'."""
        # Count monopolies
        monopoly_count = 0
        for color in HOUSE_PRICES.keys():
            if game_state.has_monopoly(player, color):
                monopoly_count += 1
        
        # Use card if we have one and have monopolies or it's late in jail
        if player.get_out_of_jail_cards > 0:
            if monopoly_count > 0 or player.jail_turns >= 2:
                return "card"
        
        # Pay if we have money and monopolies to build on
        if player.money >= 200 and monopoly_count > 0:
            return "pay"
        
        # Otherwise try to roll
        return "roll"
    
    def get_all_actions(self, player, game_state) -> List[Tuple[str, any]]:
        """Get all actions the AI wants to take before rolling."""
        actions = []
        
        # Try to build houses (up to 3 per turn)
        for _ in range(3):
            build_prop = self.decide_build_house(player, game_state)
            if build_prop is not None:
                actions.append(("build", build_prop))
            else:
                break
        
        # Try to unmortgage
        unmortgage_prop = self.decide_unmortgage(player, game_state)
        if unmortgage_prop is not None:
            actions.append(("unmortgage", unmortgage_prop))
        
        return actions
