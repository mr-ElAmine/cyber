"""Étape 2 : convertir les symboles Microsoft au format JSON de Volatility."""

import hashlib
import json
import subprocess
from pathlib import Path

from references import DOSSIER_SYMBOLES, RESULTATS, SERVEUR_MICROSOFT, SYMBOLES


def convertir(nom, identifiant):
    fichier_pdb = DOSSIER_SYMBOLES / nom
    dossier_sortie = DOSSIER_SYMBOLES / 'windows' / nom
    dossier_sortie.mkdir(parents=True, exist_ok=True)
    fichier_json = dossier_sortie / f'{identifiant}.json'

    commande = [
        'python', '-m', 'volatility3.framework.symbols.windows.pdbconv',
        '-f', str(fichier_pdb),  # Symboles Microsoft à lire.
        '-p', nom,              # Nom du PDB : nécessaire pour son identification.
        '-o', str(fichier_json), # Symboles convertis à enregistrer.
    ]
    print(f'Conversion de {nom}…', flush=True)
    with Path('/cache', f'conversion-{nom}.log').open('w') as journal:
        subprocess.run(commande, check=True, stdout=journal, stderr=subprocess.STDOUT)

    empreintes = {}
    for chemin in (fichier_pdb, fichier_json):
        with chemin.open('rb') as fichier:
            empreintes[chemin.name] = hashlib.file_digest(fichier, 'sha256').hexdigest()

    return {
        'url': f'{SERVEUR_MICROSOFT}/{nom}/{identifiant}/{nom}',
        'identifiant_pdb': identifiant,
        'sha256': empreintes,
    }


def main():
    resultats = []
    for nom, identifiant in SYMBOLES.items():
        resultats.append(convertir(nom, identifiant))

    (RESULTATS / 'symboles.json').write_text(json.dumps(resultats, indent=2) + '\n')
    print('Symboles prêts pour l’analyse hors réseau.')


if __name__ == '__main__':
    main()
