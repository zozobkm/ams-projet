from db import init_db , insert_mesure, clean_old_mesures
from db import init_alerts_table , insert_alert, delete_old_alerts
from datetime import datetime
from envoyer_email import envoyer_email
import psutil
# Initialisation de la base de données
init_db()

def detecter_crise():
    """Détecte une situation de crise basée sur les mesures du CPU et de la RAM."""
    result = get_last_measurements()

    if result:
        # Extraction des valeurs CPU et RAM
        cpu = next((float(value) for sonde, value in result if sonde == 'cpu'), None)
        ram = next((float(value) for sonde, value in result if sonde == 'ram'), None)

        print(f"Dernière utilisation CPU: {cpu}% et RAM: {ram}%")

        # Seuils de crise
        seuil_cpu = 80
        seuil_ram = 80

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

if __name__ == "__main__":
    detecter_crise()
