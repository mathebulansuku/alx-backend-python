#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    """Context manager that executes a provided SQL query with parameters."""
    
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.result = None

    def __enter__(self):
        """Establish connection, execute the query, and return the result."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection. Rollback if an exception occurred."""
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery('users.db', query, params) as users:
        for user in users:
            print(user)
