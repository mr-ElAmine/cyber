#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# L’US9 prépare l’image Docker et identifie la clé.
mkdir -p resultats
docker compose run --rm -T analyse
