"""US9 : lire la source, identifier la clé, puis retrouver son volume."""

import json
from datetime import datetime, timezone
from pathlib import Path

from identifier_usb import identifier_usb
from lire_archive import lire_archive
from registre import valeur
from relier_volume import relier_volume


def main():
    print('1. Vérification de l’archive et lecture du registre.')
    registres, provenance = lire_archive()

    print('2. Identification du stockage USB.')
    controle, appareils = identifier_usb(registres['SYSTEM'])

    print('3. Recherche du volume et de sa lettre.')
    for appareil in appareils:
        appareil.update(relier_volume(registres, appareil))
        print(f"{appareil['modele']} — {appareil['numero_serie']}")

    fuseau = registres['SYSTEM'].open(controle + r'\Control\TimeZoneInformation')
    resultat = {
        'control_set': controle,
        'fuseau_windows': valeur(fuseau, 'TimeZoneKeyName'),
        'appareils': appareils,
        'critere_uid_extrait': bool(appareils),
        'limite': 'Identifiants lus dans le registre ; propriétaire et fuite non établis.',
    }
    provenance['analyse_utc'] = datetime.now(timezone.utc).isoformat()
    for nom, donnees in [('usb.json', resultat), ('provenance.json', provenance)]:
        texte = json.dumps(donnees, ensure_ascii=False, indent=2)
        Path('/resultats', nom).write_text(texte + '\n', encoding='utf-8')
    print('Résultats enregistrés dans us9/resultats/.')


if __name__ == '__main__':
    main()
