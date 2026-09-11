#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

docker build -t cyber-dynamic-analysis:local .
mkdir -p resultats
docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --memory 768m --pids-limit 32 \
  --volume cyber-windows_windows-disk:/storage:ro \
  --volume "$PWD/analyse.py:/analyse.py:ro" \
  --volume "$PWD/resultats:/resultats" \
  cyber-dynamic-analysis:local python /analyse.py
