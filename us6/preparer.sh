#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"
docker build -t cyber-memory-analysis:local .
mkdir -p cache symboles resultats
# Ce conteneur telecharge les symboles publics ; aucun dump ne lui est fourni.
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --memory 2g --tmpfs /tmp:uid=1000,gid=1000 \
  --volume "$PWD/cache:/cache" \
  --volume "$PWD/symboles:/symboles" \
  --volume "$PWD/resultats:/resultats" \
  --volume "$PWD/symboles.py:/symboles.py:ro" \
  cyber-memory-analysis:local python /symboles.py
