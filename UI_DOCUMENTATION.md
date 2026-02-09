# UI Visual Documentation

This document describes the visual layout of the game screens since the development environment doesn't support GUI display.

## Start Screen Layout

```
┌────────────────────────────────────────────────────────────────────┐
│                   Number Sequence Speed Test                       │
│                                                                    │
│        Click the circles in numerical order as fast as you can!   │
│                                                                    │
│               Player Name:  [Player              ]                │
│         Number of Circles:  [10          ▼]                       │
│                                                                    │
│                      [ Start Game ]                               │
│                                                                    │
│  ┌──────────────────── 🏆 Top 10 Fastest Times ─────────────────┐ │
│  │ Rank  Player          Time      Circles  Date                │ │
│  │ ───────────────────────────────────────────────────────────  │ │
│  │  #1   TestPlayer4    8.50s      5        2024-02-09...       │ │
│  │  #2   TestPlayer2    12.30s     10       2024-02-09...       │ │
│  │  #3   TestPlayer1    15.50s     10       2024-02-09...       │ │
│  │  #4   TestPlayer3    20.10s     15       2024-02-09...       │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Features:
- Clean title at the top
- Instructions text below title
- Player name input field (default: "Player")
- Number of circles dropdown (5, 10, 15, 20)
- Large green "Start Game" button
- Leaderboard showing top 10 times with ranking

---

## Game Screen Layout

```
┌────────────────────────────────────────────────────────────────────┐
│ Player: Alice      Time: 5.23s               Next: 7              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│        ┌──┐              ┌──┐                                     │
│        │ 3│              │ 8│              ┌──┐                   │
│        └──┘              └──┘              │ 1│                   │
│                                             └──┘                   │
│                  ┌──┐                                             │
│    ┌──┐          │ 5│                              ┌──┐          │
│    │ 9│          └──┘          ┌──┐                │ 4│          │
│    └──┘                        │ 7│                └──┘          │
│                                └──┘                               │
│                      ┌──┐                                         │
│                      │ 2│              ┌──┐                       │
│          ┌──┐        └──┘              │ 6│                       │
│          │10│                          └──┘                       │
│          └──┘                                                     │
│                                                                    │
│                                                                    │
│                       [ Quit to Menu ]                            │
└────────────────────────────────────────────────────────────────────┘
```

### Features:
- Dark info bar at top showing:
  - Player name (left)
  - Current time (center, yellow/gold color)
  - Next number to click (right, green color)
- Large canvas with circles at random positions
- Circles are blue (#3498db) initially
- When clicked correctly, circles turn green (#2ecc71)
- Numbers are displayed in white, centered in circles
- "Quit to Menu" button at bottom (red)

### Circle States:
- **Unclicked**: Blue circle with white number
- **Correctly Clicked**: Green circle with white number
- **Wrong Click**: Triggers immediate game over

### Click Behavior:
- Click correct number → Circle turns green, proceed to next
- Click wrong number → Game over screen
- Click empty space → Nothing happens, game continues

---

## Success Screen Layout

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                          🎉 Congratulations!                       │
│                                                                    │
│              You completed all 10 numbers in 15.42 seconds!       │
│                                                                    │
│                                                                    │
│            [ Play Again ]           [ Back to Menu ]              │
│                                                                    │
│                                                                    │
│  ┌──────────────────── 🏆 Top 10 Leaderboard ──────────────────┐  │
│  │  #1  TestPlayer4  -  8.50s  -  5 circles                    │  │
│  │  #2  TestPlayer2  -  12.30s  -  10 circles                  │  │
│  │  #3  Alice  -  15.42s  -  10 circles          [HIGHLIGHTED] │  │
│  │  #4  TestPlayer1  -  15.50s  -  10 circles                  │  │
│  │  #5  TestPlayer3  -  20.10s  -  15 circles                  │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Features:
- Success message with emoji
- Completion time display
- Two buttons: "Play Again" (green) and "Back to Menu" (blue)
- Leaderboard with player's new score highlighted in yellow
- Shows ranking and context

---

## Game Over Screen Layout

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                            ❌ Game Over!                           │
│                                                                    │
│                     You clicked the wrong number.                 │
│                            You needed: 5                          │
│                          Time: 3.21 seconds                       │
│                                                                    │
│            [ Play Again ]           [ Back to Menu ]              │
│                                                                    │
│                                                                    │
│  ┌──────────────────── 🏆 Top 10 Leaderboard ──────────────────┐  │
│  │  #1  TestPlayer4  -  8.50s  -  5 circles                    │  │
│  │  #2  TestPlayer2  -  12.30s  -  10 circles                  │  │
│  │  #3  TestPlayer1  -  15.50s  -  10 circles                  │  │
│  │  #4  TestPlayer3  -  20.10s  -  15 circles                  │  │
│  │                                                               │  │
│  │  (Your failed attempt was not added to leaderboard)          │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Features:
- Game over message with emoji
- Explanation of what went wrong
- Shows which number was needed
- Time spent before failure
- Two buttons: "Play Again" (green) and "Back to Menu" (blue)
- Leaderboard (failed attempts don't appear but are recorded in DB)

---

## Color Scheme

| Element | Color | Hex Code |
|---------|-------|----------|
| Background | Light Gray | #ecf0f1 |
| Primary Button | Green | #27ae60 |
| Secondary Button | Blue | #3498db |
| Danger Button | Red | #e74c3c |
| Circle (unclicked) | Blue | #3498db |
| Circle (clicked) | Green | #2ecc71 |
| Text (dark) | Dark Gray | #2c3e50 |
| Info Bar | Dark Gray | #34495e |
| Timer Text | Gold | #f39c12 |
| Highlight | Yellow | #fff9c4 |

---

## Technical Specifications

### Window
- Size: 800x700 pixels (fixed, non-resizable)
- Title: "Number Sequence Speed Test"

### Canvas
- Size: 800x500 pixels
- Background: Light gray (#ecf0f1)

### Circles
- Radius: 30 pixels (60px diameter)
- Border: 2px solid (darker shade of fill color)
- Font: Arial, 16pt, Bold
- Text Color: White
- Minimum spacing: 10px between circles

### Timer
- Updates every 50ms
- Displayed with 2 decimal places
- Format: "Time: X.XXs"

### Fonts
- Title: Arial, 24pt, Bold
- Buttons: Arial, 14-16pt, Bold
- Info bar: Arial, 12pt
- Instructions: Arial, 12pt
- Leaderboard: Arial, 10pt

---

## Game Flow Diagram

```
┌─────────────┐
│ Start Screen│
│   (Menu)    │
└──────┬──────┘
       │
       ├─ Enter name
       ├─ Select circles (5/10/15/20)
       └─ Click "Start Game"
       │
       ▼
