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
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            temp_min REAL,
            temp_max REAL
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
    connention.commit()
    connention.close()
    print("Inserted to database")



if __name__ == "__main__":
    #create_database()
    insert_database()
