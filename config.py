"""
MONOPOLY GUI - Configuration & Constants
"""

# Window settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
BOARD_SIZE = 700
CELL_SIZE = BOARD_SIZE // 11

# Colors
COLORS = {
    'board_bg': '#C8E6C9',
    'cell_bg': '#FFFFFF',
    'go': '#90EE90',
    'jail': '#FFA500',
    'free_parking': '#FF6347',
    'go_to_jail': '#4169E1',
    'chance': '#FF8C00',
    'community_chest': '#87CEEB',
    'tax': '#D3D3D3',
    'railroad': '#2F2F2F',
    'utility': '#E0E0E0',
    
    # Property colors
    'brown': '#8B4513',
    'lightblue': '#87CEEB',
    'pink': '#FF69B4',
    'orange': '#FFA500',
    'red': '#FF0000',
    'yellow': '#FFFF00',
    'green': '#008000',
    'blue': '#0000FF',
    
    # Player colors
    'player_colors': ['#E53935', '#1E88E5', '#43A047', '#FDD835', '#8E24AA', '#FF8A65'],
    
    # UI colors
    'button_bg': '#4CAF50',
    'button_hover': '#45a049',
    'panel_bg': '#F5F5F5',
    'text_dark': '#212121',
    'text_light': '#FFFFFF',
    'money_green': '#2E7D32',
    'warning_red': '#C62828',
}

# Player tokens (emoji/symbols)
TOKENS = ['🎩', '🚗', '🐕', '⛵', '👢', '🎲']
TOKEN_NAMES = ['Top Hat', 'Car', 'Dog', 'Ship', 'Boot', 'Dice']

# Starting money
STARTING_MONEY = 1500

# Board spaces (40 spaces, 0-39)
SPACE_NAMES = [
    "GO",
    "Mediterranean Avenue",
    "Community Chest",
    "Baltic Avenue",
    "Income Tax",
    "Reading Railroad",
    "Oriental Avenue",
    "Chance",
    "Vermont Avenue",
    "Connecticut Avenue",
    "Jail / Just Visiting",
    "St. Charles Place",
    "Electric Company",
    "States Avenue",
    "Virginia Avenue",
    "Pennsylvania Railroad",
    "St. James Place",
    "Community Chest",
    "Tennessee Avenue",
    "New York Avenue",
    "Free Parking",
    "Kentucky Avenue",
    "Chance",
    "Indiana Avenue",
    "Illinois Avenue",
    "B&O Railroad",
    "Atlantic Avenue",
    "Ventnor Avenue",
    "Water Works",
    "Marvin Gardens",
    "Go To Jail",
    "Pacific Avenue",
    "North Carolina Avenue",
    "Community Chest",
    "Pennsylvania Avenue",
    "Short Line Railroad",
    "Chance",
    "Park Place",
    "Luxury Tax",
    "Boardwalk"
]

# Short names for board display
SPACE_SHORT_NAMES = [
    "GO",
    "Mediterranean",
    "Community\nChest",
    "Baltic",
    "Income\nTax",
    "Reading\nRR",
    "Oriental",
    "Chance",
    "Vermont",
    "Connecticut",
    "JAIL",
    "St. Charles",
    "Electric\nCompany",
    "States",
    "Virginia",
    "Penn.\nRR",
    "St. James",
    "Community\nChest",
    "Tennessee",
    "New York",
    "FREE\nPARKING",
    "Kentucky",
    "Chance",
    "Indiana",
    "Illinois",
    "B&O\nRR",
    "Atlantic",
    "Ventnor",
    "Water\nWorks",
    "Marvin\nGardens",
    "GO TO\nJAIL",
    "Pacific",
    "N. Carolina",
    "Community\nChest",
    "Pennsylvania",
    "Short Line\nRR",
    "Chance",
    "Park\nPlace",
    "Luxury\nTax",
    "Boardwalk"
]

# Property prices
PROPERTY_PRICES = [
    0, 60, 0, 60, 200, 200, 100, 0, 100, 120,
    0, 140, 150, 140, 160, 200, 180, 0, 180, 200,
    0, 220, 0, 220, 240, 200, 260, 260, 150, 280,
    0, 300, 300, 0, 320, 200, 0, 350, 100, 400
]

