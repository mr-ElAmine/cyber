#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
mkdir -p resultats

# Lire la copie existante, hors réseau et en lecture seule.
docker compose run --rm -T analyse
