# db.py
from flask import g
import sqlite3

DATABASE = 'database.db'

def get_db():
    """Connect to the database and return the connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    """Close the database connection when done."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
