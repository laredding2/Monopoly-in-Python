"""
MONOPOLY GUI - Board Widget
"""

import tkinter as tk
from tkinter import font as tkfont
from config import (
    BOARD_SIZE, CELL_SIZE, COLORS, SPACE_SHORT_NAMES,
    PROPERTY_COLORS, SPACE_TYPES
)


class BoardWidget(tk.Canvas):
    """Canvas widget that draws the Monopoly board."""
    
    def __init__(self, parent, game_state, **kwargs):
        super().__init__(parent, width=BOARD_SIZE, height=BOARD_SIZE, 
                        bg=COLORS['board_bg'], **kwargs)
        self.game_state = game_state
        self.cell_size = CELL_SIZE
        self.corner_size = CELL_SIZE * 1.3
        
        # Fonts
        self.name_font = tkfont.Font(family="Arial", size=7, weight="bold")
        self.price_font = tkfont.Font(family="Arial", size=6)
        self.token_font = tkfont.Font(family="Arial", size=14)
        self.corner_font = tkfont.Font(family="Arial", size=9, weight="bold")
        
        self.draw_board()
    
    def get_cell_position(self, space_index: int) -> tuple:
        """Get the x, y coordinates for a board space."""
        # Bottom row (0-10): right to left
        if space_index <= 10:
            x = BOARD_SIZE - self.corner_size - (space_index * self.cell_size)
            if space_index == 0:
                x = BOARD_SIZE - self.corner_size
            elif space_index == 10:
                x = 0
            else:
                x = BOARD_SIZE - self.corner_size - ((space_index) * self.cell_size)
            y = BOARD_SIZE - self.corner_size
            return (x, y)
        
        # Left column (11-20): bottom to top
        elif space_index <= 20:
            x = 0
            idx = space_index - 10
            if space_index == 20:
                y = 0
            else:
                y = BOARD_SIZE - self.corner_size - (idx * self.cell_size)
            return (x, y)
        
        # Top row (21-30): left to right
        elif space_index <= 30:
            idx = space_index - 20
            if space_index == 30:
                x = BOARD_SIZE - self.corner_size
            else:
                x = self.corner_size + ((idx - 1) * self.cell_size)
            y = 0
            return (x, y)
        
        # Right column (31-39): top to bottom
        else:
            idx = space_index - 30
            x = BOARD_SIZE - self.corner_size
            y = self.corner_size + ((idx - 1) * self.cell_size)
            return (x, y)
    
    def get_cell_size(self, space_index: int) -> tuple:
        """Get the width and height for a board space."""
        if space_index in [0, 10, 20, 30]:
            return (self.corner_size, self.corner_size)
        elif space_index < 10 or (20 < space_index < 30):
            return (self.cell_size, self.corner_size)
        else:
            return (self.corner_size, self.cell_size)
    
    def draw_board(self):
        """Draw the complete board."""
        self.delete("all")
        
        # Draw center
        center_x = BOARD_SIZE // 2
        center_y = BOARD_SIZE // 2
        center_size = BOARD_SIZE - 2 * self.corner_size
        
        self.create_rectangle(
            self.corner_size, self.corner_size,
            BOARD_SIZE - self.corner_size, BOARD_SIZE - self.corner_size,
            fill=COLORS['board_bg'], outline=""
        )
        
        # Draw "MONOPOLY" text in center
        self.create_text(
            center_x, center_y - 30,
            text="MONOPOLY",
            font=tkfont.Font(family="Arial", size=28, weight="bold"),
            fill="#C62828"
        )
        
        self.create_text(
            center_x, center_y + 10,
            text="Python Edition",
            font=tkfont.Font(family="Arial", size=14),
            fill="#424242"
        )
        
        # Draw all spaces
        for i in range(40):
            self.draw_space(i)
        
        # Draw player tokens
        self.draw_players()
    
    def draw_space(self, index: int):
        """Draw a single board space."""
        x, y = self.get_cell_position(index)
        w, h = self.get_cell_size(index)
        
        # Determine background color
        space_type = SPACE_TYPES.get(index)
        prop_color = PROPERTY_COLORS[index]
        
        if space_type:
            bg_color = COLORS.get(space_type, COLORS['cell_bg'])
        elif prop_color:
            bg_color = COLORS['cell_bg']
        else:
            bg_color = COLORS['cell_bg']
        
        # Draw cell background
        self.create_rectangle(x, y, x + w, y + h, fill=bg_color, outline="#333333", width=1)
        
        # Draw color bar for properties
        if prop_color and prop_color not in ['railroad', 'utility']:
            bar_color = COLORS.get(prop_color, "#CCCCCC")
            bar_height = 12
            
            if index < 10:  # Bottom row
                self.create_rectangle(x, y, x + w, y + bar_height, fill=bar_color, outline="")
            elif index < 20:  # Left column
                self.create_rectangle(x + w - bar_height, y, x + w, y + h, fill=bar_color, outline="")
            elif index < 30:  # Top row
                self.create_rectangle(x, y + h - bar_height, x + w, y + h, fill=bar_color, outline="")
            else:  # Right column
                self.create_rectangle(x, y, x + bar_height, y + h, fill=bar_color, outline="")
        
        # Draw space name
        name = SPACE_SHORT_NAMES[index]
        
        if index in [0, 10, 20, 30]:
            # Corner spaces
            self.create_text(
                x + w/2, y + h/2,
                text=name,
                font=self.corner_font,
                fill="#333333",
                justify=tk.CENTER
            )
        else:
            # Regular spaces
            text_x = x + w/2
            text_y = y + h/2
            
            self.create_text(
                text_x, text_y - 5,
                text=name,
                font=self.name_font,
                fill="#333333",
                justify=tk.CENTER,
                width=w - 4
            )
            
            # Draw price if property
            prop = self.game_state.properties[index]
            if prop.price > 0:
                self.create_text(
                    text_x, text_y + 18,
                    text=f"${prop.price}",
                    font=self.price_font,
                    fill="#666666"
                )
        
        # Draw ownership indicator
        prop = self.game_state.properties[index]
        if prop.owner:
            owner_color = prop.owner.color
            # Draw small ownership dot
            dot_x = x + w - 8
            dot_y = y + h - 8
            self.create_oval(
                dot_x - 5, dot_y - 5, dot_x + 5, dot_y + 5,
                fill=owner_color, outline="#333333"
            )
            
            # Draw houses
            if prop.houses > 0:
                self.draw_houses(index, prop.houses)
    
    def draw_houses(self, index: int, count: int):
        """Draw houses or hotel on a property."""
        x, y = self.get_cell_position(index)
        w, h = self.get_cell_size(index)
        
        if count == 5:  # Hotel
            # Draw hotel (red rectangle)
            if index < 10:
                hx, hy = x + w/2 - 8, y + 15
            elif index < 20:
                hx, hy = x + w - 20, y + h/2 - 5
            elif index < 30:
                hx, hy = x + w/2 - 8, y + h - 25
            else:
                hx, hy = x + 8, y + h/2 - 5
            
            self.create_rectangle(hx, hy, hx + 16, hy + 10, fill="#C62828", outline="#333")
        else:
            # Draw houses (green squares)
            house_size = 6
            spacing = 8
            
            if index < 10:
                start_x = x + (w - count * spacing) / 2
                for i in range(count):
                    hx = start_x + i * spacing
                    hy = y + 15
                    self.create_rectangle(hx, hy, hx + house_size, hy + house_size, 
                                        fill="#2E7D32", outline="#333")
            elif index < 20:
                start_y = y + (h - count * spacing) / 2
                for i in range(count):
                    hx = x + w - 18
                    hy = start_y + i * spacing
                    self.create_rectangle(hx, hy, hx + house_size, hy + house_size,
                                        fill="#2E7D32", outline="#333")
            elif index < 30:
                start_x = x + (w - count * spacing) / 2
                for i in range(count):
                    hx = start_x + i * spacing
                    hy = y + h - 22
                    self.create_rectangle(hx, hy, hx + house_size, hy + house_size,
                                        fill="#2E7D32", outline="#333")
            else:
                start_y = y + (h - count * spacing) / 2
                for i in range(count):
                    hx = x + 10
                    hy = start_y + i * spacing
                    self.create_rectangle(hx, hy, hx + house_size, hy + house_size,
                                        fill="#2E7D32", outline="#333")
    
    def draw_players(self):
        """Draw all player tokens on the board."""
        # Group players by position
        positions = {}
        for player in self.game_state.players:
            if player.bankrupt:
                continue
            if player.position not in positions:
                positions[player.position] = []
            positions[player.position].append(player)
        
        # Draw tokens at each position
        for pos, players in positions.items():
            x, y = self.get_cell_position(pos)
            w, h = self.get_cell_size(pos)
            
            center_x = x + w / 2
            center_y = y + h / 2
            
            # Offset multiple players
            offsets = [
                (0, 0), (-12, -12), (12, -12), (-12, 12), (12, 12), (0, -15)
            ]
            
            for i, player in enumerate(players):
                ox, oy = offsets[i % len(offsets)]
                
                # Draw token background circle
                self.create_oval(
                    center_x + ox - 12, center_y + oy - 12,
                    center_x + ox + 12, center_y + oy + 12,
                    fill=player.color, outline="#333333", width=2
                )
                
                # Draw token emoji
                self.create_text(
                    center_x + ox, center_y + oy,
                    text=player.token,
                    font=self.token_font
                )
    
    def refresh(self):
        """Refresh the board display."""
        self.draw_board()
