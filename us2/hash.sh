#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

# L'image de la console contient déjà Python.
docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --memory 128m --pids-limit 32 \
  --volume cyber-malware-samples:/samples:ro \
  --volume "$PWD/hashes.py:/hashes.py:ro" \
  cyber-windows-console:local python3 /hashes.py | tee hashes.json
