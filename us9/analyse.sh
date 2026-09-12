#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

mkdir -p resultats

# Installer le lecteur de registre dans Docker.
docker compose build analyse

# Lire l’archive hors réseau, sans la modifier.
docker compose run --rm -T analyse
