from db import init_db, insert_mesure, clean_old_mesures
from db import init_alerts_table, insert_alert, delete_old_alerts
from datetime import datetime
from envoyer_email import envoyer_email
import psutil
import sqlite3  # Assurez-vous d'importer sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialisation de la base de données
init_db()

def detecter_crise():
    try:
        # Connexion à la base de données avec le bon chemin
        conn = sqlite3.connect('/home/uapv2305487/projet/monitoring.db')
        cursor = conn.cursor()

        # Interroger la table "mesures" pour récupérer les dernières valeurs de CPU et RAM
        cursor.execute("""
        SELECT sonde, valeur
        FROM mesures
        WHERE sonde IN ('cpu', 'ram')
        ORDER BY date DESC
        LIMIT 2;
        """)
        result = cursor.fetchall()

        if result:
            # Les deux premières lignes devraient être CPU et RAM
            cpu = next((value for sonde, value in result if sonde == 'cpu'), None)
            ram = next((value for sonde, value in result if sonde == 'ram'), None)

            # Convertir les valeurs en float pour éviter l'erreur de type
            cpu = float(cpu) if cpu is not None else 0
            ram = float(ram) if ram is not None else 0

            print(f"Dernière utilisation CPU: {cpu}% et RAM: {ram}%")

            # Seuils de crise
            seuil_cpu = 0
            seuil_ram = 1

            if cpu >= seuil_cpu or ram >= seuil_ram:
                print(f"CRISE DETECTEE ! CPU: {cpu}% | RAM: {ram}%")
                # Envoi de l'email d'alerte
                contenu_email = f"Alerte: Situation de crise détectée.\nCPU: {cpu}%\nRAM: {ram}%"
                insert_alert(f"CRISE DETECTEE ! CPU: {cpu}% | RAM: {ram}%")
                envoyer_email(contenu_email, "zohra.belkacem-matallah@alumni.univ-avignon.fr")
            else:
                print("Aucune crise détectée.")
        else:
            print("Aucune donnée disponible pour la détection de crise.")
        
        conn.close()

    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")

# Fonction pour envoyer l'email
def envoyer_email(contenu, destinataire):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = destinataire
    msg['Subject'] = "Alerte AMS - Situation de crise"

    msg.attach(MIMEText(contenu, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, destinataire, msg.as_string())
            print("Mail envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi du mail: {e}")

if __name__ == "__main__":
    detecter_crise()
