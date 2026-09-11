"""Confirmer le même lancement de Res.exe dans la RAM et dans Process Monitor."""

import json
from datetime import datetime

from fichiers import normaliser


def verifier_lancement(correlation_res, evenements):
    processus = correlation_res['processus_ram_apres']
    if len(processus) != 1:
        raise ValueError('Un seul processus Res.exe est attendu dans la RAM après essai.')
    res = processus[0]
    if res['PID'] != 6064 or res['ExitTime'] is not None:
        raise ValueError('Le processus attendu est Res.exe, PID 6064, encore actif.')

    if not correlation_res['chemin_ram_retrouve_sur_disque']:
        raise ValueError('Le chemin du module en RAM est absent de l’inventaire disque.')
    chemin_attendu = normaliser(correlation_res['fichier_lancement']['chemin'])
    for commande in correlation_res['commandes_ram']:
        if normaliser(commande) != chemin_attendu:
            raise ValueError('La commande en RAM désigne un autre exécutable.')

    demarrage = None
    for evenement in evenements:
        if evenement['operation'] == 'Process_Start' and evenement['pid'] == '6064':
            demarrage = evenement
            break
    if demarrage is None:
        raise ValueError('Le lancement du PID 6064 manque dans Process Monitor.')

    parent_trace = json.loads(demarrage['details'])['Parent PID']
    if parent_trace != res['PPID']:
        raise ValueError('Le parent du processus diffère entre la trace et la RAM.')

    # Volatility donne la seconde ; Process Monitor conserve aussi les fractions de seconde.
    heure_trace = datetime.fromisoformat(demarrage['heure_windows_utc'])
    heure_ram = datetime.fromisoformat(res['CreateTime'])
    if heure_trace.replace(microsecond=0) != heure_ram:
        raise ValueError('L’heure de lancement diffère entre la trace et la RAM.')
