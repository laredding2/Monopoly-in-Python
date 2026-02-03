# Monopoly GUI - Python  Edition

A complete Monopoly game with a graphical user interface built in Python using Tkinter.

![Monopoly](https://img.shields.io/badge/Game-Monopoly-red)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

## Features

### Gameplay
- **Full 40-space board** with all classic Monopoly properties
- **2-6 players** - mix of human and AI opponents
- **Property trading** - buy properties, collect rent
- **Build houses and hotels** on your monopolies
- **Chance and Community Chest cards** with all classic effects
- **Jail mechanics** - pay, use card, or roll for doubles
- **Mortgage system** to raise funds when low on cash

### AI Opponents
- **Three difficulty levels:**
  - **Easy** - Makes random decisions, good for beginners
  - **Medium** - Reasonable strategy, balanced gameplay
  - **Hard** - Optimal decision-making, challenging opponent

- **AI Strategy includes:**
  - Smart property evaluation (monopoly potential, blocking opponents)
  - Strategic house building (even distribution, ROI consideration)
  - Intelligent mortgage decisions (least valuable properties first)
  - Jail strategy based on game state

### Visual Interface
- **Colorful game board** with property colors and ownership indicators
- **Animated dice rolls**
- **Player tokens** with unique colors
- **Real-time game log**
- **Property management dialogs**

## Requirements

- Python 3.7 or higher
- Tkinter (usually included with Python)

## Installation

1. Clone or download the `monopoly-gui` directory
2. No additional dependencies required!

## Running the Game

```bash
cd monopoly-gui
python monopoly.py
```

Or:

```bash
python3 monopoly.py
```

## File Structure

```
monopoly-gui/
├── monopoly.py      # Main launcher
├── game.py          # Main game window and logic
├── config.py        # Game constants and configuration
├── player.py        # Player class
├── property.py      # Property class
├── game_state.py    # Game state manager
├── ai.py            # AI decision-making logic
├── board_widget.py  # Board rendering
├── dialogs.py       # Dialog windows (setup, property management, etc.)
└── README.md        # This file
```

## How to Play

1. **Start the game** - Run `python monopoly.py`
2. **Setup** - Choose Quick Start or Custom Game
   - Quick Start: Enter your name and select number of AI opponents
   - Custom: Configure each player (human/AI)
3. **Select AI difficulty** - Easy, Medium, or Hard
4. **Play!**
   - Click "Roll Dice" to move
   - Buy properties when you land on them
   - Use "Manage Properties" to build houses or mortgage
   - Click "End Turn" when finished

## Game Rules

- Each player starts with $1,500
- Pass GO to collect $200
- Buy properties to collect rent from other players
- Own all properties in a color group to get a monopoly
- Build houses (then hotels) on monopolies to increase rent
- If you can't pay, mortgage properties or go bankrupt
- Last player standing wins!

## Screenshots

The game features:
- A visual game board with all 40 spaces
- Color-coded properties with ownership indicators
- Player tokens positioned on the board
- Dice display with roll animation
- Player status panel
- Game action log

## License

This is a fan-made implementation of the classic Monopoly board game for educational purposes.

Monopoly® is a trademark of Hasbro, Inc.
