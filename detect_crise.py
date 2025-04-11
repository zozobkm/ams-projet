import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass  # Pour demander le mot de passe de manière sécurisée

# Configuration
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EMAIL_FROM = "zohra.belkacem-matallah@alumni.univ-avignon.fr"  # Remplace par ton adresse mail
EMAIL_TO = "zohra.belkacem-matallah@alumni.univ-avignon.fr"  # L'adresse du destinataire (par exemple, admin)

# Demander le mot de passe dans la console (sécurisé, ne s'affiche pas)
EMAIL_PASSWORD = getpass.getpass(prompt="Entrez votre mot de passe SMTP : ")

# Connexion à la base de données
def detecter_crise():
    try:
        # Connexion à la base de données avec le bon chemin
        conn = sqlite3.connect('/home/uapv2305487/projet/monitoring.db')
        cursor = conn.cursor()

        # Récupérer les dernières valeurs du CPU et de la RAM
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

            # Détection d'une situation de crise (par exemple, si CPU > 0 ou RAM > 0)
            seuil_cpu = 0
            seuil_ram = 1
            if cpu > seuil_cpu or ram > seuil_ram:
                print(f"CRISE DETECTEE ! CPU: {cpu}% | RAM: {ram}%")
                # Envoi de l'email d'alerte
                contenu_email = f"Alerte: Situation de crise détectée.\nCPU: {cpu}%\nRAM: {ram}%"
                envoyer_email(contenu_email, EMAIL_TO)
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
