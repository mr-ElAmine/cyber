"""Contrôler l’archive, puis ouvrir uniquement les trois registres utiles."""

import hashlib
import io
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile

from dissect.regf import RegistryHive

from telecharger import COMMIT, URL

SHA256_ARCHIVE = '591dd24d95ef5021d56f5cc2f58aa0ce5429aea48b7b2dc375ad1356829dd81a'


def lire_archive():
    chemin = Path('/preuves/dump.zip')
    with chemin.open('rb') as fichier:
        empreinte = hashlib.file_digest(fichier, 'sha256').hexdigest()
    if empreinte != SHA256_ARCHIVE:
        raise ValueError('L’archive diffère de celle utilisée pour cette analyse.')

    provenance = {
        'depot': 'https://github.com/Waelmeg/Dump_memoire',
        'commit': COMMIT, 'url': URL,
        'archive_sha256': empreinte, 'archive_octets': chemin.stat().st_size,
        'registres': {},
        'dissect.regf': version('dissect.regf'),
        'limite': 'Fichiers lus tels que fournis ; aucun journal de récupération disponible.',
    }
    registres = {}
    with ZipFile(chemin) as archive:
        provenance['contenu_archive'] = archive.namelist()
        for nom in ('SYSTEM', 'SOFTWARE', 'NTUSER.DAT'):
            contenu = archive.read('dump/' + nom)
            ruche = RegistryHive(io.BytesIO(contenu))
            registres[nom] = ruche
            provenance['registres'][nom] = {
                'sha256': hashlib.sha256(contenu).hexdigest(),
                'octets': len(contenu),
                'sequence1': ruche.header.Sequence1,
                'sequence2': ruche.header.Sequence2,
                'ecriture_inachevee': ruche.in_transaction,
            }
    return registres, provenance