# Property rents (base rent without houses)
PROPERTY_RENTS = [
    0, 2, 0, 4, 0, 25, 6, 0, 6, 8,
    0, 10, 0, 10, 12, 25, 14, 0, 14, 16,
    0, 18, 0, 18, 20, 25, 22, 22, 0, 24,
    0, 26, 26, 0, 28, 25, 0, 35, 0, 50
]

# Property colors (for grouping)
PROPERTY_COLORS = [
    None, "brown", None, "brown", None, "railroad", "lightblue", None, "lightblue", "lightblue",
    None, "pink", "utility", "pink", "pink", "railroad", "orange", None, "orange", "orange",
    None, "red", None, "red", "red", "railroad", "yellow", "yellow", "utility", "yellow",
    None, "green", "green", None, "green", "railroad", None, "blue", None, "blue"
]

# House prices per color group
HOUSE_PRICES = {
    "brown": 50, "lightblue": 50, "pink": 100, "orange": 100,
    "red": 150, "yellow": 150, "green": 200, "blue": 200
}

# Group sizes
GROUP_SIZES = {
    "brown": 2, "lightblue": 3, "pink": 3, "orange": 3,
    "red": 3, "yellow": 3, "green": 3, "blue": 2,
    "railroad": 4, "utility": 2
}

# Space types
SPACE_TYPES = {
    0: 'go',
    2: 'community_chest', 17: 'community_chest', 33: 'community_chest',
    4: 'tax', 38: 'tax',
    7: 'chance', 22: 'chance', 36: 'chance',
    10: 'jail',
    20: 'free_parking',
    30: 'go_to_jail',
    5: 'railroad', 15: 'railroad', 25: 'railroad', 35: 'railroad',
    12: 'utility', 28: 'utility'
}

# Chance cards
CHANCE_CARDS = [
    ("Advance to GO. Collect $200.", "go"),
    ("Advance to Illinois Avenue.", "move_to_24"),
    ("Advance to St. Charles Place.", "move_to_11"),
    ("Advance to nearest Railroad. Pay owner twice normal rent.", "nearest_railroad"),
    ("Advance to nearest Utility. Pay 10x dice roll if owned.", "nearest_utility"),
    ("Bank pays you dividend of $50.", "collect_50"),
    ("Get Out of Jail Free card.", "jail_card"),
    ("Go back 3 spaces.", "back_3"),
    ("Go directly to Jail. Do not pass GO.", "go_to_jail"),
    ("Make general repairs: $25 per house, $100 per hotel.", "repairs_25_100"),
    ("Pay poor tax of $15.", "pay_15"),
    ("Take a trip to Reading Railroad.", "move_to_5"),
    ("Take a walk on the Boardwalk.", "move_to_39"),
    ("You have been elected Chairman of the Board. Pay each player $50.", "pay_each_50"),
    ("Your building loan matures. Collect $150.", "collect_150"),
    ("You have won a crossword competition. Collect $100.", "collect_100")
]

# Community Chest cards
COMMUNITY_CARDS = [
    ("Advance to GO. Collect $200.", "go"),
    ("Bank error in your favor. Collect $200.", "collect_200"),
    ("Doctor's fees. Pay $50.", "pay_50"),
    ("From sale of stock you get $50.", "collect_50"),
    ("Get Out of Jail Free card.", "jail_card"),
    ("Go directly to Jail. Do not pass GO.", "go_to_jail"),
    ("Grand Opera Night. Collect $50 from every player.", "collect_from_each_50"),
    ("Holiday Fund matures. Collect $100.", "collect_100"),
    ("Income tax refund. Collect $20.", "collect_20"),
    ("It's your birthday. Collect $10 from every player.", "collect_from_each_10"),
    ("Life insurance matures. Collect $100.", "collect_100"),
    ("Hospital fees. Pay $100.", "pay_100"),
    ("School fees. Pay $50.", "pay_50"),
    ("Receive $25 consultancy fee.", "collect_25"),
    ("You are assessed for street repairs: $40 per house, $115 per hotel.", "repairs_40_115"),
    ("You have won second prize in a beauty contest. Collect $10.", "collect_10")
]

# AI Names
AI_NAMES = ["RoboBaron", "CashBot", "PropertyPro", "MonopolyMind", "WealthWizard", "DealDroid"]
