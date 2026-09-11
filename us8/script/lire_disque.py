"""Relire les sept fichiers utiles et vérifier leurs empreintes contre l’US7."""

import hashlib
from pathlib import PureWindowsPath

from dissect.ntfs import NTFS
from dissect.volume.disk import Disk

from fichiers import lire_json, normaliser


def ouvrir_windows(flux):
    disque = Disk(flux)
    # Dans cette VM, Windows occupe la plus grande partition.
    partition = max(disque.partitions, key=lambda partition: partition.size)
    return NTFS(partition.open())


def relever_fichiers(ntfs):
    fichiers = {}
    noms_utiles = ('res.exe', 'env.exe', 'log.txt', 'ntuser.dat', 'trace.pml')

    for reference in lire_json('/disque/analyse.json')['fichiers']:
        chemin = PureWindowsPath(reference['chemin'])
        if chemin.name.lower() not in noms_utiles:
            continue

        # Dissect attend le chemin sans la lettre du lecteur C:.
        chemin_ntfs = '/'.join(chemin.parts[1:])
        entree = ntfs.mft.get(chemin_ntfs)
        with entree.open() as contenu:
            empreinte = hashlib.file_digest(contenu, 'sha256').hexdigest()

        if empreinte != reference['sha256'] or entree.size() != reference['octets']:
            raise ValueError(f'Le fichier {chemin} diffère du relevé US7.')

        fichiers[normaliser(str(chemin))] = {
            'chemin': str(chemin),
            'octets': entree.size(),
            'sha256': empreinte,
        }
    return fichiers
