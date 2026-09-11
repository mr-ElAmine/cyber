"""Étape 4 : comparer l’état de Windows avant et pendant le premier essai."""

import json
from importlib.metadata import version

from references import PID_RES, RESULTATS
from volatility import lancer_volatility


def main():
    commandes = []

    # Avant : système Windows, processus présents et traces réseau.
    lancer_volatility('avant', 'info', commandes)     # Version de Windows et de la capture.
    lancer_volatility('avant', 'pslist', commandes)   # Liste des processus.
    lancer_volatility('avant', 'netscan', commandes)  # Traces de connexions dans la RAM.

    # Après : même lecture, complétée par un scan des processus et le suivi réseau.
    lancer_volatility('apres', 'info', commandes)
    lancer_volatility('apres', 'pslist', commandes)
    # Chercher aussi les traces de processus déjà terminés.
    lancer_volatility('apres', 'psscan', commandes)
    lancer_volatility('apres', 'netscan', commandes)
    # Lire les structures réseau suivies par Windows.
    lancer_volatility('apres', 'netstat', commandes)

    # Pour Res.exe : retrouver sa commande de lancement et ses modules chargés.
    lancer_volatility('apres', 'cmdline', commandes, pid=PID_RES)
    lancer_volatility('apres', 'dlllist', commandes, pid=PID_RES)

    versions = {}
    for outil in ('volatility3', 'pyelftools', 'pefile', 'jsonschema'):
        versions[outil] = version(outil)
    (RESULTATS / 'versions.json').write_text(json.dumps(versions, indent=2) + '\n')
    print('Analyse terminée. Les relevés sont dans resultats/.')


if __name__ == '__main__':
    main()
