#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges --memory 768m \
  --volume "$PWD/images:/images:ro" \
  --volume "$PWD/analyse.py:/analyse.py:ro" \
  --volume "$PWD/resultats:/resultats" \
  cyber-disk-analysis:local python /analyse.py
