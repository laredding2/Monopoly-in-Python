"""
MONOPOLY GUI - Property Class
"""

from config import (
    SPACE_NAMES, PROPERTY_PRICES, PROPERTY_RENTS, 
    PROPERTY_COLORS, HOUSE_PRICES, GROUP_SIZES
)


class Property:
    """Represents a property on the board."""
    
    def __init__(self, index: int):
        self.index = index
        self.name = SPACE_NAMES[index]
        self.price = PROPERTY_PRICES[index]
        self.base_rent = PROPERTY_RENTS[index]
        self.color = PROPERTY_COLORS[index]
        self.owner = None
        self.houses = 0  # 5 = hotel
        self.mortgaged = False
    
    @property
    def is_property(self) -> bool:
        """Check if this space is a purchasable property."""
        return self.price > 0
    
    @property
    def is_railroad(self) -> bool:
        """Check if this is a railroad."""
        return self.color == "railroad"
    
    @property
    def is_utility(self) -> bool:
        """Check if this is a utility."""
        return self.color == "utility"
    
    @property
    def house_price(self) -> int:
        """Get the price to build a house on this property."""
        if self.color and self.color in HOUSE_PRICES:
            return HOUSE_PRICES[self.color]
        return 0
    
    @property
    def mortgage_value(self) -> int:
        """Get the mortgage value of this property."""
        return self.price // 2
    
    @property
    def unmortgage_cost(self) -> int:
        """Get the cost to unmortgage this property (mortgage + 10%)."""
        return int(self.mortgage_value * 1.1)
    
    def can_build(self, game_state) -> bool:
        """Check if a house can be built on this property."""
        if not self.owner or self.mortgaged or self.houses >= 5:
            return False
        if self.is_railroad or self.is_utility or not self.color:
            return False
        
        # Check if owner has monopoly
        if not game_state.has_monopoly(self.owner, self.color):
            return False
        
        # Check for even building rule
        min_houses = min(
            game_state.properties[i].houses 
            for i in range(40) 
            if game_state.properties[i].color == self.color and game_state.properties[i].owner == self.owner
        )
        
        return self.houses <= min_houses
    
    def calculate_rent(self, game_state, dice_roll: int = 0) -> int:
        """Calculate the rent for landing on this property."""
        if not self.owner or self.mortgaged:
            return 0
        
        if self.is_railroad:
            # Count railroads owned
            rr_count = sum(
                1 for i in [5, 15, 25, 35] 
                if game_state.properties[i].owner == self.owner
            )
            return 25 * (2 ** (rr_count - 1))
        
        if self.is_utility:
            # Count utilities owned
            util_count = sum(
                1 for i in [12, 28] 
                if game_state.properties[i].owner == self.owner
            )
            multiplier = 4 if util_count == 1 else 10
            return dice_roll * multiplier
        
        # Regular property
        if self.houses == 0:
            rent = self.base_rent
            # Double rent for monopoly
            if game_state.has_monopoly(self.owner, self.color):
                rent *= 2
            return rent
        
        # Rent with houses (approximate standard Monopoly rates)
        rent_multipliers = [1, 5, 15, 45, 80, 125]  # 0-4 houses, 5 = hotel
        return self.base_rent * rent_multipliers[self.houses]
    
    def mortgage(self):
        """Mortgage this property."""
        if not self.mortgaged and self.houses == 0:
            self.mortgaged = True
            return self.mortgage_value
        return 0
    
    def unmortgage(self) -> int:
        """Unmortgage this property. Returns cost."""
        if self.mortgaged:
            cost = self.unmortgage_cost
            self.mortgaged = False
            return cost
        return 0
    
    def build_house(self) -> int:
        """Build a house. Returns cost."""
        if self.houses < 5:
            self.houses += 1
            return self.house_price
        return 0
    
    def sell_house(self) -> int:
        """Sell a house. Returns money received (half of house price)."""
        if self.houses > 0:
            self.houses -= 1
            return self.house_price // 2
        return 0
    
    def __str__(self):
        status = ""
        if self.owner:
            status = f" (Owner: {self.owner.name})"
            if self.mortgaged:
                status += " [M]"
            elif self.houses > 0:
                status += f" [{self.houses}H]" if self.houses < 5 else " [Hotel]"
        return f"{self.name}{status}"
