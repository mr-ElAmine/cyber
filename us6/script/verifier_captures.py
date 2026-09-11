"""Étape 3 : vérifier les empreintes et la structure des deux captures RAM."""

import hashlib
import json
from datetime import datetime, timezone

from references import CAPTURES, RESULTATS
from verifier_elf import lire_regions


def verifier_capture(nom, reference):
    chemin = reference['chemin']
    print(f'Vérification de la capture {nom}…', flush=True)

    with chemin.open('rb') as fichier:
        empreinte = hashlib.file_digest(fichier, 'sha256').hexdigest()
    if empreinte != reference['sha256']:
        raise ValueError(f'Capture {nom} : le SHA-256 diffère du relevé initial.')

    regions = lire_regions(chemin)
    print(f'{nom} : empreinte conforme et {len(regions)} régions complètes.', flush=True)
    return {
        'capture': nom,
        'fichier': chemin.name,
        'octets': chemin.stat().st_size,
        'sha256': empreinte,
        'format': 'ELF64 little-endian x86-64 ET_CORE',
        'segments': regions,
        'octets_physiques': sum(region['octets'] for region in regions),
        'segments_declares_complets': True,
    }


def main():
    captures_verifiees = []
    for nom, reference in CAPTURES.items():
        captures_verifiees.append(verifier_capture(nom, reference))

    rapport = {
        'verification_utc': datetime.now(timezone.utc).isoformat(),
        'captures': captures_verifiees,
    }
    (RESULTATS / 'integrite.json').write_text(json.dumps(rapport, indent=2) + '\n')


if __name__ == '__main__':
    main()
