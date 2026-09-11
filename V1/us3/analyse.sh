#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

echo "Construction des outils d'analyse..."
docker build -t cyber-static-analysis:local .

mkdir -p resultats
echo "Analyse des deux EXE, sans reseau et sans les executer..."
docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --memory 512m --pids-limit 32 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  --volume cyber-malware-samples:/samples:ro \
  --volume "$PWD/analyse.py:/analyse.py:ro" \
  --volume "$PWD/resultats:/resultats" \
  cyber-static-analysis:local
