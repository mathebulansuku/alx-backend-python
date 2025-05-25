#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one at a time"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # Loop 1
            yield int(age)

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return


def calculate_average_age():
    """Calculates and prints average age using streamed ages"""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate average age.")
