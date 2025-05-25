#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to yield users in batches from the user_data table"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def batch_processing(batch_size):
    """Processes each batch, filtering users older than 25"""
    for batch in stream_users_in_batches(batch_size):  # 1 loop
        for user in batch:                              # 2nd loop
            if int(user['age']) > 25:                   # filter condition
                yield user                              # generator use
