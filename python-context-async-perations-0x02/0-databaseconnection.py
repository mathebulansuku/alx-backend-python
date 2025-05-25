#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return the connection object."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection. Rollback if exception occurred."""
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()

# Using the context manager to perform a query
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(user)
