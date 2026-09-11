"""Lire la clé Run dans le registre propre et dans la copie après l’essai."""

import hashlib
from pathlib import Path

from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.regf import RegistryHive

from lire_disque import ouvrir_windows

SNAPSHOT_PROPRE = 'windows-clean-us1'
CLE_RUN = r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'


def lire_run(ntfs):
    entree = ntfs.mft.get('Users/Analyste/NTUSER.DAT')
    with entree.open() as contenu:
        empreinte = hashlib.file_digest(contenu, 'sha256').hexdigest()

    with entree.open() as contenu:
        ruche = RegistryHive(contenu)
        if ruche.in_transaction:
            raise ValueError('La ruche contient une transaction inachevée.')
        cle = ruche.open(r'Software\Microsoft\Windows\CurrentVersion\Run')

        valeurs = {}
        for valeur in cle.values():
            valeurs[valeur.name] = {'type': int(valeur.type), 'donnee': valeur.value}

        return {
            'ruche_sha256': empreinte,
            'sequence1': ruche.header.Sequence1,
            'sequence2': ruche.header.Sequence2,
            'en_transaction': ruche.in_transaction,
            'cle_modifiee_windows_utc': cle.timestamp.isoformat(),
            'valeurs': valeurs,
        }


def lire_etat_propre():
    disque = QCow2(Path('/source/windows.qcow2'))
    for snapshot in disque.snapshots:
        if snapshot.name == SNAPSHOT_PROPRE:
            return lire_run(ouvrir_windows(snapshot.open()))
    raise ValueError(f'Snapshot absent : {SNAPSHOT_PROPRE}.')
