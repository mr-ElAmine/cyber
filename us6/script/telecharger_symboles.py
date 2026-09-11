"""Étape 1 : télécharger les deux fichiers de symboles Microsoft."""

from urllib.request import urlopen

from references import DOSSIER_SYMBOLES, SERVEUR_MICROSOFT, SYMBOLES


def telecharger(url, destination):
    print(f'Téléchargement de {destination.name}…', flush=True)

    with urlopen(url, timeout=60) as reponse, destination.open('wb') as fichier:
        taille_totale = int(reponse.headers.get('Content-Length', 0))
        octets_recus = 0

        while True:
            bloc = reponse.read(1024 * 1024)
            if not bloc:
                break

            fichier.write(bloc)
            octets_recus += len(bloc)
            progression = f'{octets_recus / 1024**2:.1f} Mio reçus'
            if taille_totale > 0:
                progression += f' sur {taille_totale / 1024**2:.1f} Mio'
            print('\r' + progression, end='', flush=True)

    print()


def main():
    for nom, identifiant in SYMBOLES.items():
        url = f'{SERVEUR_MICROSOFT}/{nom}/{identifiant}/{nom}'
        telecharger(url, DOSSIER_SYMBOLES / nom)

    print('Téléchargements terminés. Les fichiers sont dans symboles/.')


if __name__ == '__main__':
    main()
