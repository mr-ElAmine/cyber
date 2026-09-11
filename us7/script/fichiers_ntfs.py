"""Parcourir les dossiers Windows et relever les empreintes de leurs fichiers."""

import hashlib
from pathlib import PureWindowsPath

from references import EMPREINTES_US2


def role_fichier(nom):
    if nom in EMPREINTES_US2:
        return 'executable suspect'
    if nom == 'log.txt':
        return 'journal associe au malware'
    if nom.lower().endswith('.dll'):
        return 'bibliotheque accompagnant les executables'
    return 'fichier a examiner'


def relever_fichier(ntfs, chemin, role):
    entree = ntfs.mft.get(chemin)
    with entree.open() as contenu:
        empreinte = hashlib.file_digest(contenu, 'sha256').hexdigest()

    # La comparaison US2 concerne uniquement Res.exe et Env.exe.
    identique = None
    if entree.filename in EMPREINTES_US2:
        identique = empreinte == EMPREINTES_US2[entree.filename]

    return {
        'chemin': str(PureWindowsPath('C:/' + chemin)),
        'octets': entree.size(),
        'sha256': empreinte,
        'role': role,
        'echantillon_us2_identique': identique,
    }


def parcourir_dossier(ntfs, chemin):
    fichiers = []
    dossier = ntfs.mft.get(chemin)

    # Lire les entrées réelles, sans doubler les fichiers avec leurs noms DOS courts.
    for entree in dossier.iterdir(dereference=True, ignore_dos=True):
        enfant = chemin + '/' + entree.filename
        if entree.is_dir():
            fichiers.extend(parcourir_dossier(ntfs, enfant))
        elif entree.is_file():
            role = role_fichier(entree.filename)
            fichiers.append(relever_fichier(ntfs, enfant, role))

    return fichiers
