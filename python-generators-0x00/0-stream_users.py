#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator function that yields users from the user_data table one at a time"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return
