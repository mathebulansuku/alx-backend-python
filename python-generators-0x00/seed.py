#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

DB_NAME = 'ALX_prodev'

TABLES = {}
TABLES['user_data'] = (
    "CREATE TABLE IF NOT EXISTS user_data ("
    "  user_id CHAR(36) NOT NULL PRIMARY KEY,"
    "  name VARCHAR(255) NOT NULL,"
    "  email VARCHAR(255) NOT NULL,"
    "  age DECIMAL NOT NULL,"
    "  INDEX (user_id)"
    ") ENGINE=InnoDB"
)

def connect_db():
    """Connects to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates ALX_prodev database if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def connect_to_prodev():
    """Connects to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def create_table(connection):
    """Creates the user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute(TABLES['user_data'])
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")

def insert_data(connection, csv_filename):
    """Inserts data from CSV file into user_data table"""
    try:
        cursor = connection.cursor()
        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if user_id exists
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                # Use INSERT IGNORE or check manually for duplicates if needed
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
