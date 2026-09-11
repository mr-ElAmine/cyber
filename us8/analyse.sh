#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

# Le snapshot de reference est lu avec la VM arretee.
test "$(docker inspect --format '{{.State.Running}}' cyber-windows-vm-1)" = false
mkdir -p resultats
docker build -t cyber-correlation:local .
docker inspect --format '{{json .State}}' cyber-windows-vm-1 > resultats/etat-vm.json
docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges --memory 768m --cpus 2 \
  --volume cyber-windows_windows-disk:/source:ro \
  --volume "$PWD/../us7/images:/images:ro" \
  --volume "$PWD/../us7/resultats:/disque:ro" \
  --volume "$PWD/../us6/resultats:/ram:ro" \
  --volume "$PWD/../us4/resultats:/dynamique:ro" \
  --volume "$PWD/analyse.py:/analyse.py:ro" \
  --volume "$PWD/resultats:/resultats" \
  cyber-correlation:local python /analyse.py
