from db import init_db , insert_mesure, clean_old_mesures
import psutil
import subprocess
init_db()

######cpu=psutil.cpu_percent(interval=1)
cpu = 97
insert_mesure('cpu',str(cpu))


if cpu > 95:
	print("crise :cpu>95%")


##disk = p sutil.disk.usage('/').percent

disk=98
insert_mesure('disque',str(disk))

if disk >95:
	print("crise: disque>95%")

users=subprocess.getoutput("who |wc -l")
insert_mesure('utilisateurs',users)

clean_old_mesures(60)

