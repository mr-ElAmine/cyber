#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

# Une acquisition se fait VM arretee, sans ecraser une preuve existante.
test "$(docker inspect --format '{{.State.Running}}' cyber-windows-vm-1)" = false
test ! -e images/windows-first-run.raw
mkdir -p images resultats
docker inspect --format '{{json .State}}' cyber-windows-vm-1 > resultats/etat-vm.json
docker build -t cyber-disk-analysis:local .

docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges --memory 768m \
  --volume cyber-windows_windows-disk:/storage:ro \
  --volume "$PWD/images:/images" \
  --volume "$PWD/resultats:/resultats" \
  cyber-windows-vm:local sh -ec '
    qemu-img --version > /resultats/qemu-version.txt
    qemu-img info --output=json /storage/windows.qcow2 > /resultats/source.json
    qemu-img check --output=json /storage/windows.qcow2 > /resultats/controle-source.json
    date -u +%Y-%m-%dT%H:%M:%SZ > /resultats/acquisition-debut.txt
    qemu-img convert -p -f qcow2 -l snapshot.name=malware-first-run \
      -O raw -S 4k /storage/windows.qcow2 /images/windows-first-run.raw
    date -u +%Y-%m-%dT%H:%M:%SZ > /resultats/acquisition-fin.txt
    qemu-img info -f raw --output=json /images/windows-first-run.raw > /resultats/image.json
  '
chmod 0444 images/windows-first-run.raw

docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges --memory 768m --cpus 2 \
  --volume cyber-windows_windows-disk:/storage:ro \
  --volume "$PWD/images:/images:ro" \
  --volume "$PWD/verifier.py:/verifier.py:ro" \
  --volume "$PWD/resultats:/resultats" \
  cyber-disk-analysis:local python /verifier.py
