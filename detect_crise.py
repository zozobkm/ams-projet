import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import sqlite3

# Configuration du serveur SMTP
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EMAIL_FROM = "zohra.belkacem-matallah@alumni.univ-avignon.fr"
EMAIL_TO = "zohra.belkacem-matallah@alumni.univ-avignon.fr"

# Demander le mot de passe du mail dans la console
EMAIL_PASSWORD = getpass.getpass(prompt="Entrez votre mot de passe SMTP : ")

# Fonction pour envoyer un email
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


# Fonction pour récupérer les données CPU/RAM et vérifier si une alerte est nécessaire
def detecter_crise():
    SEUIL_CPU = 80.0  # seuil d'alerte pour le CPU
    SEUIL_RAM = 90.0  # seuil d'alerte pour la RAM

    # Connexion à la base de données
    conn = sqlite3.connect('/home/uapv2202351/data/systeme_monitor.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT timestamps, cpu_usage, ram_usage FROM system_metrics 
    ORDER BY timestamps DESC LIMIT 1
    """)
    
    result = cursor.fetchone()
    conn.close()

    if result:
        timestamp, cpu, ram = result
        # Vérification des seuils
        if cpu > SEUIL_CPU or ram > SEUIL_RAM:
            message = f"Alerte AMS : Situation de crise détectée !\n\nDétails de la crise:\nTemps: {timestamp}\nCPU: {cpu}%\nRAM: {ram}%"
            envoyer_email(message, EMAIL_TO)  # Envoi du mail si alerte
        else:
            print("Aucune alerte détectée.")
    else:
        print("Aucune donnée disponible.")


# Appel de la fonction de détection de crise
if __name__ == "__main__":
    detecter_crise()
