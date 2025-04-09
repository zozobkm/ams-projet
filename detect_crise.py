import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
from datetime import datetime

# Configuration
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EMAIL_FROM = "zohra.belkacem-matallah@alumni.univ-avignon.fr"
EMAIL_TO = "zohra.belkacem-matallah@alumni.univ-avignon.fr"

# Demander le mot de passe dans la console (sécurisé, ne s'affiche pas)
EMAIL_PASSWORD = getpass.getpass(prompt="Entrez votre mot de passe SMTP : ")

# Seuils de crise
SEUIL_CPU = 90.0
SEUIL_RAM = 90.0

# Fonction pour envoyer l'email
def envoyer_email(contenu, destinataire):
    # Créer l'objet du message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = destinataire
    msg['Subject'] = "Alerte AMS - Situation de crise"

    # Ajouter le contenu du mail
    msg.attach(MIMEText(contenu, 'plain'))

    try:
        # Connexion au serveur SMTP et envoi du mail
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)  # Connexion avec ton email et mot de passe
            server.sendmail(EMAIL_FROM, destinataire, msg.as_string())  # Envoi du mail
            print("Mail envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi du mail: {e}")

# Fonction pour détecter une crise
def detecter_crise():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('/home/uapv2202351/data/systeme_monitor.db')
        cursor = conn.cursor()

        # Récupérer les dernières mesures
        cursor.execute("""
            SELECT cpu_usage, ram_usage
            FROM mesures
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        result = cursor.fetchone()

        if result:
            cpu_usage, ram_usage = result
            print(f"CPU : {cpu_usage}% , RAM : {ram_usage}%")

            # Vérifier si les seuils sont dépassés
            if cpu_usage > SEUIL_CPU or ram_usage > SEUIL_RAM:
                alerte_msg = f"CRISE DETECTEE ! CPU={cpu_usage}% et RAM={ram_usage}%"
                print(alerte_msg)
                envoyer_email(alerte_msg, EMAIL_TO)  # Envoyer un mail en cas de crise
            else:
                print("Aucune crise détectée.")
        else:
            print("Aucune donnée trouvée dans la table 'mesures'.")

        # Fermer la connexion
        conn.close()

    except sqlite3.Error as e:
        print(f"Erreur de base de données : {e}")

# Appeler la fonction de détection de crise
if __name__ == "__main__":
    detecter_crise()
