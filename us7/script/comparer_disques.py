"""Comparer le contenu du snapshot et de la copie, sans tout charger en RAM."""

import hashlib

from references import TAILLE_BLOC


def comparer(source, copie, taille):
    empreinte_source = hashlib.sha256()
    empreinte_copie = hashlib.sha256()
    octets_compares = 0

    while octets_compares < taille:
        bloc_source = source.read(TAILLE_BLOC)
        if not bloc_source:
            raise ValueError('Le snapshot se termine avant la taille attendue.')

        bloc_copie = copie.read(len(bloc_source))
        if bloc_source != bloc_copie:
            raise ValueError(f'Différence à partir de l’octet {octets_compares}.')

        empreinte_source.update(bloc_source)
        empreinte_copie.update(bloc_copie)
        octets_compares += len(bloc_source)

        # Afficher la progression à chaque Gio comparé.
        if octets_compares % (1024**3) == 0:
            print(f'Comparaison : {octets_compares / 1024**3:.0f} / {taille / 1024**3:.0f} Gio')

    if octets_compares != taille or copie.read(1) != b'':
        raise ValueError('Le contenu dépasse la taille attendue du disque.')

    return {
        'octets_compares': octets_compares,
        'sha256_source_logique': empreinte_source.hexdigest(),
        'sha256_image_raw': empreinte_copie.hexdigest(),
    }
