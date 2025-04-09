import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass  # Pour demander le mot de passe de manière sécurisée

# Configuration
SMTP_SERVER = "partage.univ-avignon.fr"
SMTP_PORT = 465
EMAIL_FROM = "ton-adresse@univ-avignon.fr"  # Remplace par ton adresse mail
EMAIL_TO = "destinataire@exemple.com"  # L'adresse du destinataire (par exemple, admin)

# Demander le mot de passe dans la console (sécurisé, ne s'affiche pas)
EMAIL_PASSWORD = getpass.getpass(prompt="Entrez votre mot de passe SMTP : ")

# Fonction pour envoyer l'email
def envoyer_email(contenu, destinataire):
    print("Début de l'envoi de l'email.")
    
    # Créer l'objet du message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = destinataire
    msg['Subject'] = "Alerte AMS - Situation de crise"

    # Ajouter le contenu du mail
    msg.attach(MIMEText(contenu, 'plain'))

    try:
        # Connexion au serveur SMTP et envoi du mail
        print("Connexion au serveur SMTP...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            print("Connexion réussie. Tentative de login...")
            server.login(EMAIL_FROM, EMAIL_PASSWORD)  # Connexion avec ton email et mot de passe
            print("Login réussi. Envoi de l'email...")
            server.sendmail(EMAIL_FROM, destinataire, msg.as_string())  # Envoi du mail
            print("Mail envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du mail: {e}")

# Test : Envoi d'un mail de test
envoyer_email("Ceci est un test d'alerte AMS", EMAIL_TO)
