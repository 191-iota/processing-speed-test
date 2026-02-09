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
# TODO: Add cleanup mechanism for stale game sessions (TTL-based)
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


def generate_circles(count: int, width: int, height: int, radius: int = 30, safe_area: dict = None):
    """Generate non-overlapping circles at random positions within safe area."""
    circles = []
    
    # Use safe area if provided, otherwise add basic padding
    if safe_area:
        min_x = safe_area.get('minX', radius + 20)
        max_x = safe_area.get('maxX', width - radius - 20)
        min_y = safe_area.get('minY', radius + 20)
        max_y = safe_area.get('maxY', height - radius - 20)
    else:
        min_x = radius + 20
        max_x = width - radius - 20
        min_y = radius + 20
        max_y = height - radius - 20
    
    # Ensure we have valid boundaries
    if max_x <= min_x or max_y <= min_y:
        # Invalid safe area boundaries - log warning and use conservative defaults
        print(f"Warning: Invalid safe_area boundaries received. Using defaults. "
              f"min_x={min_x}, max_x={max_x}, min_y={min_y}, max_y={max_y}")
        # Use conservative boundaries to ensure circles stay in safe area
        min_x = max(radius + 40, min_x) if min_x > 0 else radius + 40
        max_x = min(width - radius - 40, max_x) if max_x > 0 else width - radius - 40
        min_y = max(radius + 100, min_y) if min_y > 0 else radius + 100  # Extra space for header
        max_y = min(height - radius - 120, max_y) if max_y > 0 else height - radius - 120  # Extra space for footer
    
    for i in range(1, count + 1):
        max_attempts = 100
        for attempt in range(max_attempts):
            # Generate position within safe boundaries
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            
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
    """Get the leaderboard, optionally grouped by circle count."""
    numbers_count = request.args.get('numbers_count', type=int)
    grouped = request.args.get('grouped', default='false').lower() == 'true'
    
    if grouped:
        # Return leaderboards grouped by circle count
        grouped_leaderboard = db.get_leaderboard_grouped_by_circles(limit_per_group=10)
        
        result = {}
        for circle_count, entries in grouped_leaderboard.items():
            result[circle_count] = [
                {
                    'name': name,
                    'time': round(time_sec, 2),
                    'timestamp': timestamp
                }
                for name, time_sec, num_circles, timestamp in entries
            ]
        
        return jsonify(result)
    else:
        # Return single leaderboard (backward compatible)
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
    
    # Get safe area boundaries from client
    safe_area = data.get('safe_area', None)
    
    # Generate circles within safe area
    circles = generate_circles(numbers_count, canvas_width, canvas_height, safe_area=safe_area)
    
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
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
