#!/usr/bin/env bash
set -e # Arrêter le script si une commande échoue.

# Retrouver compose.yaml même si le script est lancé depuis un autre dossier.
cd "$(dirname "$0")"

# Démarrer Windows et la console en arrière-plan ; le disque existant est conservé.
docker compose up -d

echo "Ouvre http://127.0.0.1:6085/vnc.html pour accéder à Windows."
