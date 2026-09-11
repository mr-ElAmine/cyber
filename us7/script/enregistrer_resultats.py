"""Enregistrer les partitions et l’inventaire dans les fichiers JSON et CSV."""

import csv
import json
from datetime import datetime, timezone
from importlib.metadata import version

from references import IMAGE_RAW, RESULTATS


def enregistrer_partitions(disque):
    partitions = []
    for partition in disque.partitions:
        partitions.append({
            'numero': partition.number,
            'offset_octets': partition.offset,
            'octets': partition.size,
            'type': str(partition.type),
            'nom': partition.name,
        })
    (RESULTATS / 'partitions.json').write_text(json.dumps(partitions, indent=2) + '\n')


def enregistrer_inventaire(fichiers, numero_partition):
    fichiers.sort(key=lambda fichier: fichier['chemin'].lower())
    colonnes = ['chemin', 'octets', 'sha256', 'role', 'echantillon_us2_identique']

    with (RESULTATS / 'fichiers.csv').open('w', newline='') as sortie:
        tableau = csv.DictWriter(sortie, fieldnames=colonnes)
        tableau.writeheader()
        tableau.writerows(fichiers)

    versions = {}
    for outil in ('dissect.hypervisor', 'dissect.volume', 'dissect.ntfs'):
        versions[outil] = version(outil)

    rapport = {
        'analyse_utc': datetime.now(timezone.utc).isoformat(),
        'image': IMAGE_RAW.name,
        'partition_windows': numero_partition,
        'versions': versions,
        'fichiers': fichiers,
    }
    texte = json.dumps(rapport, indent=2, ensure_ascii=False)
    (RESULTATS / 'analyse.json').write_text(texte + '\n')
