"""
Main entry point for the Number Sequence Speed Test game.
"""

import tkinter as tk
from game import NumberSequenceGame


def main():
    """Initialize and run the game."""
    root = tk.Tk()
    game = NumberSequenceGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
