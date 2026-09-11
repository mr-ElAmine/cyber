"""Conserver les événements retenus et les références des données utilisées."""

import csv
import hashlib
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from fichiers import enregistrer_json


def enregistrer_evenements(evenements):
    colonnes = [
        'evenement', 'heure_windows_utc', 'filetime', 'pid', 'processus',
        'classe', 'operation', 'chemin', 'resultat_ntstatus', 'details',
    ]
    with Path('/resultats/evenements.csv').open('w', newline='') as sortie:
        tableau = csv.DictWriter(sortie, fieldnames=colonnes)
        tableau.writeheader()
        tableau.writerows(evenements)


def enregistrer_provenance(debut, controle_image, fichiers):
    # Ces empreintes identifient les relevés utilisés pour la comparaison.
    sources = [
        '/ram/avant-pslist.json',
        '/ram/apres-pslist.json',
        '/ram/apres-psscan.json',
        '/ram/apres-cmdline.json',
        '/ram/apres-dlllist.json',
        '/ram/integrite.json',
        '/ram/apres-info.json',
        '/ram/acquisition.json',
        '/disque/analyse.json',
        '/disque/integrite.json',
        '/dynamique/resume.json',
        '/dynamique/evenements.csv',
    ]
    empreintes = {}
    for chemin in sources:
        with Path(chemin).open('rb') as contenu:
            empreintes[chemin] = hashlib.file_digest(contenu, 'sha256').hexdigest()

    versions = {}
    for outil in ('dissect.hypervisor', 'dissect.volume', 'dissect.ntfs', 'dissect.regf'):
        versions[outil] = version(outil)

    enregistrer_json('provenance.json', {
        'debut_utc': debut,
        'fin_utc': datetime.now(timezone.utc).isoformat(),
        'image_raw_sha256_recalcule': controle_image['sha256'],
        'image_raw_octets': controle_image['octets'],
        'fichiers_disque_relus': list(fichiers.values()),
        'sha256_resultats_utilises': empreintes,
        'memoire': 'Resultats Volatility reutilises de l US6 ; aucune nouvelle extraction RAM.',
        'versions': versions,
    })
