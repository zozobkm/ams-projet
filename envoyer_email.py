import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EMAIL_FROM = "ton-adresse@univ-avignon.fr"  # Remplace par ton adresse mail
EMAIL_TO = "destinataire@exemple.com"  # L'adresse du destinataire (par exemple, admin)
EMAIL_PASSWORD = "ton-mot-de-passe-ici"  # Ton mot de passe

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
