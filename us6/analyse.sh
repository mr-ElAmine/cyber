#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"
mkdir -p cache resultats
docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --memory 3g --cpus 2 --pids-limit 64 \
  --volume cyber-windows_windows-disk:/storage:ro \
  --volume "$PWD/../infrastructure/windows/results:/avant:ro" \
  --volume "$PWD:/travail:ro" \
  --volume "$PWD/symboles:/symboles:ro" \
  --volume "$PWD/cache:/cache" \
  --volume "$PWD/resultats:/resultats" \
  cyber-memory-analysis:local python /travail/analyse.py
