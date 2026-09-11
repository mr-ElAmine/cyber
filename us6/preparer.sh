#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Installer Volatility dans l’image Docker.
docker compose build symboles
mkdir -p cache symboles resultats

# Télécharger les symboles Microsoft.
docker compose run --rm -T symboles /script/telecharger_symboles.py

# Les convertir au format attendu par Volatility.
docker compose run --rm -T symboles /script/convertir_symboles.py
