#! /bin/bash

if [ -f backup.db ]; then
	cp backup.db monitoring.db
	echo "restauration faites"

else
	echo "aucune sauvegardes"

fi
