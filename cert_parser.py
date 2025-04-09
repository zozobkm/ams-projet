import re
import requests
from db import init_alerts_table , insert_alert, delete_old_alerts
from datetime import datetime

def get_lastcert_alert():
	url = "https://www.cert.ssi.gouv.fr/"
	reponse = requests.get(url)
	

	match = re.search(r'< div class_="last_alert">(.*?)</div>',reponse.text, re.DOTALL)

	if match:
		alert_text = match.group(1).strip()
		return alert_text

	return "Aucune alerte trouvee"


def store_alert():
	init_alerts_table()
	delete_old_alerts()
	alert = get_lastcert_alert()
	insert_alert(alert)
	

if __name__ == "__main__":
	store_alert()
