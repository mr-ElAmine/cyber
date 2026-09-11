#!/usr/bin/env bash
set -e # Arrêter le script si une commande échoue.

cd "$(dirname "$0")"

# Démarrer la VM et sa console.
docker compose up -d

echo "Ouvre http://127.0.0.1:6085/vnc.html pour accéder à Windows."
