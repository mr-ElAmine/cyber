#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Le disque source doit rester stable pendant la lecture du snapshot propre.
vm_en_marche=$(docker inspect --format '{{.State.Running}}' cyber-windows-vm-1)
if [ "$vm_en_marche" != false ]; then
    echo 'Arrête la VM Windows avant de lancer cette analyse.'
    exit 1
fi

mkdir -p resultats
docker inspect --format '{{json .State}}' cyber-windows-vm-1 > resultats/etat-vm.json

# Préparer les bibliothèques Dissect dans Docker.
docker compose build analyse

# Croiser le disque, la mémoire et Process Monitor, hors réseau.
docker compose run --rm -T analyse
