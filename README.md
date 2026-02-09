# Processing Speed Test

A web-based cognitive assessment tool that measures processing speed and visuomotor coordination through a sequential number clicking task.

## Overview

This interactive test challenges you to click numbered circles in sequential order (1, 2, 3...) as quickly and accurately as possible. Inspired by clinical reaction time assessments used in neuropsychological testing, this tool provides an engaging way to measure cognitive processing speed.

## The Science Behind Processing Speed

Processing speed is a fundamental cognitive ability that determines how quickly your brain can perceive information, process it, and respond. It's measured in neuropsychological assessments and affects everyday tasks from reading to driving.

### What is Processing Speed?

Processing speed refers to the pace at which the brain takes in information, makes sense of it, and begins to respond. It's a core component of cognitive function that underlies many mental operations:

- The ability to automatically and fluently perform cognitive tasks, especially when under pressure
- The efficiency of mental processing, independent of intelligence or prior knowledge
- A measurable aspect of cognitive function that typically peaks in early adulthood and gradually declines with age

### Neurological Foundation

Processing speed depends on several neural mechanisms:

- **Neural efficiency**: How quickly neurons fire and transmit signals between brain regions
- **White matter integrity**: Myelin insulation around nerve fibers that speeds signal transmission across neural pathways
- **Network connectivity**: Communication efficiency between brain regions, particularly the prefrontal cortex (decision-making) and parietal cortex (visual-spatial processing)
- **Synaptic function**: The speed and reliability of neurotransmitter signaling at neural connections

### What This Test Measures

This sequential number test evaluates several interconnected cognitive components:

- **Visual scanning speed**: Rapidly searching the visual field for target numbers among distractors
- **Selective attention**: Focusing on the correct stimulus while filtering out irrelevant information
- **Response inhibition**: Suppressing incorrect responses under time pressure and maintaining accuracy
- **Visuomotor coordination**: Translating visual perception into accurate motor action (hand-eye coordination)
- **Working memory**: Maintaining the current target number in mind during visual search
- **Decision speed**: Quick evaluation and selection of the correct response

### Clinical Relevance

Processing speed assessment is valuable for detecting cognitive changes in various conditions:

- **Attention-deficit disorders**: ADHD and attention deficits often show as reduced processing speed
- **Traumatic brain injury**: Concussion and TBI frequently impact processing efficiency
- **Neurodegenerative conditions**: Early marker in conditions affecting cognitive function
- **Normal cognitive aging**: Natural decline in processing speed with age
- **Rehabilitation monitoring**: Tracking recovery and improvement over time

Research shows that processing speed training can improve performance on timed cognitive tasks and may have broader effects on executive function and quality of life.

## How to Play

1. **Start Screen**: Enter your player name, select the number of circles (5, 10, 15, or 20), and click "Start Game"
2. **During the Game**: Click circles in numerical order (1 → 2 → 3 → ...) as quickly as possible
3. **Correct Click**: Circle turns green and you proceed to the next number
4. **Wrong Click**: Game ends and your time is recorded as incomplete
5. **Complete All Numbers**: Your completion time is saved to the leaderboard

## Features

- **Modern Web Interface**: Responsive fullscreen design that works on desktop and mobile devices
- **Customizable Difficulty**: Choose between 5, 10, 15, or 20 circles
- **Real-time Performance Tracking**: Millisecond-precision timer
- **Persistent Leaderboard**: SQLite database stores all game results with player profiles
- **Smart Game Logic**: Correct clicks advance the sequence, wrong clicks end the game, empty clicks are ignored
- **Visual Feedback**: Color changes indicate successful clicks
- **Random Placement**: Circles are positioned randomly with no overlaps each game

## Installation

**Prerequisites**: Python 3.7 or higher

1. Clone the repository:
```bash
git clone https://github.com/191-iota/processing-speed-test.git
cd processing-speed-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser to `http://localhost:5000`

## Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

Using Gunicorn (recommended):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

The application can be deployed to various cloud platforms including Heroku, AWS Elastic Beanstalk, Google Cloud Run, and DigitalOcean App Platform.

## Database

The application uses SQLite to store game results with the following schema:

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

The leaderboard displays the top 10 fastest completion times, filterable by circle count. All games (completed and incomplete) are stored in the database.

## Technical Details

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript with Canvas API
- **Database**: SQLite3
- **Design**: Fullscreen responsive layout
- **Timer Precision**: 50ms update interval

## API Endpoints

**GET `/`** - Returns the main HTML page

**GET `/api/leaderboard`** - Get top 10 leaderboard entries
- Optional query param: `numbers_count` (filter by circle count)

**POST `/api/game/start`** - Start a new game session
- Body: `{ player_name, numbers_count, canvas_width, canvas_height }`
- Returns: `{ game_id, circles, current_number }`

**POST `/api/game/click`** - Handle a circle click
- Body: `{ game_id, x, y }`
- Returns: `{ result, ... }` (result: 'correct', 'wrong', 'complete', or 'empty')

## Requirements

- Python 3.7+
- Flask
- SQLite3 (included with Python)

## License

This project is open source and available under the MIT License.

---

**Note**: This is an educational tool inspired by clinical reaction time tests. It is not a substitute for professional cognitive assessment.
