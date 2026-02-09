"""
Main game logic and UI for the number sequence speed test.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math
from typing import List, Tuple
from database import GameDatabase


class Circle:
    """Represents a numbered circle in the game."""
    
    def __init__(self, x: int, y: int, number: int, radius: int = 30):
        self.x = x
        self.y = y
        self.number = number
        self.radius = radius
        self.clicked = False
        self.canvas_id = None
        self.text_id = None
    
    def contains_point(self, px: int, py: int) -> bool:
        """Check if a point is inside this circle."""
        distance = math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2)
        return distance <= self.radius
    
    def overlaps_with(self, other: 'Circle') -> bool:
        """Check if this circle overlaps with another circle."""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < (self.radius + other.radius + 10)  # 10px padding


class NumberSequenceGame:
    """Main game class handling UI and game logic."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Number Sequence Speed Test")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        self.db = GameDatabase()
        
        # Game state
        self.circles: List[Circle] = []
        self.current_number = 1
        self.start_time = None
        self.game_active = False
        self.player_name = ""
        self.numbers_count = 10
        
        # Canvas settings
        self.canvas_width = 800
        self.canvas_height = 500
        self.circle_radius = 30
        
        # Colors
        self.circle_color = "#3498db"
        self.clicked_color = "#2ecc71"
        self.text_color = "white"
        
        # UI elements
        self.main_frame = None
        self.canvas = None
        self.timer_label = None
        self.hint_label = None
        
        self.show_start_screen()
    
    def show_start_screen(self):
        """Display the start screen with options and leaderboard."""
        self.clear_screen()
        
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Number Sequence Speed Test",
            font=("Arial", 24, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.main_frame,
            text="Click the circles in numerical order as fast as you can!",
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#34495e"
        )
        instructions.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        input_frame.pack(pady=20)
        
        # Player name input
        tk.Label(
            input_frame,
            text="Player Name:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        name_entry = tk.Entry(input_frame, font=("Arial", 11), width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, "Player")
        
        # Number of circles selection
        tk.Label(
            input_frame,
            text="Number of Circles:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        numbers_var = tk.StringVar(value="10")
        numbers_combo = ttk.Combobox(
            input_frame,
            textvariable=numbers_var,
            values=["5", "10", "15", "20"],
            state="readonly",
            width=18,
            font=("Arial", 11)
        )
        numbers_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Start button
        def start_game():
            self.player_name = name_entry.get().strip() or "Player"
            self.numbers_count = int(numbers_var.get())
            self.show_game_screen()
        
        start_button = tk.Button(
            self.main_frame,
            text="Start Game",
            font=("Arial", 16, "bold"),
            bg="#27ae60",
            fg="white",
            command=start_game,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        start_button.pack(pady=20)
        
        # Leaderboard
        self.show_leaderboard_on_start()
    
    def show_leaderboard_on_start(self):
        """Display leaderboard on the start screen."""
        leaderboard_frame = tk.LabelFrame(
            self.main_frame,
            text="🏆 Top 10 Fastest Times",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        leaderboard_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Create a frame with scrollbar for leaderboard
        canvas_frame = tk.Frame(leaderboard_frame, bg="#ecf0f1")
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        leaderboard = self.db.get_leaderboard(limit=10)
        
        if leaderboard:
            # Headers
            headers_frame = tk.Frame(canvas_frame, bg="#ecf0f1")
            headers_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(headers_frame, text="Rank", font=("Arial", 10, "bold"), 
                    bg="#ecf0f1", width=6).pack(side=tk.LEFT)
            tk.Label(headers_frame, text="Player", font=("Arial", 10, "bold"), 
                    bg="#ecf0f1", width=15).pack(side=tk.LEFT)
            tk.Label(headers_frame, text="Time", font=("Arial", 10, "bold"), 
                    bg="#ecf0f1", width=10).pack(side=tk.LEFT)
            tk.Label(headers_frame, text="Circles", font=("Arial", 10, "bold"), 
                    bg="#ecf0f1", width=8).pack(side=tk.LEFT)
            tk.Label(headers_frame, text="Date", font=("Arial", 10, "bold"), 
                    bg="#ecf0f1", width=18).pack(side=tk.LEFT)
            
            # Leaderboard entries
            for idx, (name, time_sec, num_circles, timestamp) in enumerate(leaderboard, 1):
                entry_frame = tk.Frame(canvas_frame, bg="white", relief=tk.RAISED, bd=1)
                entry_frame.pack(fill=tk.X, pady=2)
                
                tk.Label(entry_frame, text=f"#{idx}", font=("Arial", 10), 
                        bg="white", width=6).pack(side=tk.LEFT)
                tk.Label(entry_frame, text=name, font=("Arial", 10), 
                        bg="white", width=15, anchor="w").pack(side=tk.LEFT)
                tk.Label(entry_frame, text=f"{time_sec:.2f}s", font=("Arial", 10), 
                        bg="white", width=10).pack(side=tk.LEFT)
                tk.Label(entry_frame, text=str(num_circles), font=("Arial", 10), 
                        bg="white", width=8).pack(side=tk.LEFT)
                
                # Format timestamp
                timestamp_str = timestamp.split('.')[0] if '.' in timestamp else timestamp
                tk.Label(entry_frame, text=timestamp_str, font=("Arial", 9), 
                        bg="white", width=18).pack(side=tk.LEFT)
        else:
            tk.Label(
                canvas_frame,
                text="No records yet. Be the first!",
                font=("Arial", 11, "italic"),
                bg="#ecf0f1",
                fg="#7f8c8d"
            ).pack(pady=20)
    
    def show_game_screen(self):
        """Display the main game screen."""
        self.clear_screen()
        
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top info bar
        info_frame = tk.Frame(self.main_frame, bg="#34495e", height=60)
        info_frame.pack(fill=tk.X)
        info_frame.pack_propagate(False)
        
        # Player info
        player_label = tk.Label(
            info_frame,
            text=f"Player: {self.player_name}",
            font=("Arial", 12),
            bg="#34495e",
            fg="white"
        )
        player_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Timer
        self.timer_label = tk.Label(
            info_frame,
            text="Time: 0.00s",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#f39c12"
        )
        self.timer_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Hint
        self.hint_label = tk.Label(
            info_frame,
            text=f"Next: {self.current_number}",
            font=("Arial", 12),
            bg="#34495e",
            fg="#2ecc71"
        )
        self.hint_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Canvas for game
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#ecf0f1",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Bottom frame with quit button
        bottom_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        bottom_frame.pack(pady=10)
        
        quit_button = tk.Button(
            bottom_frame,
            text="Quit to Menu",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            command=self.quit_to_menu,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        quit_button.pack()
        
        # Initialize game
        self.initialize_game()
    
    def initialize_game(self):
        """Set up the game with random circle positions."""
        self.circles = []
        self.current_number = 1
        self.game_active = True
        self.start_time = time.time()
        
        # Generate circles with random positions
        for i in range(1, self.numbers_count + 1):
            max_attempts = 100
            for attempt in range(max_attempts):
                x = random.randint(self.circle_radius + 10, 
                                 self.canvas_width - self.circle_radius - 10)
                y = random.randint(self.circle_radius + 10, 
                                 self.canvas_height - self.circle_radius - 10)
                
                circle = Circle(x, y, i, self.circle_radius)
                
                # Check for overlaps
                overlap = False
                for existing_circle in self.circles:
                    if circle.overlaps_with(existing_circle):
                        overlap = True
                        break
                
                if not overlap:
                    self.circles.append(circle)
                    break
            else:
                # If we couldn't find a non-overlapping position, just place it anyway
                self.circles.append(circle)
        
        # Draw all circles
        self.draw_circles()
        
        # Start timer update
        self.update_timer()
    
    def draw_circles(self):
        """Draw all circles on the canvas."""
        for circle in self.circles:
            if not circle.clicked:
                # Draw circle
                x1 = circle.x - circle.radius
                y1 = circle.y - circle.radius
                x2 = circle.x + circle.radius
                y2 = circle.y + circle.radius
                
                circle.canvas_id = self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=self.circle_color,
                    outline="#2980b9",
                    width=2
                )
                
                # Draw number
                circle.text_id = self.canvas.create_text(
                    circle.x, circle.y,
                    text=str(circle.number),
                    font=("Arial", 16, "bold"),
                    fill=self.text_color
                )
    
    def on_canvas_click(self, event):
        """Handle canvas click events."""
        if not self.game_active:
            return
        
        # Check if any circle was clicked
        clicked_circle = None
        for circle in self.circles:
            if not circle.clicked and circle.contains_point(event.x, event.y):
                clicked_circle = circle
                break
        
        # If no circle was clicked (empty space), do nothing
        if clicked_circle is None:
            return
        
        # Check if it's the correct number
        if clicked_circle.number == self.current_number:
            # Correct click
            self.mark_circle_clicked(clicked_circle)
            self.current_number += 1
            
            # Update hint
            if self.hint_label:
                if self.current_number <= self.numbers_count:
                    self.hint_label.config(text=f"Next: {self.current_number}")
                else:
                    self.hint_label.config(text="Almost done!")
            
            # Check if game is complete
            if self.current_number > self.numbers_count:
                self.game_complete()
        else:
            # Wrong click - game over
            self.game_over()
    
    def mark_circle_clicked(self, circle: Circle):
        """Mark a circle as clicked (change its appearance)."""
        circle.clicked = True
        
        # Change color to indicate it's done
        if circle.canvas_id:
            self.canvas.itemconfig(circle.canvas_id, fill=self.clicked_color, 
                                  outline="#27ae60")
    
    def update_timer(self):
        """Update the timer display."""
        if self.game_active and self.timer_label:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed:.2f}s")
            self.root.after(50, self.update_timer)  # Update every 50ms
    
    def game_complete(self):
        """Handle successful game completion."""
        self.game_active = False
        elapsed = time.time() - self.start_time
        
        # Save to database
        self.db.save_result(self.player_name, elapsed, self.numbers_count, True)
        
        # Show success message
        self.show_result_screen(
            success=True,
            time_seconds=elapsed,
            message=f"🎉 Congratulations!\n\nYou completed all {self.numbers_count} numbers in {elapsed:.2f} seconds!"
        )
    
    def game_over(self):
        """Handle game over (wrong number clicked)."""
        self.game_active = False
        elapsed = time.time() - self.start_time
        
        # Save to database
        self.db.save_result(self.player_name, elapsed, self.numbers_count, False)
        
        # Show failure message
        self.show_result_screen(
            success=False,
            time_seconds=elapsed,
            message=f"❌ Game Over!\n\nYou clicked the wrong number.\nYou needed: {self.current_number}\nTime: {elapsed:.2f} seconds"
        )
    
    def show_result_screen(self, success: bool, time_seconds: float, message: str):
        """Display the result screen after game ends."""
        self.clear_screen()
        
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Result message
        result_label = tk.Label(
            self.main_frame,
            text=message,
            font=("Arial", 16),
            bg="#ecf0f1",
            fg="#2c3e50",
            justify=tk.CENTER
        )
        result_label.pack(pady=40)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        buttons_frame.pack(pady=20)
        
        # Play again button
        play_again_button = tk.Button(
            buttons_frame,
            text="Play Again",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.show_game_screen,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        play_again_button.pack(side=tk.LEFT, padx=10)
        
        # Back to menu button
        menu_button = tk.Button(
            buttons_frame,
            text="Back to Menu",
            font=("Arial", 14),
            bg="#3498db",
            fg="white",
            command=self.show_start_screen,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        menu_button.pack(side=tk.LEFT, padx=10)
        
        # Show leaderboard
        self.show_leaderboard_on_result(time_seconds if success else None)
    
    def show_leaderboard_on_result(self, player_time: float = None):
        """Display leaderboard on result screen."""
        leaderboard_frame = tk.LabelFrame(
            self.main_frame,
            text="🏆 Top 10 Leaderboard",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        leaderboard_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        leaderboard = self.db.get_leaderboard(limit=10)
        
        if leaderboard:
            # Create scrollable frame
            canvas_frame = tk.Frame(leaderboard_frame, bg="#ecf0f1")
            canvas_frame.pack(fill=tk.BOTH, expand=True)
            
            for idx, (name, time_sec, num_circles, timestamp) in enumerate(leaderboard, 1):
                # Highlight player's new score if applicable
                bg_color = "#fff9c4" if (player_time and abs(time_sec - player_time) < 0.01 
                                        and name == self.player_name) else "white"
                
                entry_frame = tk.Frame(canvas_frame, bg=bg_color, relief=tk.RAISED, bd=1)
                entry_frame.pack(fill=tk.X, pady=2)
                
                entry_text = f"#{idx}  {name}  -  {time_sec:.2f}s  -  {num_circles} circles"
                tk.Label(
                    entry_frame,
                    text=entry_text,
                    font=("Arial", 10),
                    bg=bg_color,
                    anchor="w"
                ).pack(fill=tk.X, padx=10, pady=5)
        else:
            tk.Label(
                canvas_frame,
                text="No records yet.",
                font=("Arial", 11, "italic"),
                bg="#ecf0f1",
                fg="#7f8c8d"
            ).pack(pady=20)
    
    def quit_to_menu(self):
        """Quit current game and return to menu."""
        if self.game_active:
            # Save incomplete game
            elapsed = time.time() - self.start_time
            self.db.save_result(self.player_name, elapsed, self.numbers_count, False)
        
        self.game_active = False
        self.show_start_screen()
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
        
        self.canvas = None
        self.timer_label = None
        self.hint_label = None
