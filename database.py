import sqlite3

def init_db():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        ratings REAL,
        distance REAL,
        weather TEXT,
        traffic TEXT,
        vehicle TEXT,
        preparation_time INTEGER,
        prediction REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_record(data):
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history (
        age, ratings, distance, weather, traffic, vehicle, preparation_time, prediction
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()