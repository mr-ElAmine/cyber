#!/usr/bin/env bash
set -e

# Se placer dans le dossier de cette story.
cd "$(dirname "$0")"

# Préparer les outils de lecture des traces.
docker compose build analyse

# Préparer le dossier de sortie.
mkdir -p resultats

# Relire les deux essais enregistrés, sans démarrer Windows.
docker compose run --rm -T analyse
