import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass  # Pour demander le mot de passe de manière sécurisée

# Configuration
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EMAIL_FROM = "zohra.belkacem-matallah@alumni.univ-avignon.fr"  # Remplace par ton adresse mail
EMAIL_TO = "zohra.belkacem-matallah@alumni.univ-avignon.fr"  # L'adresse du destinataire

# Demander le mot de passe dans la console (sécurisé, ne s'affiche pas)
EMAIL_PASSWORD = getpass.getpass(prompt="Entrez votre mot de passe SMTP : ")

def envoyer_email(contenu, destinataire):
    """Envoie un email d'alerte."""
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
