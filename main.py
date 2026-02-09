"""
Main entry point for the Number Sequence Speed Test web application.
"""

from flask import Flask, render_template, request, jsonify, session
from database import GameDatabase
import secrets
import time
import random
import math

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
db = GameDatabase()

# Store active games in memory (in production, use Redis or similar)
active_games = {}


class Circle:
    """Represents a numbered circle in the game."""
    
    def __init__(self, x: float, y: float, number: int, radius: int = 30):
        self.x = x
        self.y = y
        self.number = number
        self.radius = radius
        self.clicked = False
    
    def contains_point(self, px: float, py: float) -> bool:
        """Check if a point is inside this circle."""
        distance = math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2)
        return distance <= self.radius
    
    def overlaps_with(self, other: 'Circle') -> bool:
        """Check if this circle overlaps with another circle."""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < (self.radius + other.radius + 10)
    
    def to_dict(self):
        """Convert circle to dictionary for JSON serialization."""
        return {
            'x': self.x,
            'y': self.y,
            'number': self.number,
            'radius': self.radius,
            'clicked': self.clicked
        }


def generate_circles(count: int, width: int, height: int, radius: int = 30):
    """Generate non-overlapping circles at random positions."""
    circles = []
    for i in range(1, count + 1):
        max_attempts = 100
        for attempt in range(max_attempts):
            # Add padding from edges
            x = random.uniform(radius + 20, width - radius - 20)
            y = random.uniform(radius + 20, height - radius - 20)
            
            circle = Circle(x, y, i, radius)
            
            # Check for overlaps
            overlap = False
            for existing in circles:
                if circle.overlaps_with(existing):
                    overlap = True
                    break
            
            if not overlap:
                circles.append(circle)
                break
        else:
            # Force placement if no position found
            circles.append(circle)
    
    return circles


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get the top 10 leaderboard."""
    numbers_count = request.args.get('numbers_count', type=int)
    leaderboard = db.get_leaderboard(numbers_count=numbers_count, limit=10)
    
    results = []
    for name, time_sec, num_circles, timestamp in leaderboard:
        results.append({
            'name': name,
            'time': round(time_sec, 2),
            'circles': num_circles,
            'timestamp': timestamp
        })
    
    return jsonify(results)


@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Start a new game session."""
    data = request.json
    player_name = data.get('player_name', 'Player')
    numbers_count = data.get('numbers_count', 10)
    
    # Get viewport dimensions from client
    canvas_width = data.get('canvas_width', 1200)
    canvas_height = data.get('canvas_height', 700)
    
    # Generate circles
    circles = generate_circles(numbers_count, canvas_width, canvas_height)
    
    # Create game session
    game_id = secrets.token_hex(8)
    active_games[game_id] = {
        'player_name': player_name,
        'numbers_count': numbers_count,
        'circles': circles,
        'current_number': 1,
        'start_time': time.time(),
        'completed': False
    }
    
    return jsonify({
        'game_id': game_id,
        'circles': [c.to_dict() for c in circles],
        'current_number': 1
    })


@app.route('/api/game/click', methods=['POST'])
def handle_click():
    """Handle a circle click."""
    data = request.json
    game_id = data.get('game_id')
    click_x = data.get('x')
    click_y = data.get('y')
    
    if game_id not in active_games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = active_games[game_id]
    
    if game['completed']:
        return jsonify({'error': 'Game already completed'}), 400
    
    # Find clicked circle
    clicked_circle = None
    for circle in game['circles']:
        if not circle.clicked and circle.contains_point(click_x, click_y):
            clicked_circle = circle
            break
    
    # Empty space click - do nothing
    if clicked_circle is None:
        return jsonify({
            'result': 'empty',
            'current_number': game['current_number']
        })
    
    # Check if correct number
    if clicked_circle.number == game['current_number']:
        # Correct click
        clicked_circle.clicked = True
        game['current_number'] += 1
        
        # Check if game complete
        if game['current_number'] > game['numbers_count']:
            elapsed = time.time() - game['start_time']
            game['completed'] = True
            
            # Save to database
            db.save_result(
                game['player_name'],
                elapsed,
                game['numbers_count'],
                True
            )
            
            return jsonify({
                'result': 'complete',
                'time': round(elapsed, 2),
                'circles': [c.to_dict() for c in game['circles']]
            })
        
        return jsonify({
            'result': 'correct',
            'current_number': game['current_number'],
            'circles': [c.to_dict() for c in game['circles']]
        })
    else:
        # Wrong click - game over
        elapsed = time.time() - game['start_time']
        game['completed'] = True
        
        # Save to database as incomplete
        db.save_result(
            game['player_name'],
            elapsed,
            game['numbers_count'],
            False
        )
        
        return jsonify({
            'result': 'wrong',
            'expected': game['current_number'],
            'clicked': clicked_circle.number,
            'time': round(elapsed, 2)
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
