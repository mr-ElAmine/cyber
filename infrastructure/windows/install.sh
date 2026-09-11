#!/usr/bin/env bash
set -e # Arrêter le script si une commande échoue.

cd "$(dirname "$0")"

# Première installation uniquement : ce script recrée le disque Windows.
# Télécharger Windows.
python3 download_windows.py

# Construire les images Docker.
docker compose build

# Créer le disque Windows dans Docker.
docker compose run --rm --no-deps vm qemu-img create -f qcow2 /storage/windows.qcow2 64G

# Démarrer la VM et sa console.
docker compose up -d

echo "Ouvre http://127.0.0.1:6085/vnc.html pour accéder à Windows."
