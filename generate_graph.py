import pygal
import sqlite3
from datetime import datetime

def generate_cpu_graph():
    # Connexion à la base de données
    conn = sqlite3.connect('/home/uapv2305487/projet/monitoring.db')
    cursor = conn.cursor()

    # Extraire les données de CPU de la table 'mesures'
    cursor.execute("SELECT valeur, date FROM mesures WHERE sonde='cpu' ORDER BY date DESC LIMIT 60")
    data = cursor.fetchall()

    # Données pour le graphique
    cpu_values = [float(value) for value, date in data]
    dates = [date for value, date in data]

    # Créer le graphique
    line_chart = pygal.Line()
    line_chart.title = 'Utilisation CPU sur les 60 dernières minutes'
    line_chart.x_labels = dates
    line_chart.add('CPU (%)', cpu_values)

    # Sauvegarder le graphique sous format SVG
    line_chart.render_to_file('cpu_usage.svg')

    # Fermer la connexion à la base de données
    conn.close()

def generate_ram_graph():
    # Connexion à la base de données
    conn = sqlite3.connect('/home/uapv2305487/projet/monitoring.db')
    cursor = conn.cursor()

    # Extraire les données de RAM de la table 'mesures'
    cursor.execute("SELECT valeur, date FROM mesures WHERE sonde='ram' ORDER BY date DESC LIMIT 60")
    data = cursor.fetchall()

    # Données pour le graphique
    ram_values = [float(value) for value, date in data]
    dates = [date for value, date in data]

    # Créer le graphique
    line_chart = pygal.Line()
    line_chart.title = 'Utilisation RAM sur les 60 dernières minutes'
    line_chart.x_labels = dates
    line_chart.add('RAM (%)', ram_values)

    # Sauvegarder le graphique sous format SVG
    line_chart.render_to_file('ram_usage.svg')

    # Fermer la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    generate_cpu_graph()
    generate_ram_graph()
