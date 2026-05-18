# SysMon-Alerting : Outil de Supervision Serveur & Veille Cyber Automatisée

##  Description
**SysMon-Alerting** est une solution modulaire et légère développée en Python pour assurer la supervision continue d'un serveur Linux (monitoring) et intégrer un flux de veille sur les cybermenaces. Cet outil collecte en temps réel les métriques de performance du système, les historise dans une base de données SQLite, extrait les dernières alertes de sécurité du CERT-FR (Scraping), génère des visualisations graphiques et déclenche des alertes immédiates par email (SMTP SSL) en cas de surcharge (situation de crise).

Ce projet démontre des compétences clés en **Scripting Python**, **Administration Système Linux**, **Automatisation DevOps**, **Gestion de données (SQL)** et **Cybersécurité**.

---

## Fonctionnalités
- **Supervision des ressources (Monitoring) :** Collecte automatisée de l'utilisation CPU, du disque et du nombre d'utilisateurs actuellement connectés (`psutil`, `subprocess`).
- **Rétention intelligente :** Nettoyage automatique des anciennes mesures pour ne conserver qu'un historique glissant des 60 dernières minutes.
- **Veille cyber (Threat Intel Scraping) :** Récupération automatique et journalisation de la dernière alerte critique publiée sur le site officiel du **CERT-FR** (`requests`, `re`).
- **Gestion des crises & Alerting :** Analyse continue des métriques et envoi instantané d'un email d'alerte basé sur un template textuel en cas de dépassement des seuils critiques.
- **Visualisation de données :** Génération automatique de graphiques temporels au format SVG (`pygal`) illustrant la charge du serveur.
- **Résilience (Backup/Restore) :** Scripts Bash automatisés pour la sauvegarde à chaud et la restauration de la base de données de supervision.

---

## Architecture du Projet
Le projet est structuré de manière modulaire :
- `collect_all.py` : Script principal de collecte des métriques système.
- `cert_parser.py` : Module de scraping pour récupérer le flux d'alertes du CERT-FR.
- `detect_crise.py` : Analyseur de seuils et orchestrateur de l'envoi d'alertes en cas d'anomalie.
- `envoyer_email.py` : Gestionnaire d'expédition des notifications via protocole SMTP sécurisé (SSL).
- `generate_graph.py` : Générateur de graphiques statistiques (`graphe.svg`).
- `db.py` : Couche d'abstraction pour la base de données SQLite (`monitoring.db`).
- `backup.sh` & `restore.sh` : Scripts de maintenance et de sauvegarde de l'infrastructure.
- `template.txt` : Modèle de corps d'email pour les alertes de crise.

---

## Installation & Configuration

### 1. Prérequis
Assurez-vous de disposer de Python 3 et des dépendances nécessaires installées sur votre serveur :
```bash
pip install psutil requests pygal

```

### 2. Configuration SMTP

Modifiez les variables d'en-tête dans `envoyer_email.py` et `detect_crise.py` pour configurer votre serveur de messagerie :

```python
SMTP_SERVER = "votre.serveur.smtp.fr"
SMTP_PORT = 465
EMAIL_FROM = "votre-email@domaine.fr"
EMAIL_TO = "destinataire-alerte@domaine.fr"

```

### 3. Initialisation et exécution

Pour lancer une collecte de métriques et vérifier l'état du système :


python3 collect_all.py
python3 detect_crise.py



### 4. Automatisation (Crontab)

Pour exécuter la surveillance en arrière-plan toutes les minutes, ajoutez les scripts à la crontab de votre serveur :

* * * * * /usr/bin/python3 /chemin/vers/le/projet/collect_all.py
* * * * * /usr/bin/python3 /chemin/vers/le/projet/detect_crise.py
0 * * * * /usr/bin/python3 /chemin/vers/le/projet/generate_graph.py


##  Exemple de Visualisation

L'outil génère un fichier `graphe.svg` dynamique représentant l'évolution de la charge système.


## Licence

Ce projet est distribué sous licence libre. Vous pouvez le réutiliser et le modifier dans le cadre de vos déploiements ou infrastructures de test.


Cette documentation technique met parfaitement en valeur l'interaction entre tes scripts Python, ta base SQLite et tes scripts d'automatisation Bash. Une fois ce fichier enregistré à la racine de ton projet, il s'affichera automatiquement en page d'accueil sur GitHub !

```
