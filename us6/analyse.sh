#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
mkdir -p cache resultats

# Vérifier que les captures sont intactes. Arrêter en cas d’erreur.
docker compose run --rm -T analyse /script/verifier_captures.py

# Lire les processus et les traces réseau avec Volatility, hors réseau.
docker compose run --rm -T analyse /script/analyser_memoire.py
