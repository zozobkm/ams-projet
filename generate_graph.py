import pygal
import sqlite3
from datetime import datetime

def generate_combined_graph():
    # Connexion à la base de données
    conn = sqlite3.connect('/home/uapv2305487/projet/monitoring.db')
    cursor = conn.cursor()

    # Extraire les données de CPU et RAM de la table 'mesures'
    cursor.execute("SELECT valeur, date, sonde FROM mesures WHERE sonde IN ('cpu', 'ram') ORDER BY date DESC LIMIT 60")
    data = cursor.fetchall()

    # Organiser les données pour le graphique
    cpu_values = [float(value) for value, date, sonde in data if sonde == 'cpu']
    ram_values = [float(value) for value, date, sonde in data if sonde == 'ram']
    dates = [date for value, date, sonde in data]

    # Créer le graphique
    line_chart = pygal.Line()
    line_chart.title = 'Utilisation CPU et RAM sur les 60 dernières minutes'
    line_chart.x_labels = dates
    line_chart.add('CPU (%)', cpu_values)
    line_chart.add('RAM (%)', ram_values)

    # Sauvegarder le graphique sous format SVG
    line_chart.render_to_file('graphe.svg')

    # Fermer la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    generate_combined_graph()
