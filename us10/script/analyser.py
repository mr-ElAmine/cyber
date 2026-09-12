"""US10 : relire les preuves, extraire les dates et remettre les traces dans l’ordre."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from enregistrer import enregistrer
from identifier_usb import identifier_usb
from lire_archive import lire_archive
from lire_dates import lire_dates
from relier_volume import relier_volume


def ordre_chronologique(evenement):
    # Compléter les fractions de seconde, sans perdre les intervalles de 100 ns.
    date = evenement['date_utc'].removesuffix('+00:00')
    return date.ljust(27, '0')


def main():
    print('1. Vérification de la source et de l’identification US9.')
    registres, provenance = lire_archive()
    _, appareils = identifier_usb(registres['SYSTEM'])
    for appareil in appareils:
        appareil.update(relier_volume(registres, appareil))
    fichier_us9 = Path('/identification/usb.json').read_bytes()
    identification = json.loads(fichier_us9)
    if appareils != identification['appareils']:
        raise ValueError('Les résultats US9 ne correspondent plus au registre fourni.')

    print('2. Lecture des dates de la clé USB.')
    evenements = []
    for appareil in appareils:
        evenements.extend(lire_dates(registres['SYSTEM'], appareil))

    evenements.sort(key=ordre_chronologique)
    dates = {evenement['evenement'] for evenement in evenements}
    bilan = {
        'nombre_traces': len(evenements),
        'horloge': 'Dates du poste étudié, en UTC ; indépendantes du laboratoire des US1 à US8.',
        'fuseau_windows': identification['fuseau_windows'],
        'premiere_installation_extraite': 'premiere_installation' in dates,
        'derniere_connexion_extraite': 'derniere_connexion' in dates,
        'dernier_retrait_extrait': 'dernier_retrait' in dates,
        'fuite_demontree': False,
        'concordance_avec_fuite': 'Non vérifiable : aucune date supposée de fuite fournie.',
        'limite': 'Registres avec écriture inachevée, sans journaux de récupération. Historique non exhaustif.',
    }
    provenance['analyse_utc'] = datetime.now(timezone.utc).isoformat()
    provenance['us9_usb_json_sha256'] = hashlib.sha256(fichier_us9).hexdigest()
    print('3. Enregistrement de la chronologie et des preuves.')
    enregistrer(evenements, bilan, provenance)
    print(f'{len(evenements)} traces enregistrées dans us10/resultats/.')


if __name__ == '__main__':
    main()
