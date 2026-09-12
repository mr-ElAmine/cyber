"""Télécharger l’archive fournie pour les US9 et US10, sans l’exécuter."""

from pathlib import Path
from urllib.request import urlopen

COMMIT = 'c2741e9bfed329c780a07f230b4ce548ee3806a7'
URL = f'https://raw.githubusercontent.com/Waelmeg/Dump_memoire/{COMMIT}/dump.zip'


def main():
    destination = Path('/preuves/dump.zip')
    temporaire = destination.with_suffix('.part')
    print('Téléchargement de dump.zip…')

    with urlopen(URL, timeout=60) as reponse, temporaire.open('wb') as fichier:
        total = int(reponse.headers['Content-Length'])
        recus = 0
        while bloc := reponse.read(1024 * 1024):
            fichier.write(bloc)
            recus += len(bloc)
            print(f'\r{recus / total:.0%} — {recus / 1024**2:.1f} Mio', end='', flush=True)

    if recus != total:
        raise ValueError('Le téléchargement est incomplet.')
    temporaire.replace(destination)
    print('\nArchive enregistrée dans us9/preuves/dump.zip.')


if __name__ == '__main__':
    main()
