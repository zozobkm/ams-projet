import re
import requests
from db import init_alerts_table, insert_alert, delete_old_alerts  # Assurez-vous que 'db' est correctement importé
from datetime import datetime

def get_lastcert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    reponse = requests.get(url)

    # Rechercher la dernière alerte dans le contenu HTML
    match = re.search(r'<div class="last_alert">(.*?)</div>', reponse.text, re.DOTALL)

    if match:
        alert_text = match.group(1).strip()
        return alert_text
    return "Aucune alerte trouvée"

def store_alert():
    # Initialisation de la table et suppression des anciennes alertes
    init_alerts_table()  # Assurez-vous que cette fonction existe dans db.py
    delete_old_alerts()  # Assurez-vous que cette fonction existe dans db.py

    # Récupérer la dernière alerte
    alert = get_lastcert_alert()

    # Insertion de l'alerte dans la base de données
    insert_alert(alert)  # Assurez-vous que cette fonction existe dans db.py

if __name__ == "__main__":
    store_alert()
