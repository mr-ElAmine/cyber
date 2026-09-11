#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Le disque source doit rester stable pendant la copie.
vm_en_marche=$(docker inspect --format '{{.State.Running}}' cyber-windows-vm-1)
if [ "$vm_en_marche" != false ]; then
    echo 'Arrête la VM Windows avant de lancer l’acquisition.'
    exit 1
fi

# Ne pas remplacer une image déjà conservée.
if [ -e images/windows-first-run.raw ]; then
    echo 'L’image existe déjà. Pour la lire, lance bash us7/analyse.sh depuis le projet.'
    exit 1
fi

mkdir -p images resultats
docker inspect --format '{{json .State}}' cyber-windows-vm-1 > resultats/etat-vm.json
docker compose build analyse

# Copier le snapshot, puis protéger la copie en lecture seule.
docker compose run --rm -T acquisition
chmod 0444 images/windows-first-run.raw

# Comparer tous les octets de la copie à ceux du snapshot.
docker compose run --rm -T verification
