#!/usr/bin/env python3

import sqlite3
import time
import os


def create_database():
    if os.path.exists("items.db"):
        os.remove("items.db")
        print("An old database removed.")

    connection = sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            temp_min REAL NOT NULL,
            temp_max REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            card_number TEXT NOT NULL UNIQUE,
            user_name TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    print("The new database created.")

def insert_database():
    connention = sqlite3.connect("items.db")
    cursor = connention.cursor()
    cursor.execute("INSERT INTO items (name, temp_min, temp_max) VALUES (?,?,?)",
        ("Krew 5l", 3, 18))
    cursor.execute("INSERT INTO items (name, temp_min, temp_max) VALUES (?,?,?)",
        ("Strzykawki 100 szt", 15, 25))
    sample_users = [
        ('1234567890123456', 'Jacenty Kowalski'),
        ('9876543210987654', 'Anna Janiak'),
        ('5555666677778888', 'Mariusz Arbuz')
    ]

    cursor.executemany("INSERT INTO users (card_number, user_name) VALUES (?, ?)", sample_users)

    connention.commit()
    connention.close()





if __name__ == "__main__":
    create_database()
    insert_database()
