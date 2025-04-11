import sqlite3
from datetime import datetime, timedelta


DB_PATH = 'monitoring.db'

def init_alerts_table():
	conn = sqlite3.connect (DB_PATH)
	cursor = conn.cursor()

	
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS alerts(
		
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			timestamps TEXT,
			alert_text TEXT

 		)
	''')

	conn.commit()
	conn.close()

def  alert_exists(alert_text):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT (*) FROM alerts WHERE alert_text=?',(alert_text,))
	result = cursor.fetchone()[0]
	conn.close()
	return result > 0

def insert_alert(alert_text):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()

	cursor.execute('''
		INSERT INTO alerts (timestamps, alert_text)
		VALUES (?, ?)

	''', (datetime.now().strftime('%d-%m-%Y  %H:%M:%S'),alert_text))


	conn.commit()
	conn.close()


def delete_old_alerts(days=7):  
	seuil = datetime.now() - timedelta(days=days) 
	seuil_str = seuil.strftime('%d-%m-%Y %H:%M:%S')
 
	conn = sqlite3.connect(DB_PATH)	
	cursor = conn.cursor()

	cursor.execute('DELETE FROM alerts WHERE timestamps < ?',(seuil_str,))
	
	conn.commit() 
	conn.close()

def init_db():
	conn= sqlite3.connect( DB_PATH)
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF  NOT EXISTS mesures (
			id INTEGER PRIMARY KEY AUTOINCREMENT ,
			sonde TEXT,
			valeur TEXT,
			date TEXT
		)
	''')
	conn.commit()
	conn.close()
def insert_mesure(sonde, valeur):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	date = datetime.now().strftime('%d-%m-%Y %H:%M:%S ' )
	cursor.execute(
		'INSERT INTO mesures (sonde, valeur, date) VALUES (? , ?, ?)',
		(sonde, valeur, date)
	)
	conn.commit()
	conn.close()

def clean_old_mesures(max=60):
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	
	cutoff = datetime.now() - timedelta( minutes =max)
	
	cutoff_str = cutoff.strftime('%d-%m-%Y %H:%M:%S ')
	cursor.execute('DELETE FROM mesures WHERE date < ?',(cutoff_str,))
	conn.commit()
	conn.close()
