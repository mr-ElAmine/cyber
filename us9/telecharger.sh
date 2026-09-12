#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

mkdir -p preuves
docker compose run --rm -T telechargement
