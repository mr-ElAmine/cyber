#!/usr/bin/env bash
set -e # Arrêter le script si une commande échoue.

# Les commandes suivantes utilisent les fichiers de ce dossier.
cd "$(dirname "$0")"

# Première installation uniquement : ce script recrée le disque Windows.
# Récupérer le DVD d'installation de Windows, avec sa progression.
python3 download_windows.py

# Préparer les outils : QEMU pour la VM, noVNC pour son affichage.
docker compose build

# Créer un disque QCOW2 de 64 Gio dans le volume réservé à Windows.
docker compose run --rm --no-deps vm qemu-img create -f qcow2 /storage/windows.qcow2 64G

# Ouvrir la VM et sa console pour poursuivre l'installation dans Windows.
docker compose up -d

echo "Ouvre http://127.0.0.1:6085/vnc.html pour accéder à Windows."
