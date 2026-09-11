#!/usr/bin/env bash
set -e

# Se placer dans le dossier de cette story.
cd "$(dirname "$0")"

# Regrouper l'archive, les outils et les scripts dans un DVD virtuel.
docker compose run --rm -T dvd

echo "DVD créé : infrastructure/windows/media/us4.iso"
