"""Lancer une lecture Volatility et conserver son résultat et son journal."""

import json
import subprocess
from datetime import datetime, timezone

from references import CAPTURES, DOSSIER_SYMBOLES, RESULTATS


def lancer_volatility(capture, plugin, commandes, pid=None):
    fichier_capture = CAPTURES[capture]['chemin']
    nom_resultat = f'{capture}-{plugin}'
    fichier_resultat = RESULTATS / f'{nom_resultat}.json'
    fichier_journal = RESULTATS / f'{nom_resultat}.log'

    commande = [
        'vol',
        '--offline',                 # Aucun téléchargement pendant l’analyse.
        '-q',                        # Désactiver la progression de Volatility.
        '-s', str(DOSSIER_SYMBOLES), # Symboles déjà préparés.
        '-r', 'json',                # Résultats structurés.
        '-f', str(fichier_capture),  # Capture à lire.
        'windows.' + plugin,         # Type de lecture demandé.
    ]
    if not commandes:
        # Au premier appel, reconstruire le cache avec les symboles actuels.
        commande.insert(1, '--clear-cache')
    if pid is not None:
        commande += ['--pid', str(pid)]

    print(f'{capture} : lecture {plugin}…', flush=True)
    debut = datetime.now(timezone.utc).isoformat()
    with fichier_resultat.open('w') as resultat, fichier_journal.open('w') as journal:
        retour = subprocess.run(commande, stdout=resultat, stderr=journal)

    commandes.append({
        'commande': commande,
        'debut_utc': debut,
        'fin_utc': datetime.now(timezone.utc).isoformat(),
        'code_sortie': retour.returncode,
    })
    (RESULTATS / 'commandes.json').write_text(json.dumps(commandes, indent=2) + '\n')

    retour.check_returncode()
    # Volatility peut écrire ERROR dans son journal tout en retournant le code 0.
    for ligne in fichier_journal.read_text().splitlines():
        if ligne.startswith('ERROR'):
            raise RuntimeError(f'Échec de {nom_resultat} : consulter {fichier_journal}.')
    json.loads(fichier_resultat.read_text())
