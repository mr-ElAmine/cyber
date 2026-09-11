"""Lire les relevés JSON, enregistrer les résultats et comparer les chemins Windows."""

import json
from pathlib import Path, PureWindowsPath


def lire_json(chemin):
    return json.loads(Path(chemin).read_text())


def enregistrer_json(nom, donnees):
    texte = json.dumps(donnees, indent=2, ensure_ascii=False)
    Path('/resultats', nom).write_text(texte + '\n')


def normaliser(chemin):
    # Windows ignore la casse ; accepter aussi les slashs et les chemins entre guillemets.
    chemin = chemin.strip('"')
    return str(PureWindowsPath(chemin)).casefold()
