import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'monitoring.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mesures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sonde TEXT,
            valeur TEXT,
            date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamps TEXT,
            alert_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_mesure(sonde, valeur):
    date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mesures (sonde, valeur, date)
        VALUES (?, ?, ?)
    ''', (sonde, valeur, date))
    conn.commit()
    conn.close()

def insert_alert(alert_text):
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (timestamps, alert_text)
        VALUES (?, ?)
    ''', (timestamp, alert_text))
    conn.commit()
    conn.close()

def clean_old_mesures(max_minutes=60):
    cutoff = datetime.now() - timedelta(minutes=max_minutes)
    cutoff_str = cutoff.strftime('%d-%m-%Y %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mesures WHERE date < ?', (cutoff_str,))
    conn.commit()
    conn.close()

def get_last_measurements():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sonde, valeur
        FROM mesures
        WHERE sonde IN ('cpu', 'ram')
        ORDER BY date DESC
        LIMIT 2;
    """)
    result = cursor.fetchall()
    conn.close()
    return result
