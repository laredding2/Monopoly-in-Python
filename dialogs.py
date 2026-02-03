"""
MONOPOLY GUI - Dialog Windows
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, SPACE_NAMES, AI_NAMES, TOKENS, TOKEN_NAMES


class SetupDialog(tk.Toplevel):
    """Dialog for game setup."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Game Setup")
        self.geometry("500x600")
        self.resizable(False, False)
        self.configure(bg=COLORS['panel_bg'])
        
        self.result = None
        self.player_entries = []
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        # Title
        title = tk.Label(
            self, text="🎲 MONOPOLY Setup 🎲",
            font=("Arial", 20, "bold"),
            bg=COLORS['panel_bg'],
            fg=COLORS['text_dark']
        )
        title.pack(pady=20)
        
        # Mode selection
        mode_frame = tk.LabelFrame(
            self, text="Game Mode",
            font=("Arial", 12, "bold"),
            bg=COLORS['panel_bg']
        )
        mode_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.mode_var = tk.StringVar(value="quick")
        
        tk.Radiobutton(
            mode_frame, text="Quick Start (1 Human vs AI)",
            variable=self.mode_var, value="quick",
            bg=COLORS['panel_bg'],
            command=self.update_player_frame
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Radiobutton(
            mode_frame, text="Watch Mode (All AI)",
            variable=self.mode_var, value="all_ai",
            bg=COLORS['panel_bg'],
            command=self.update_player_frame
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Radiobutton(
            mode_frame, text="Custom Game",
            variable=self.mode_var, value="custom",
            bg=COLORS['panel_bg'],
            command=self.update_player_frame
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Player configuration frame
        self.player_frame = tk.LabelFrame(
            self, text="Players",
            font=("Arial", 12, "bold"),
            bg=COLORS['panel_bg']
        )
        self.player_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # AI Difficulty
        diff_frame = tk.LabelFrame(
            self, text="AI Difficulty",
            font=("Arial", 12, "bold"),
            bg=COLORS['panel_bg']
        )
        diff_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.difficulty_var = tk.IntVar(value=2)
        
        for val, text in [(1, "Easy"), (2, "Medium"), (3, "Hard")]:
            tk.Radiobutton(
                diff_frame, text=text,
                variable=self.difficulty_var, value=val,
                bg=COLORS['panel_bg']
            ).pack(side=tk.LEFT, padx=20, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self, bg=COLORS['panel_bg'])
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            btn_frame, text="Start Game",
            font=("Arial", 12, "bold"),
            bg=COLORS['button_bg'],
            fg=COLORS['text_light'],
            command=self.on_start
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            btn_frame, text="Cancel",
            font=("Arial", 12),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        self.update_player_frame()
    
    def update_player_frame(self):
        # Clear existing widgets
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        self.player_entries = []
        
        if self.mode_var.get() == "quick":
            # Quick start - just name and AI count
            row = tk.Frame(self.player_frame, bg=COLORS['panel_bg'])
            row.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(row, text="Your Name:", bg=COLORS['panel_bg']).pack(side=tk.LEFT)
            name_entry = tk.Entry(row, width=20)
            name_entry.insert(0, "Player")
            name_entry.pack(side=tk.LEFT, padx=10)
            self.player_entries.append(('human', name_entry))
            
            row2 = tk.Frame(self.player_frame, bg=COLORS['panel_bg'])
            row2.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(row2, text="AI Opponents:", bg=COLORS['panel_bg']).pack(side=tk.LEFT)
            self.ai_count_var = tk.IntVar(value=3)
            ai_spin = tk.Spinbox(row2, from_=1, to=5, width=5, textvariable=self.ai_count_var)
            ai_spin.pack(side=tk.LEFT, padx=10)
        
        elif self.mode_var.get() == "all_ai":
            # All AI mode - just select number of AI players
            row = tk.Frame(self.player_frame, bg=COLORS['panel_bg'])
            row.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(row, text="Number of AI Players:", bg=COLORS['panel_bg']).pack(side=tk.LEFT)
            self.all_ai_count_var = tk.IntVar(value=4)
            ai_spin = tk.Spinbox(row, from_=2, to=6, width=5, textvariable=self.all_ai_count_var)
            ai_spin.pack(side=tk.LEFT, padx=10)
            
            info_label = tk.Label(
                self.player_frame, 
                text="🤖 Watch Mode: All players are AI.\nSit back and watch them play!",
                bg=COLORS['panel_bg'],
                fg="#666666",
                font=("Arial", 9, "italic")
            )
            info_label.pack(pady=10)
        
        else:
            # Custom game
            row = tk.Frame(self.player_frame, bg=COLORS['panel_bg'])
            row.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(row, text="Number of Players:", bg=COLORS['panel_bg']).pack(side=tk.LEFT)
            self.num_players_var = tk.IntVar(value=4)
            num_spin = tk.Spinbox(
                row, from_=2, to=6, width=5, 
                textvariable=self.num_players_var,
                command=self.create_player_rows
            )
            num_spin.pack(side=tk.LEFT, padx=10)
            num_spin.bind('<Return>', lambda e: self.create_player_rows())
            
            tk.Button(row, text="Update", command=self.create_player_rows).pack(side=tk.LEFT)
            
            # Player rows container
            self.rows_frame = tk.Frame(self.player_frame, bg=COLORS['panel_bg'])
            self.rows_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            self.create_player_rows()
    
    def create_player_rows(self):
        if not hasattr(self, 'rows_frame'):
            return
        
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        self.player_entries = []
        
        num = self.num_players_var.get()
        
        for i in range(num):
            row = tk.Frame(self.rows_frame, bg=COLORS['panel_bg'])
            row.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(
                row, text=f"{TOKENS[i]} Player {i+1}:",
                bg=COLORS['panel_bg'],
                width=12
            ).pack(side=tk.LEFT)
            
            name_entry = tk.Entry(row, width=15)
            name_entry.insert(0, f"Player {i+1}" if i == 0 else AI_NAMES[i-1])
            name_entry.pack(side=tk.LEFT, padx=5)
            
            is_ai_var = tk.BooleanVar(value=(i > 0))
            ai_check = tk.Checkbutton(
                row, text="AI",
                variable=is_ai_var,
                bg=COLORS['panel_bg']
            )
            ai_check.pack(side=tk.LEFT, padx=5)
            
            self.player_entries.append((name_entry, is_ai_var))
    
    def on_start(self):
        players = []
        
        if self.mode_var.get() == "quick":
            # Human player
            name = self.player_entries[0][1].get().strip() or "Player"
            players.append((name, False))
            
            # AI players
            ai_count = self.ai_count_var.get()
            for i in range(ai_count):
                players.append((AI_NAMES[i], True))
        
        elif self.mode_var.get() == "all_ai":
            # All AI players
            ai_count = self.all_ai_count_var.get()
            for i in range(ai_count):
                players.append((AI_NAMES[i], True))
        
        else:
            # Custom game
            for name_entry, is_ai_var in self.player_entries:
                name = name_entry.get().strip() or "Player"
                players.append((name, is_ai_var.get()))
        
        self.result = {
            'players': players,
            'difficulty': self.difficulty_var.get()
        }
        self.destroy()


class PropertyDialog(tk.Toplevel):
    """Dialog for property actions (buy, mortgage, etc.)."""
    
    def __init__(self, parent, game_state, player, action_type="manage"):
        super().__init__(parent)
        self.game_state = game_state
        self.player = player
        self.action_type = action_type
        self.result = None
        
        self.title(f"Property Management - {player.name}")
        self.geometry("400x500")
        self.configure(bg=COLORS['panel_bg'])
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        # Money display
        money_label = tk.Label(
            self, text=f"Money: ${self.player.money}",
            font=("Arial", 14, "bold"),
            bg=COLORS['panel_bg'],
            fg=COLORS['money_green']
        )
        money_label.pack(pady=10)
        
        # Tab notebook for different actions
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Build tab
        build_frame = tk.Frame(notebook, bg=COLORS['panel_bg'])
        notebook.add(build_frame, text="Build Houses")
        self.create_build_tab(build_frame)
        
        # Mortgage tab
        mortgage_frame = tk.Frame(notebook, bg=COLORS['panel_bg'])
        notebook.add(mortgage_frame, text="Mortgage")
        self.create_mortgage_tab(mortgage_frame)
        
        # Unmortgage tab
        unmortgage_frame = tk.Frame(notebook, bg=COLORS['panel_bg'])
        notebook.add(unmortgage_frame, text="Unmortgage")
        self.create_unmortgage_tab(unmortgage_frame)
        
        # Close button
        tk.Button(
            self, text="Close",
            font=("Arial", 12),
            command=self.destroy
        ).pack(pady=10)
    
    def create_build_tab(self, parent):
        tk.Label(
            parent, text="Select a property to build on:",
            font=("Arial", 10),
            bg=COLORS['panel_bg']
        ).pack(pady=5)
        
        listbox = tk.Listbox(parent, height=12, width=40)
        listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        buildable = []
        for prop_idx in self.player.properties:
            prop = self.game_state.properties[prop_idx]
            if prop.can_build(self.game_state):
                houses = "Hotel" if prop.houses == 4 else f"{prop.houses} houses"
                listbox.insert(tk.END, f"{prop.name} ({houses}) - ${prop.house_price}")
                buildable.append(prop_idx)
        
        if not buildable:
            listbox.insert(tk.END, "No properties available for building")
            listbox.insert(tk.END, "(Need complete color group)")
        
        def on_build():
            sel = listbox.curselection()
            if sel and buildable:
                idx = buildable[sel[0]]
                prop = self.game_state.properties[idx]
                if self.player.money >= prop.house_price:
                    self.player.subtract_money(prop.house_price)
                    prop.houses += 1
                    self.result = ("build", idx)
                    self.destroy()
                else:
                    messagebox.showwarning("Insufficient Funds", "Not enough money!")
        
        tk.Button(
            parent, text="Build",
            command=on_build,
            bg=COLORS['button_bg'],
            fg=COLORS['text_light']
        ).pack(pady=5)
    
    def create_mortgage_tab(self, parent):
        tk.Label(
            parent, text="Select a property to mortgage:",
            font=("Arial", 10),
            bg=COLORS['panel_bg']
        ).pack(pady=5)
        
        listbox = tk.Listbox(parent, height=12, width=40)
        listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        mortgageable = []
        for prop_idx in self.player.properties:
            prop = self.game_state.properties[prop_idx]
            if not prop.mortgaged and prop.houses == 0:
                listbox.insert(tk.END, f"{prop.name} - Value: ${prop.mortgage_value}")
                mortgageable.append(prop_idx)
        
        if not mortgageable:
            listbox.insert(tk.END, "No properties available to mortgage")
            listbox.insert(tk.END, "(Sell houses first)")
        
        def on_mortgage():
            sel = listbox.curselection()
            if sel and mortgageable:
                idx = mortgageable[sel[0]]
                prop = self.game_state.properties[idx]
                value = prop.mortgage()
                self.player.add_money(value)
                self.result = ("mortgage", idx)
                self.destroy()
        
        tk.Button(
            parent, text="Mortgage",
            command=on_mortgage,
            bg="#FF9800",
            fg=COLORS['text_light']
        ).pack(pady=5)
    
    def create_unmortgage_tab(self, parent):
        tk.Label(
            parent, text="Select a property to unmortgage:",
            font=("Arial", 10),
            bg=COLORS['panel_bg']
        ).pack(pady=5)
        
        listbox = tk.Listbox(parent, height=12, width=40)
        listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        unmortgageable = []
        for prop_idx in self.player.properties:
            prop = self.game_state.properties[prop_idx]
            if prop.mortgaged:
                listbox.insert(tk.END, f"{prop.name} - Cost: ${prop.unmortgage_cost}")
                unmortgageable.append(prop_idx)
        
        if not unmortgageable:
            listbox.insert(tk.END, "No mortgaged properties")
        
        def on_unmortgage():
            sel = listbox.curselection()
            if sel and unmortgageable:
                idx = unmortgageable[sel[0]]
                prop = self.game_state.properties[idx]
                if self.player.money >= prop.unmortgage_cost:
                    cost = prop.unmortgage()
                    self.player.subtract_money(cost)
                    self.result = ("unmortgage", idx)
                    self.destroy()
                else:
                    messagebox.showwarning("Insufficient Funds", "Not enough money!")
        
        tk.Button(
            parent, text="Unmortgage",
            command=on_unmortgage,
            bg=COLORS['button_bg'],
            fg=COLORS['text_light']
        ).pack(pady=5)


class JailDialog(tk.Toplevel):
    """Dialog for jail options."""
    
    def __init__(self, parent, player):
        super().__init__(parent)
        self.player = player
        self.result = None
        
        self.title("You're in Jail!")
        self.geometry("350x250")
        self.configure(bg=COLORS['panel_bg'])
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        tk.Label(
            self, text="🔒 You are in JAIL! 🔒",
            font=("Arial", 16, "bold"),
            bg=COLORS['panel_bg'],
            fg=COLORS['warning_red']
        ).pack(pady=20)
        
        tk.Label(
            self, text=f"Money: ${self.player.money}",
            font=("Arial", 12),
            bg=COLORS['panel_bg']
        ).pack(pady=5)
        
        if self.player.get_out_of_jail_cards > 0:
            tk.Label(
                self, text=f"Get Out of Jail Free Cards: {self.player.get_out_of_jail_cards}",
                font=("Arial", 12),
                bg=COLORS['panel_bg']
            ).pack(pady=5)
        
        btn_frame = tk.Frame(self, bg=COLORS['panel_bg'])
        btn_frame.pack(pady=20)
        
        # Pay $50
        pay_btn = tk.Button(
            btn_frame, text="Pay $50",
            font=("Arial", 11),
            command=lambda: self.select("pay"),
            state=tk.NORMAL if self.player.money >= 50 else tk.DISABLED
        )
        pay_btn.pack(fill=tk.X, pady=3)
        
        # Use card
        if self.player.get_out_of_jail_cards > 0:
            tk.Button(
                btn_frame, text="Use Get Out of Jail Free Card",
                font=("Arial", 11),
                command=lambda: self.select("card")
            ).pack(fill=tk.X, pady=3)
        
        # Roll for doubles
        tk.Button(
            btn_frame, text="Roll for Doubles",
            font=("Arial", 11),
            command=lambda: self.select("roll")
        ).pack(fill=tk.X, pady=3)
    
    def select(self, choice):
        self.result = choice
        self.destroy()


class CardDialog(tk.Toplevel):
    """Dialog to show a drawn card."""
    
    def __init__(self, parent, card_type: str, card_text: str):
        super().__init__(parent)
        self.title(card_type)
        self.geometry("400x200")
        
        bg_color = COLORS['chance'] if card_type == "Chance" else COLORS['community_chest']
        self.configure(bg=bg_color)
        
        self.transient(parent)
        self.grab_set()
        
        tk.Label(
            self, text=f"🎴 {card_type} 🎴",
            font=("Arial", 18, "bold"),
            bg=bg_color
        ).pack(pady=20)
        
        tk.Label(
            self, text=card_text,
            font=("Arial", 12),
            bg=bg_color,
            wraplength=350,
            justify=tk.CENTER
        ).pack(pady=10)
        
        tk.Button(
            self, text="OK",
            font=("Arial", 12),
            command=self.destroy
        ).pack(pady=20)
        
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
