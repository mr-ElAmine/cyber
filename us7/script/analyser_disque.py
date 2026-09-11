"""Étape 3 : retrouver les fichiers suspects dans la copie du disque Windows."""

from dissect.ntfs import NTFS
from dissect.volume.disk import Disk

from enregistrer_resultats import enregistrer_inventaire, enregistrer_partitions
from fichiers_ntfs import parcourir_dossier, relever_fichier
from references import IMAGE_RAW


def main():
    with IMAGE_RAW.open('rb') as image:
        disque = Disk(image)
        enregistrer_partitions(disque)

        # Dans notre VM, Windows occupe la plus grande partition du disque.
        partition = max(disque.partitions, key=lambda partition: partition.size)
        ntfs = NTFS(partition.open())

        print('Inventaire du dossier de test et de WindSyst…')
        fichiers = parcourir_dossier(ntfs, 'Lab/sample/virus')
        fichiers.extend(parcourir_dossier(ntfs, 'WindSyst'))

        # Conserver aussi les références de la trace et du registre utilisateur.
        fichiers.append(relever_fichier(
            ntfs, 'Lab/trace.pml', 'trace Process Monitor du laboratoire'))
        fichiers.append(relever_fichier(
            ntfs, 'Users/Analyste/NTUSER.DAT',
            'ruche utilisateur a examiner pour la persistance'))

        enregistrer_inventaire(fichiers, partition.number)

    print(f'Inventaire terminé : {len(fichiers)} fichiers, sans extraction des exécutables.')


if __name__ == '__main__':
    main()
