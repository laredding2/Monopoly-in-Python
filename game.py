"""
MONOPOLY GUI - Main Game Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import Optional

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, SPACE_NAMES,
    PROPERTY_COLORS, SPACE_TYPES
)
from game_state import GameState
from player import Player
from ai import AIPlayer
from board_widget import BoardWidget
from dialogs import SetupDialog, PropertyDialog, JailDialog, CardDialog


class MonopolyGame(tk.Tk):
    """Main application window for Monopoly."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Monopoly - Python Edition GUI")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=COLORS['panel_bg'])
        self.resizable(True, True)
        
        self.game_state = GameState()
        self.ai_player = None
        self.turn_phase = "idle"
        self.pending_actions = []
        
        self.create_widgets()
        self.center_window()
        
        self.after(100, self.show_setup)
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        main_frame = tk.Frame(self, bg=COLORS['panel_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Board
        left_frame = tk.Frame(main_frame, bg=COLORS['panel_bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.board = BoardWidget(left_frame, self.game_state)
        self.board.pack(padx=10, pady=10)
        
        # Right panel
        right_frame = tk.Frame(main_frame, bg=COLORS['panel_bg'], width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        right_frame.pack_propagate(False)
        
        # Current player info
        self.player_info_frame = tk.LabelFrame(
            right_frame, text="Current Player",
            font=("Arial", 12, "bold"), bg=COLORS['panel_bg']
        )
        self.player_info_frame.pack(fill=tk.X, pady=5)
        
        self.player_name_label = tk.Label(
            self.player_info_frame, text="",
            font=("Arial", 14, "bold"), bg=COLORS['panel_bg']
        )
        self.player_name_label.pack(pady=5)
        
        self.player_money_label = tk.Label(
            self.player_info_frame, text="",
            font=("Arial", 12), bg=COLORS['panel_bg'], fg=COLORS['money_green']
        )
        self.player_money_label.pack(pady=2)
        
        self.player_position_label = tk.Label(
            self.player_info_frame, text="",
            font=("Arial", 10), bg=COLORS['panel_bg']
        )
        self.player_position_label.pack(pady=2)
        
        # Dice display
        self.dice_frame = tk.LabelFrame(
            right_frame, text="Dice",
            font=("Arial", 12, "bold"), bg=COLORS['panel_bg']
        )
        self.dice_frame.pack(fill=tk.X, pady=5)
        
        self.dice_label = tk.Label(
            self.dice_frame, text="🎲  🎲",
            font=("Arial", 32), bg=COLORS['panel_bg']
        )
        self.dice_label.pack(pady=10)
        
        self.dice_result_label = tk.Label(
            self.dice_frame, text="",
            font=("Arial", 12), bg=COLORS['panel_bg']
        )
        self.dice_result_label.pack(pady=5)
        
        # Action buttons
        self.buttons_frame = tk.Frame(right_frame, bg=COLORS['panel_bg'])
        self.buttons_frame.pack(fill=tk.X, pady=10)
        
        self.roll_button = tk.Button(
            self.buttons_frame, text="🎲 Roll Dice",
            font=("Arial", 12, "bold"),
            bg=COLORS['button_bg'], fg=COLORS['text_light'],
            command=self.roll_dice, state=tk.DISABLED
        )
        self.roll_button.pack(fill=tk.X, pady=3)
        
        self.manage_button = tk.Button(
            self.buttons_frame, text="🏠 Manage Properties",
            font=("Arial", 11),
            command=self.show_property_dialog, state=tk.DISABLED
        )
        self.manage_button.pack(fill=tk.X, pady=3)
        
        self.end_turn_button = tk.Button(
            self.buttons_frame, text="✓ End Turn",
            font=("Arial", 11),
            command=self.end_turn, state=tk.DISABLED
        )
        self.end_turn_button.pack(fill=tk.X, pady=3)
        
        # All players list
        self.players_frame = tk.LabelFrame(
            right_frame, text="All Players",
            font=("Arial", 12, "bold"), bg=COLORS['panel_bg']
        )
        self.players_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.players_list = tk.Listbox(
            self.players_frame, font=("Arial", 10), height=8
        )
        self.players_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message log
        self.log_frame = tk.LabelFrame(
            right_frame, text="Game Log",
            font=("Arial", 12, "bold"), bg=COLORS['panel_bg']
        )
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        log_container = tk.Frame(self.log_frame)
        log_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(
            log_container, font=("Arial", 9), height=8,
            wrap=tk.WORD, state=tk.DISABLED
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(log_container, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    
    def show_setup(self):
        dialog = SetupDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            self.start_game(dialog.result)
        else:
            self.destroy()
    
    def start_game(self, config: dict):
        self.ai_player = AIPlayer(config['difficulty'])
        
        for name, is_ai in config['players']:
            self.game_state.add_player(name, is_ai)
        
        self.game_state.game_started = True
        
        self.log_message("🎲 Game Started! 🎲")
        self.log_message(f"Players: {', '.join(p.name for p in self.game_state.players)}")
        self.log_message("")
        
        self.update_display()
        self.start_turn()
    
    def update_display(self):
        self.board.refresh()
        
        player = self.game_state.current_player
        if player:
            ai_tag = " 🤖" if player.is_ai else ""
            self.player_name_label.config(
                text=f"{player.token} {player.name}{ai_tag}",
                fg=player.color
            )
            self.player_money_label.config(text=f"💰 ${player.money}")
            self.player_position_label.config(
                text=f"📍 {SPACE_NAMES[player.position]}"
            )
        
        self.players_list.delete(0, tk.END)
        for p in self.game_state.players:
            status = ""
            if p.bankrupt:
                status = " [BANKRUPT]"
            elif p.in_jail:
                status = " [JAIL]"
            
            ai_tag = " 🤖" if p.is_ai else ""
            current = "► " if p == self.game_state.current_player else "  "
            
            self.players_list.insert(
                tk.END,
                f"{current}{p.token} {p.name}{ai_tag}: ${p.money}{status}"
            )
    
    def log_message(self, message: str):
        self.game_state.log_message(message)
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def start_turn(self):
        player = self.game_state.current_player
        
        if player.bankrupt:
            self.game_state.next_player()
            self.start_turn()
            return
        
        self.game_state.doubles_count = 0
        self.turn_phase = "pre_roll"
        
        ai_tag = " 🤖" if player.is_ai else ""
        self.log_message(f"\n{'='*30}")
        self.log_message(f"{player.token} {player.name}'s Turn{ai_tag}")
        
        self.update_display()
        
        if player.is_ai:
            self.after(500, self.ai_turn)
        else:
            self.enable_player_controls()
    
    def enable_player_controls(self):
        player = self.game_state.current_player
        
        if player.in_jail:
            self.handle_jail()
        else:
            self.roll_button.config(state=tk.NORMAL)
            self.manage_button.config(state=tk.NORMAL)
            self.end_turn_button.config(state=tk.DISABLED)
    
    def disable_all_controls(self):
        self.roll_button.config(state=tk.DISABLED)
        self.manage_button.config(state=tk.DISABLED)
        self.end_turn_button.config(state=tk.DISABLED)
    
    def roll_dice(self):
        self.disable_all_controls()
        player = self.game_state.current_player
        
        dice_faces = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        for i in range(5):
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            self.dice_label.config(text=f"{dice_faces[d1-1]}  {dice_faces[d2-1]}")
            self.update()
            self.after(80)
        
        d1, d2 = self.game_state.roll_dice()
        self.dice_label.config(text=f"{dice_faces[d1-1]}  {dice_faces[d2-1]}")
        
        total = self.game_state.dice_total
        doubles_text = " - DOUBLES!" if self.game_state.is_doubles else ""
        self.dice_result_label.config(text=f"{d1} + {d2} = {total}{doubles_text}")
        
        self.log_message(f"Rolled: {d1} + {d2} = {total}{doubles_text}")
        
        if self.game_state.is_doubles:
            self.game_state.doubles_count += 1
            
            if self.game_state.doubles_count >= 3:
                self.log_message("Three doubles in a row - GO TO JAIL!")
                player.go_to_jail()
                self.update_display()
                self.after(1000, self.end_turn)
                return
        
        self.after(500, lambda: self.move_player(total))
    
    def move_player(self, spaces: int):
        player = self.game_state.current_player
        passed_go = player.move_forward(spaces)
        
        if passed_go:
            self.log_message("Passed GO! Collected $200")
        
        self.log_message(f"Moved to: {SPACE_NAMES[player.position]}")
        self.update_display()
        
        self.after(500, self.handle_landing)
    
    def handle_landing(self):
        player = self.game_state.current_player
        pos = player.position
        prop = self.game_state.properties[pos]
        
        space_type = SPACE_TYPES.get(pos)
        
        if space_type == "go":
            self.log_message("Landed on GO!")
            self.finish_move()
        
        elif space_type == "jail":
            self.log_message("Just visiting jail.")
            self.finish_move()
        
        elif space_type == "free_parking":
            self.log_message("Free Parking - take a rest!")
            self.finish_move()
        
        elif space_type == "go_to_jail":
            self.log_message("GO TO JAIL!")
            player.go_to_jail()
            self.update_display()
            self.after(1000, self.end_turn)
        
        elif space_type == "tax":
            amount = 200 if pos == 4 else 100
            tax_name = "Income Tax" if pos == 4 else "Luxury Tax"
            self.log_message(f"{tax_name}! Pay ${amount}")
            player.subtract_money(amount)
            self.update_display()
            self.check_bankruptcy()
            self.finish_move()
        
        elif space_type == "chance":
            self.draw_card("Chance")
        
        elif space_type == "community_chest":
            self.draw_card("Community Chest")
        
        elif prop.is_property:
            self.handle_property_landing(prop)
        
        else:
            self.finish_move()
    
    def handle_property_landing(self, prop):
        player = self.game_state.current_player
        
        if prop.owner is None:
            if player.is_ai:
                if self.ai_player.decide_buy_property(player, prop.index, self.game_state):
                    self.buy_property(prop)
                else:
                    self.log_message(f"AI decided not to buy {prop.name}")
                    self.finish_move()
            else:
                self.ask_buy_property(prop)
        
        elif prop.owner == player:
            self.log_message("You own this property.")
            self.finish_move()
        
        else:
            self.pay_rent(prop)
    
    def ask_buy_property(self, prop):
        player = self.game_state.current_player
        
        if player.money < prop.price:
            self.log_message(f"Cannot afford {prop.name} (${prop.price})")
            self.finish_move()
            return
        
        result = messagebox.askyesno(
            "Buy Property?",
            f"Would you like to buy {prop.name} for ${prop.price}?\n\n"
            f"Your money: ${player.money}"
        )
        
        if result:
            self.buy_property(prop)
        else:
            self.log_message(f"Declined to buy {prop.name}")
            self.finish_move()
    
    def buy_property(self, prop):
        player = self.game_state.current_player
        player.subtract_money(prop.price)
        prop.owner = player
        player.add_property(prop.index)
        
        self.log_message(f"Bought {prop.name} for ${prop.price}")
        self.update_display()
        self.finish_move()
    
    def pay_rent(self, prop):
        player = self.game_state.current_player
        owner = prop.owner
        
        if prop.mortgaged:
            self.log_message("Property is mortgaged - no rent owed.")
            self.finish_move()
            return
        
        rent = prop.calculate_rent(self.game_state, self.game_state.dice_total)
        
        self.log_message(f"Owes ${rent} rent to {owner.name}")
        
        if player.money >= rent:
            player.subtract_money(rent)
            owner.add_money(rent)
            self.log_message("Rent paid!")
            self.update_display()
            self.finish_move()
        else:
            self.log_message(f"{player.name} cannot afford the rent!")
            player.declare_bankruptcy(self.game_state, owner)
            self.update_display()
            self.check_game_over()
    
    def draw_card(self, card_type: str):
        player = self.game_state.current_player
        
        if card_type == "Chance":
            card_text, action = self.game_state.draw_chance_card()
        else:
            card_text, action = self.game_state.draw_community_card()
        
        self.log_message(f"{card_type}: {card_text}")
        
        if not player.is_ai:
            dialog = CardDialog(self, card_type, card_text)
            self.wait_window(dialog)
        
        self.game_state.execute_card_action(player, action)
        self.update_display()
        
        if action == "go_to_jail":
            self.after(500, self.end_turn)
        elif action in ["go", "back_3"] or action.startswith("move_to_") or action.startswith("nearest_"):
            self.after(500, self.handle_landing)
        else:
            self.check_bankruptcy()
            self.finish_move()
    
    def handle_jail(self):
        player = self.game_state.current_player
        
        if player.is_ai:
            strategy = self.ai_player.decide_jail_strategy(player, self.game_state)
            self.log_message(f"AI in jail, choosing: {strategy}")
            
            if strategy == "card" and player.get_out_of_jail_cards > 0:
                player.get_out_of_jail_cards -= 1
                player.release_from_jail()
                self.log_message("AI used Get Out of Jail Free card!")
                self.after(500, self.roll_dice)
            
            elif strategy == "pay" and player.money >= 50:
                player.subtract_money(50)
                player.release_from_jail()
                self.log_message("AI paid $50 to leave jail")
                self.update_display()
                self.after(500, self.roll_dice)
            
            else:
                self.try_roll_for_doubles()
        
        else:
            dialog = JailDialog(self, player)
            self.wait_window(dialog)
            
            if dialog.result == "pay":
                player.subtract_money(50)
                player.release_from_jail()
                self.log_message("Paid $50 to leave jail")
                self.update_display()
                self.roll_button.config(state=tk.NORMAL)
                self.manage_button.config(state=tk.NORMAL)
            
            elif dialog.result == "card":
                player.get_out_of_jail_cards -= 1
                player.release_from_jail()
                self.log_message("Used Get Out of Jail Free card!")
                self.update_display()
                self.roll_button.config(state=tk.NORMAL)
                self.manage_button.config(state=tk.NORMAL)
            
            else:
                self.try_roll_for_doubles()
    
    def try_roll_for_doubles(self):
        player = self.game_state.current_player
        
        dice_faces = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        for i in range(5):
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            self.dice_label.config(text=f"{dice_faces[d1-1]}  {dice_faces[d2-1]}")
            self.update()
            self.after(80)
        
        d1, d2 = self.game_state.roll_dice()
        self.dice_label.config(text=f"{dice_faces[d1-1]}  {dice_faces[d2-1]}")
        
        total = self.game_state.dice_total
        self.dice_result_label.config(text=f"{d1} + {d2} = {total}")
        self.log_message(f"Rolled for doubles: {d1} + {d2} = {total}")
        
        if self.game_state.is_doubles:
            self.log_message("DOUBLES! Free from jail!")
            player.release_from_jail()
            self.update_display()
            self.after(500, lambda: self.move_player(total))
        else:
            player.jail_turns += 1
            if player.jail_turns >= 3:
                self.log_message("Third turn - must pay $50 to leave")
                player.subtract_money(50)
                player.release_from_jail()
                self.update_display()
                self.after(500, lambda: self.move_player(total))
            else:
                self.log_message("No doubles. Stay in jail.")
                self.update_display()
                self.after(500, self.end_turn)
    
    def finish_move(self):
        player = self.game_state.current_player
        
        if self.game_state.is_doubles and not player.in_jail:
            self.log_message("Roll again (doubles)!")
            if player.is_ai:
                self.after(1000, self.ai_turn)
            else:
                self.roll_button.config(state=tk.NORMAL)
                self.manage_button.config(state=tk.NORMAL)
        else:
            if player.is_ai:
                self.after(500, self.end_turn)
            else:
                self.manage_button.config(state=tk.NORMAL)
                self.end_turn_button.config(state=tk.NORMAL)
    
    def check_bankruptcy(self):
        player = self.game_state.current_player
        if player.money < 0:
            self.log_message(f"{player.name} is bankrupt!")
            player.declare_bankruptcy(self.game_state)
            self.update_display()
            self.check_game_over()
    
    def check_game_over(self):
        winner = self.game_state.check_winner()
        if winner:
            self.log_message(f"\n{'='*30}")
            self.log_message(f"🎉 GAME OVER! 🎉")
            self.log_message(f"{winner.token} {winner.name} WINS!")
            self.log_message(f"Final wealth: ${winner.money}")
            
            messagebox.showinfo(
                "Game Over!",
                f"🎉 {winner.name} WINS! 🎉\n\nFinal wealth: ${winner.money}"
            )
            
            self.disable_all_controls()
            return True
        return False
    
    def end_turn(self):
        self.disable_all_controls()
        
        if self.check_game_over():
            return
        
        self.game_state.next_player()
        self.after(500, self.start_turn)
    
    def show_property_dialog(self):
        player = self.game_state.current_player
        dialog = PropertyDialog(self, self.game_state, player)
        self.wait_window(dialog)
        self.update_display()
    
    def ai_turn(self):
        player = self.game_state.current_player
        
        if player.in_jail:
            self.handle_jail()
            return
        
        # AI pre-roll actions
        actions = self.ai_player.get_all_actions(player, self.game_state)
        
        for action_type, prop_idx in actions:
            prop = self.game_state.properties[prop_idx]
            
            if action_type == "build":
                if player.money >= prop.house_price:
                    player.subtract_money(prop.house_price)
                    prop.houses += 1
                    building = "hotel" if prop.houses == 5 else "house"
                    self.log_message(f"AI built a {building} on {prop.name}")
                    self.update_display()
                    self.after(300)
            
            elif action_type == "unmortgage":
                if player.money >= prop.unmortgage_cost:
                    cost = prop.unmortgage()
                    player.subtract_money(cost)
                    self.log_message(f"AI unmortgaged {prop.name}")
                    self.update_display()
                    self.after(300)
        
        self.after(500, self.roll_dice)


def main():
    app = MonopolyGame()
    app.mainloop()


if __name__ == "__main__":
    main()
