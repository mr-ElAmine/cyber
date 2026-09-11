#!/usr/bin/env sh
# Étape 1 : copier le disque du snapshot. Ce script tourne dans Docker.
set -e

disque_source=/storage/windows.qcow2
image_copie=/images/windows-first-run.raw
snapshot=malware-first-run

# Enregistrer la version de QEMU et contrôler le disque sans le réparer.
qemu-img --version > /resultats/qemu-version.txt
qemu-img info --output=json "$disque_source" > /resultats/source.json
qemu-img check --output=json "$disque_source" > /resultats/controle-source.json

# Copier le snapshot en RAW, avec progression (-p).
# -S 4k évite de stocker les blocs de zéros, sans changer le contenu logique.
date -u +%Y-%m-%dT%H:%M:%SZ > /resultats/acquisition-debut.txt
qemu-img convert \
    -p \
    -f qcow2 \
    -l "snapshot.name=$snapshot" \
    -O raw \
    -S 4k \
    "$disque_source" "$image_copie"
date -u +%Y-%m-%dT%H:%M:%SZ > /resultats/acquisition-fin.txt

# Enregistrer le format et la taille de la copie obtenue.
qemu-img info -f raw --output=json "$image_copie" > /resultats/image.json
