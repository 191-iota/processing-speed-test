"""
Database operations for the number sequence speed test game.
Supports PostgreSQL (production) with SQLite fallback (local development).
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class GameDatabase:
    """Handles all database operations for the game."""
    
    def __init__(self, db_name: str = "game_results.db"):
        """Initialize database connection and create tables if needed."""
        # Check for PostgreSQL connection string
        self.database_url = os.environ.get('DATABASE_URL')
        
        if self.database_url:
            # Using PostgreSQL
            # Handle Heroku/Render postgres:// URLs (convert to postgresql://)
            if self.database_url.startswith('postgres://'):
                self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
            
            try:
                import psycopg2
                self.use_postgres = True
                self.db_name = None
                print("Using PostgreSQL database")
            except ImportError:
                print("Warning: psycopg2 not installed, falling back to SQLite")
                self.use_postgres = False
                self.db_name = db_name
        else:
            # Using SQLite for local development
            self.use_postgres = False
            self.db_name = db_name
            print(f"Using SQLite database: {db_name}")
        
        self.create_tables()
    
    def _get_connection(self):
        """Get a database connection (PostgreSQL or SQLite)."""
        if self.use_postgres:
            import psycopg2
            return psycopg2.connect(self.database_url)
        else:
            return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        """Create the results table if it doesn't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            # PostgreSQL syntax
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    player_name TEXT NOT NULL,
                    time_seconds REAL NOT NULL,
                    numbers_count INTEGER NOT NULL,
                    completed BOOLEAN NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            # SQLite syntax
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    time_seconds REAL NOT NULL,
                    numbers_count INTEGER NOT NULL,
                    completed BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        conn.commit()
        conn.close()
    
    def save_result(self, player_name: str, time_seconds: float, 
                   numbers_count: int, completed: bool) -> int:
        """
        Save a game result to the database.
        
        Args:
            player_name: Name of the player
            time_seconds: Time taken to complete/fail the game
            numbers_count: Number of circles in the game
            completed: Whether the game was completed successfully
            
        Returns:
            The ID of the inserted record
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            # PostgreSQL uses %s for parameters
            cursor.execute("""
                INSERT INTO results (player_name, time_seconds, numbers_count, completed, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (player_name, time_seconds, numbers_count, completed, datetime.now()))
            result_id = cursor.fetchone()[0]
        else:
            # SQLite uses ? for parameters
            cursor.execute("""
                INSERT INTO results (player_name, time_seconds, numbers_count, completed, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (player_name, time_seconds, numbers_count, completed, datetime.now()))
            result_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return result_id
    
    def get_leaderboard(self, numbers_count: Optional[int] = None, 
                       limit: int = 10) -> List[Tuple]:
        """
        Get the top completed games (fastest times).
        
        Args:
            numbers_count: Filter by specific number of circles (None for all)
            limit: Maximum number of results to return
            
        Returns:
            List of tuples (player_name, time_seconds, numbers_count, timestamp)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            # PostgreSQL uses %s for parameters
            if numbers_count is not None:
                cursor.execute("""
                    SELECT player_name, time_seconds, numbers_count, timestamp
                    FROM results
                    WHERE completed = TRUE AND numbers_count = %s
                    ORDER BY time_seconds ASC
                    LIMIT %s
                """, (numbers_count, limit))
            else:
                cursor.execute("""
                    SELECT player_name, time_seconds, numbers_count, timestamp
                    FROM results
                    WHERE completed = TRUE
                    ORDER BY time_seconds ASC
                    LIMIT %s
                """, (limit,))
        else:
            # SQLite uses ? for parameters
            if numbers_count is not None:
                cursor.execute("""
                    SELECT player_name, time_seconds, numbers_count, timestamp
                    FROM results
                    WHERE completed = 1 AND numbers_count = ?
                    ORDER BY time_seconds ASC
                    LIMIT ?
                """, (numbers_count, limit))
            else:
                cursor.execute("""
                    SELECT player_name, time_seconds, numbers_count, timestamp
                    FROM results
                    WHERE completed = 1
                    ORDER BY time_seconds ASC
                    LIMIT ?
                """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_leaderboard_grouped_by_circles(self, limit_per_group: int = 10) -> dict:
        """
        Get leaderboards grouped by number of circles.
        
        Args:
            limit_per_group: Maximum number of results per circle count
            
        Returns:
            Dictionary mapping circle counts to leaderboard entries
            {5: [(name, time, count, timestamp), ...], 10: [...], ...}
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get all unique circle counts that have completed games
        if self.use_postgres:
            cursor.execute("""
                SELECT DISTINCT numbers_count
                FROM results
                WHERE completed = TRUE
                ORDER BY numbers_count ASC
            """)
        else:
            cursor.execute("""
                SELECT DISTINCT numbers_count
                FROM results
                WHERE completed = 1
                ORDER BY numbers_count ASC
            """)
        
        circle_counts = [row[0] for row in cursor.fetchall()]
        
        # Get leaderboard for each circle count
        grouped_leaderboard = {}
        for count in circle_counts:
            if self.use_postgres:
                cursor.execute("""
                    SELECT player_name, time_seconds, numbers_count, timestamp
                    FROM results
                    WHERE completed = TRUE AND numbers_count = %s
                    ORDER BY time_seconds ASC
                    LIMIT %s
                """, (count, limit_per_group))
            else:
                cursor.execute("""
                    SELECT player_name, time_seconds, numbers_count, timestamp
                    FROM results
                    WHERE completed = 1 AND numbers_count = ?
                    ORDER BY time_seconds ASC
                    LIMIT ?
                """, (count, limit_per_group))
            
            grouped_leaderboard[count] = cursor.fetchall()
        
        conn.close()
        
        return grouped_leaderboard
    
    def get_all_results(self, limit: int = 20) -> List[Tuple]:
        """
        Get recent game results (completed and failed).
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of tuples (player_name, time_seconds, numbers_count, completed, timestamp)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            cursor.execute("""
                SELECT player_name, time_seconds, numbers_count, completed, timestamp
                FROM results
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
        else:
            cursor.execute("""
                SELECT player_name, time_seconds, numbers_count, completed, timestamp
                FROM results
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
