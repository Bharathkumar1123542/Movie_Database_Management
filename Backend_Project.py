"""
Enhanced Movie Database Backend
Provides improved database operations with proper error handling and validation
"""

import sqlite3
from typing import List, Tuple, Optional
import os

class MovieDatabase:
    """Database handler for movie management system"""
    
    def __init__(self, db_name: str = "movie_system.db"):
        self.db_name = db_name
        self.initialize_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.db_name)
    
    def initialize_database(self):
        """Create the movies table if it doesn't exist"""
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        movie_id TEXT NOT NULL UNIQUE,
                        movie_name TEXT NOT NULL,
                        release_date TEXT,
                        director TEXT,
                        cast TEXT,
                        budget TEXT,
                        duration TEXT,
                        rating TEXT
                    )
                """)
                con.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    def add_movie(self, movie_id: str, movie_name: str, release_date: str = "",
                  director: str = "", cast: str = "", budget: str = "",
                  duration: str = "", rating: str = "") -> Tuple[bool, str]:
        """
        Add a new movie record to the database
        Returns: (success: bool, message: str)
        """
        if not movie_id or not movie_name:
            return False, "Movie ID and Movie Name are required!"
        
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO movies (movie_id, movie_name, release_date, 
                                      director, cast, budget, duration, rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (movie_id, movie_name, release_date, director, 
                      cast, budget, duration, rating))
                con.commit()
                return True, "Movie added successfully!"
        except sqlite3.IntegrityError:
            return False, f"Movie ID '{movie_id}' already exists!"
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def view_all_movies(self) -> List[Tuple]:
        """Retrieve all movie records"""
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM movies ORDER BY id DESC")
                return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving movies: {e}")
            return []
    
    def search_movies(self, **kwargs) -> List[Tuple]:
        """
        Search movies by any field
        Supports partial matching for better search results
        """
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                
                # Build dynamic query
                conditions = []
                params = []
                
                for key, value in kwargs.items():
                    if value:  # Only search non-empty values
                        conditions.append(f"{key} LIKE ?")
                        params.append(f"%{value}%")
                
                if not conditions:
                    return self.view_all_movies()
                
                query = "SELECT * FROM movies WHERE " + " OR ".join(conditions)
                cur.execute(query, params)
                return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Search error: {e}")
            return []
    
    def update_movie(self, record_id: int, movie_id: str, movie_name: str,
                    release_date: str = "", director: str = "", cast: str = "",
                    budget: str = "", duration: str = "", rating: str = "") -> Tuple[bool, str]:
        """Update an existing movie record"""
        if not movie_id or not movie_name:
            return False, "Movie ID and Movie Name are required!"
        
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("""
                    UPDATE movies 
                    SET movie_id=?, movie_name=?, release_date=?, director=?,
                        cast=?, budget=?, duration=?, rating=?
                    WHERE id=?
                """, (movie_id, movie_name, release_date, director, 
                      cast, budget, duration, rating, record_id))
                con.commit()
                
                if cur.rowcount == 0:
                    return False, "No record found to update!"
                return True, "Movie updated successfully!"
        except sqlite3.IntegrityError:
            return False, f"Movie ID '{movie_id}' already exists!"
        except sqlite3.Error as e:
            return False, f"Update error: {str(e)}"
    
    def delete_movie(self, record_id: int) -> Tuple[bool, str]:
        """Delete a movie record by ID"""
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM movies WHERE id=?", (record_id,))
                con.commit()
                
                if cur.rowcount == 0:
                    return False, "No record found to delete!"
                return True, "Movie deleted successfully!"
        except sqlite3.Error as e:
            return False, f"Delete error: {str(e)}"
    
    def get_movie_by_id(self, record_id: int) -> Optional[Tuple]:
        """Retrieve a single movie by database ID"""
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM movies WHERE id=?", (record_id,))
                return cur.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving movie: {e}")
            return None
    
    def get_statistics(self) -> dict:
        """Get database statistics"""
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM movies")
                total_movies = cur.fetchone()[0]
                
                cur.execute("SELECT AVG(CAST(rating AS REAL)) FROM movies WHERE rating != ''")
                avg_rating = cur.fetchone()[0]
                
                return {
                    'total_movies': total_movies,
                    'average_rating': round(avg_rating, 2) if avg_rating else 0
                }
        except sqlite3.Error as e:
            print(f"Statistics error: {e}")
            return {'total_movies': 0, 'average_rating': 0}


# Create singleton instance
db = MovieDatabase()

# Backward compatibility functions
def MovieData():
    """Initialize database (kept for backward compatibility)"""
    db.initialize_database()

def AddMovieRec(*args):
    """Add movie record"""
    return db.add_movie(*args)

def ViewMovieData():
    """View all movies"""
    return db.view_all_movies()

def DeleteMovieRec(record_id):
    """Delete movie record"""
    return db.delete_movie(record_id)

def SearchMovieData(movie_id="", movie_name="", release_date="", director="",
                    cast="", budget="", duration="", rating=""):
    """Search movies"""
    return db.search_movies(
        movie_id=movie_id,
        movie_name=movie_name,
        release_date=release_date,
        director=director,
        cast=cast,
        budget=budget,
        duration=duration,
        rating=rating
    )

def UpdateMovieData(record_id, *args):
    """Update movie record"""
    return db.update_movie(record_id, *args)