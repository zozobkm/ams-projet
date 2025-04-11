from db import init_db, insert_mesure, clean_old_mesures
import psutil
import subprocess

# Initialisation de la base de données
init_db()

# Récupérer la valeur du CPU
cpu = psutil.cpu_percent(interval=1)  # Utilisation du CPU en pourcentage
insert_mesure('cpu', str(cpu))

# Si le CPU dépasse 95%, considérer cela comme une crise
if cpu > 95:
    print("Crise : CPU > 95%")

# Récupérer l'utilisation du disque
disk = psutil.disk_usage('/').percent  # Utilisation du disque
insert_mesure('disque', str(disk))

# Si l'utilisation du disque dépasse 95%, considérer cela comme une crise
if disk > 95:
    print("Crise : Disque > 95%")

# Récupérer le nombre d'utilisateurs connectés
users = subprocess.getoutput("who | wc -l")  # Nombre d'utilisateurs connectés
insert_mesure('utilisateurs', users)

# Nettoyer les anciennes mesures, conserver les 60 dernières minutes
clean_old_mesures(60)