┌─────────────┐
│ Game Screen │
│  (Playing)  │
└──────┬──────┘
       │
       ├─ Click circles 1→2→3→...
       │  - Correct: Circle turns green
       │  - Wrong: Game Over
       │  - Empty: Nothing
       │
       ├─ Complete all ──→ Success Screen ──┐
       │                                     │
       └─ Wrong click ──→ Game Over Screen ─┤
                                             │
       ┌─────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│Result Screen│
│(Success/Fail)
└──────┬──────┘
       │
       ├─ Play Again → Game Screen
       └─ Back to Menu → Start Screen
```

---

## Key Features Summary

1. ✅ **Random Circle Placement**: Circles never overlap
2. ✅ **Click Detection**: Accurate hit detection using distance formula
3. ✅ **Game Logic**: Enforces sequential clicking (1→2→3...)
4. ✅ **Timer**: Real-time display with millisecond precision
5. ✅ **Database**: SQLite stores all game results persistently
6. ✅ **Leaderboard**: Top 10 fastest completion times
7. ✅ **Visual Feedback**: Circles change color when clicked
8. ✅ **Empty Space Handling**: Clicking outside circles does nothing
9. ✅ **Configurable Difficulty**: 5, 10, 15, or 20 circles
10. ✅ **Player Names**: Track individual performance
11. ✅ **Play Again**: Quick restart without returning to menu
12. ✅ **Clean UI**: Modern, colorful, user-friendly interface

---

## Database Schema

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

### Example Data

| id | player_name | time_seconds | numbers_count | completed | timestamp |
|----|-------------|--------------|---------------|-----------|-----------|
| 1  | Alice       | 12.50        | 10            | 1 (True)  | 2024-02-09 10:30:00 |
| 2  | Bob         | 15.30        | 10            | 1 (True)  | 2024-02-09 10:31:00 |
| 3  | Charlie     | 8.90         | 5             | 1 (True)  | 2024-02-09 10:32:00 |
| 4  | Diana       | 5.20         | 10            | 0 (False) | 2024-02-09 10:33:00 |

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/191-iota/processing-speed-test.git
cd processing-speed-test

# Run the game
python3 main.py
```

The game will:
1. Create `game_results.db` on first run
2. Open a 800x700 window
3. Display the start screen
4. Ready to play!

No external dependencies needed - uses only Python built-in libraries (tkinter, sqlite3).
