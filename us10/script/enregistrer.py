"""Conserver la chronologie lisible et les sources qui permettent de la vérifier."""

import csv
import json
from pathlib import Path


def enregistrer(evenements, bilan, provenance):
    colonnes = ['date_utc', 'evenement', 'numero_serie', 'registre', 'cle',
                'valeur', 'donnee_hex', 'precision']
    with Path('/resultats/chronologie.csv').open('w', newline='', encoding='utf-8') as fichier:
        tableau = csv.DictWriter(fichier, fieldnames=colonnes)
        tableau.writeheader()
        tableau.writerows(evenements)

    for nom, donnees in [('bilan.json', bilan), ('provenance.json', provenance)]:
        texte = json.dumps(donnees, ensure_ascii=False, indent=2)
        Path('/resultats', nom).write_text(texte + '\n', encoding='utf-8')
