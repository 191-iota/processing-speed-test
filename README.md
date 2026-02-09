# Number Sequence Speed Test

A fun and challenging game to test your processing speed and hand-eye coordination! Click numbered circles in sequential order as fast as you can.

## 🎮 Game Overview

Test your reaction time and accuracy by clicking numbered circles in ascending order (1, 2, 3, 4...). The faster you complete all numbers, the better your score!

## ✨ Features

- **Intuitive GUI**: Clean and user-friendly interface built with Tkinter
- **Customizable Difficulty**: Choose between 5, 10, 15, or 20 circles
- **Random Placement**: Circles are randomly positioned each game (no overlaps)
- **Real-time Timer**: Track your performance with millisecond precision
- **Persistent Leaderboard**: SQLite database stores all game results
- **Player Profiles**: Enter your name and compete with others
- **Smart Game Logic**:
  - Click correct number → Continue to next
  - Click wrong number → Game over
  - Click empty space → Nothing happens
- **Visual Feedback**: Circles change color when clicked correctly

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher (with tkinter support)
- No external dependencies needed! (uses built-in libraries)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/191-iota/processing-speed-test.git
cd processing-speed-test
```

2. Run the game:
```bash
python main.py
```

Or on some systems:
```bash
python3 main.py
```

## 🎯 How to Play

1. **Start Screen**:
   - Enter your player name
   - Select number of circles (5, 10, 15, or 20)
   - View the leaderboard of top performers
   - Click "Start Game"

2. **During the Game**:
   - Click circles in numerical order (1 → 2 → 3 → ...)
   - Watch the timer to track your performance
   - Use the "Next" hint to see which number you need
   - Click "Quit to Menu" to exit early

3. **Game Rules**:
   - ✅ **Correct Click**: Circle turns green, proceed to next number
   - ❌ **Wrong Click**: Game ends, time is recorded as incomplete
   - ⭕ **Empty Space Click**: Nothing happens, game continues
   - 🎉 **Complete All Numbers**: Success! Your time is saved

4. **After the Game**:
   - View your completion time
   - Check the leaderboard
   - Play again or return to menu

## 📁 File Structure

```
processing-speed-test/
├── README.md           # This file - game instructions
├── main.py            # Main entry point
├── game.py            # Game logic and Tkinter UI
├── database.py        # SQLite database operations
├── requirements.txt   # Dependencies (none required)
└── game_results.db    # SQLite database (created on first run)
```

## 🗄️ Database Schema

The game uses SQLite to store results:

```sql
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    time_seconds REAL NOT NULL,
    numbers_count INTEGER NOT NULL,
    completed BOOLEAN NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🏆 Leaderboard

- Top 10 fastest completion times are displayed
- Only completed games count toward the leaderboard
- Failed attempts are still recorded in the database
- Filter by number of circles to compare similar difficulty

## 🎨 Technical Details

- **GUI Framework**: Tkinter (Python's built-in GUI library)
- **Database**: SQLite3 (Python's built-in database)
- **Circle Radius**: 30 pixels (60px diameter)
- **Canvas Size**: 800x500 pixels
- **Window Size**: 800x700 pixels (fixed)
- **Timer Precision**: Updates every 50ms
- **Overlap Prevention**: Circles maintain 10px minimum spacing

## 🛠️ Development

The game is structured into three main modules:

1. **database.py**: Handles all SQLite operations
   - Create/connect to database
   - Save game results
   - Retrieve leaderboard
   - Query historical data

2. **game.py**: Main game logic and UI
   - Circle class for game objects
   - NumberSequenceGame class for game state
   - Tkinter UI screens (start, game, result)
   - Click detection and game logic

3. **main.py**: Entry point
   - Initialize Tkinter
   - Start the game

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 🎮 Tips for High Scores

- Start with fewer circles (5 or 10) to practice
- Memorize number positions before clicking
- Develop a clicking pattern (left to right, top to bottom, etc.)
- Stay calm and focused - accuracy matters as much as speed
- Use the hint label to confirm the next number

## 🐛 Troubleshooting

**Issue**: "tkinter not found" error
- **Solution**: Install tkinter for your Python version:
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - macOS: tkinter comes with Python from python.org
  - Windows: tkinter is included with standard Python installation

**Issue**: Window doesn't appear
- **Solution**: Make sure you have a graphical environment (not SSH without X11)

**Issue**: Circles overlap
- **Solution**: This is rare but can happen with many circles. Try reducing the count or restarting the game.

---

**Enjoy the game and happy clicking! 🎯**
