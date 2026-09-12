"""Lire les dates des propriétés Windows, sans confondre installation et connexion."""

from datetime import datetime, timedelta, timezone

from registre import GUID_PROPRIETES, lire_propriete

# Identifiants définis dans devpkey.h, exprimés ici en hexadécimal.
PROPRIETES = {
    '0064': 'derniere_installation',
    '0065': 'premiere_installation',
    '0066': 'derniere_connexion',
    '0067': 'dernier_retrait',
}


def convertir_filetime(donnee):
    if not isinstance(donnee, bytes) or len(donnee) != 8:
        raise ValueError('Une date FILETIME doit contenir exactement 8 octets.')
    compteur = int.from_bytes(donnee, 'little')
    if compteur == 0:
        return None

    # FILETIME compte les intervalles de 100 ns depuis le 1er janvier 1601 UTC.
    secondes, fraction = divmod(compteur, 10_000_000)
    date = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=secondes)
    texte = date.strftime('%Y-%m-%dT%H:%M:%S') + f'.{fraction:07d}+00:00'
    return texte


def lire_dates(systeme, appareil):
    evenements = []
    for champ in ('cle_usb', 'cle_usbstor'):
        chemin = appareil[champ]
        for numero, nature in PROPRIETES.items():
            donnee = lire_propriete(systeme, chemin, numero)
            if donnee is None:
                continue
            date = convertir_filetime(donnee)
            if date is None:
                continue
            evenements.append({
                'date_utc': date,
                'evenement': nature,
                'numero_serie': appareil['numero_serie'],
                'registre': 'SYSTEM',
                'cle': chemin + '\\Properties\\' + GUID_PROPRIETES + '\\' + numero,
                'valeur': '(Default)',
                'donnee_hex': donnee.hex(),
                'precision': '100 ns dans la valeur ; exactitude de l’horloge non vérifiée.',
            })

    for trace in appareil['traces_profil']:
        evenements.append({
            'date_utc': trace['derniere_modification_utc'],
            'evenement': 'modification_mountpoints2',
            'numero_serie': appareil['numero_serie'],
            'registre': trace['registre'],
            'cle': trace['cle'],
            'valeur': 'Horodatage de la clé',
            'donnee_hex': '',
            'precision': 'Dernière modification de la clé ; ne date pas une copie de fichiers.',
        })
    return evenements
