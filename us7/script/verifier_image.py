"""Étape 2 : vérifier que la copie RAW contient exactement le disque du snapshot."""

import json
from datetime import datetime, timezone

from dissect.hypervisor.disk.qcow2 import QCow2

from comparer_disques import comparer
from references import DISQUE_SOURCE, IMAGE_RAW, RESULTATS, SNAPSHOT, TAILLE_DISQUE


def retrouver_snapshot(disque):
    for snapshot in disque.snapshots:
        if snapshot.name == SNAPSHOT:
            return snapshot
    raise ValueError(f'Snapshot absent : {SNAPSHOT}.')


def main():
    debut = datetime.now(timezone.utc).isoformat()
    disque = QCow2(DISQUE_SOURCE)
    snapshot = retrouver_snapshot(disque)
    source = snapshot.open()

    if source.size != TAILLE_DISQUE or IMAGE_RAW.stat().st_size != TAILLE_DISQUE:
        raise ValueError('Le snapshot et la copie doivent mesurer chacun 64 Gio.')

    with IMAGE_RAW.open('rb') as copie:
        comparaison = comparer(source, copie, TAILLE_DISQUE)

    rapport = {
        'debut_verification_utc': debut,
        'fin_verification_utc': datetime.now(timezone.utc).isoformat(),
        'source': 'cyber-windows_windows-disk:/windows.qcow2',
        'snapshot': snapshot.name,
        'snapshot_id': snapshot.id,
        'image': IMAGE_RAW.name,
        'octets_compares': comparaison['octets_compares'],
        'sha256_source_logique': comparaison['sha256_source_logique'],
        'sha256_image_raw': comparaison['sha256_image_raw'],
        'identique_octet_par_octet': True,
        'methode': 'Lecture du snapshot avec Dissect et de la copie RAW, comparaison integrale par blocs de 16 Mio.',
    }
    (RESULTATS / 'integrite.json').write_text(json.dumps(rapport, indent=2) + '\n')

    empreinte = comparaison['sha256_image_raw']
    (RESULTATS / 'SHA256SUMS').write_text(f'{empreinte}  {IMAGE_RAW.name}\n')
    print(f'Copie conforme sur les 64 Gio. SHA-256 : {empreinte}')


if __name__ == '__main__':
    main()
