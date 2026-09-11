#!/usr/bin/env bash
set -e

# Se placer dans le dossier de cette story.
cd "$(dirname "$0")"

# Préparer les outils d'analyse.
echo "Préparation de pefile et objdump..."
docker compose build

# Préparer le dossier de sortie.
mkdir -p resultats

# Lire les exécutables dans le conteneur isolé.
echo "Analyse des fichiers, sans les exécuter..."
docker compose run --rm -T analyse
