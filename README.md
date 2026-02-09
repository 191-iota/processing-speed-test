# Number Sequence Speed Test

A fun and challenging **web application** to test your processing speed and hand-eye coordination! Click numbered circles in sequential order as fast as you can.

## 🎮 Game Overview

Test your reaction time and accuracy by clicking numbered circles in ascending order (1, 2, 3, 4...). The faster you complete all numbers, the better your score!

## ✨ Features

- **Fullscreen Web Application**: Modern, responsive web interface
- **Intuitive UI**: Clean and user-friendly design with smooth animations
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
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Flask web framework

### Installation

1. Clone the repository:
```bash
git clone https://github.com/191-iota/processing-speed-test.git
cd processing-speed-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the web application:
```bash
python main.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 🌐 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

**Using Gunicorn (recommended for production):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

**Using Docker:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

**Deploy to Cloud Platforms:**
- **Heroku**: Push to Heroku with a `Procfile`
- **AWS Elastic Beanstalk**: Deploy as Python application
- **Google Cloud Run**: Deploy as containerized app
- **DigitalOcean App Platform**: Deploy directly from Git

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
├── main.py              # Flask application and API endpoints
├── database.py          # SQLite database operations
├── game.py              # Legacy Tkinter version (deprecated)
├── templates/
│   └── index.html      # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css   # Fullscreen webapp styling
│   └── js/
│       └── game.js     # Client-side game logic
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── game_results.db     # SQLite database (created on first run)
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

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (Canvas API)
- **Database**: SQLite3 (serverless database)
- **Design**: Fullscreen responsive layout with gradient backgrounds
- **Circle Radius**: 30 pixels (60px diameter)
- **Canvas Size**: Dynamically resizes to fill browser window
- **Timer Precision**: Updates every 50ms
- **Overlap Prevention**: Circles maintain 10px minimum spacing

## 🛠️ API Endpoints

### GET `/`
Returns the main HTML page

### GET `/api/leaderboard`
Get top 10 leaderboard entries
- Optional query param: `numbers_count` (filter by circle count)
- Returns: JSON array of leaderboard entries

### POST `/api/game/start`
Start a new game session
- Body: `{ player_name, numbers_count, canvas_width, canvas_height }`
- Returns: `{ game_id, circles, current_number }`

### POST `/api/game/click`
Handle a circle click
- Body: `{ game_id, x, y }`
- Returns: `{ result, ... }` (result: 'correct', 'wrong', 'complete', or 'empty')

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

**Issue**: "Connection refused" error
- **Solution**: Make sure Flask is running (`python main.py`)
- Check that port 5000 is not in use by another application

**Issue**: Database errors
- **Solution**: Delete `game_results.db` and restart the application

**Issue**: Circles not appearing
- **Solution**: Check browser console for JavaScript errors
- Ensure canvas is properly sized (refresh the page)

**Issue**: Leaderboard not loading
- **Solution**: Check network tab in browser developer tools
- Verify Flask backend is running and accessible

---

**Enjoy the game and happy clicking! 🎯**
