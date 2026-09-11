"""Étape 1 : contrôler la taille et l’empreinte de l’image conservée en US7."""

import hashlib

from fichiers import lire_json


def verifier_image(image):
    attendu = lire_json('/disque/integrite.json')['sha256_image_raw']
    empreinte = hashlib.sha256()
    octets_lus = 0
    print('Contrôle de l’image disque : 64 Gio à lire…')

    with image.open('rb') as flux:
        while True:
            bloc = flux.read(16 * 1024**2)  # Lire 16 Mio à la fois.
            if not bloc:
                break
            empreinte.update(bloc)
            octets_lus += len(bloc)

            if octets_lus % (8 * 1024**3) == 0:
                print(f'{octets_lus // 1024**3} / 64 Gio contrôlés')

    if octets_lus != 64 * 1024**3:
        raise ValueError('La taille de l’image diffère des 64 Gio attendus.')
    if empreinte.hexdigest() != attendu:
        raise ValueError('Le SHA-256 de l’image diffère du relevé US7.')

    return {'sha256': empreinte.hexdigest(), 'octets': octets_lus}
