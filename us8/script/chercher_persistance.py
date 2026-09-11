"""Étape 4 : relier les valeurs Run du registre aux écritures de Process Monitor."""

import json

from fichiers import normaliser


def trouver_ecriture(nom, evenements):
    cle = normaliser('HKCU/Software/Microsoft/Windows/CurrentVersion/Run/' + nom)
    ecritures = []
    for evenement in evenements:
        if evenement['operation'] == 'RegSetValue' and normaliser(evenement['chemin']) == cle:
            ecritures.append(evenement)

    if len(ecritures) != 1:
        raise ValueError(f'Une seule écriture de Run/{nom} est attendue dans la trace.')
    ecriture = ecritures[0]
    if ecriture['resultat_ntstatus'] != '0x00000000':
        raise ValueError(f'L’écriture de Run/{nom} n’a pas réussi.')
    return ecriture


def chercher_persistance(avant, apres, fichiers, evenements):
    persistance = []
    for nom, valeur in apres['valeurs'].items():
        cible = fichiers[normaliser(valeur['donnee'])]
        ecriture = trouver_ecriture(nom, evenements)
        cible_trace = json.loads(ecriture['details'])['Data']
        if normaliser(cible_trace) != normaliser(valeur['donnee']):
            raise ValueError(f'Run/{nom} désigne des fichiers différents dans la trace et le registre.')

        persistance.append({
            'nom': nom,
            'donnee': valeur['donnee'],
            'type': valeur['type'],
            'absente_etat_propre': nom not in avant['valeurs'],
            'fichier_cible': cible,
            'ecriture_procmon': ecriture,
            'relancement_automatique_teste': False,
        })
    return persistance
