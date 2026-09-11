#!/usr/bin/env bash
set -e

# Se placer dans le dossier qui contient compose.yaml et hashes.py.
cd "$(dirname "$0")"

# Calculer les empreintes et enregistrer le résultat.
docker compose run --rm -T empreintes > hashes.json

# Afficher le fichier obtenu dans le terminal.
cat hashes.json
