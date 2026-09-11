"""Étape 3 : rapprocher les processus en RAM des fichiers retrouvés sur disque."""

from fichiers import lire_json, normaliser


def lire_resultats_memoire():
    return {
        'avant': lire_json('/ram/avant-pslist.json'),
        'apres': lire_json('/ram/apres-pslist.json'),
        'scan': lire_json('/ram/apres-psscan.json'),
        'commandes': lire_json('/ram/apres-cmdline.json'),
        'modules': lire_json('/ram/apres-dlllist.json'),
    }


def processus_du_programme(liste, nom):
    trouves = []
    for processus in liste:
        if processus['ImageFileName'] == nom:
            trouves.append(processus)
    return trouves


def correler_processus(fichiers, memoire):
    correlations = []
    for nom in ('Res.exe', 'Env.exe'):
        origine = fichiers[normaliser('C:/Lab/sample/virus/' + nom)]
        copie = fichiers[normaliser('C:/WindSyst/' + nom)]
        if origine['sha256'] != copie['sha256']:
            raise ValueError(f'Les deux copies de {nom} sur disque sont différentes.')

        avant = processus_du_programme(memoire['avant'], nom)
        apres = processus_du_programme(memoire['apres'], nom)
        scan = processus_du_programme(memoire['scan'], nom)

        # Un module peut apparaître plusieurs fois : conserver chaque chemin une seule fois.
        chemins_ram = []
        for module in memoire['modules']:
            if module['Name'] == nom:
                chemin = normaliser(module['Path'])
                if chemin not in chemins_ram:
                    chemins_ram.append(chemin)
        chemins_ram.sort()

        commandes_ram = []
        for commande in memoire['commandes']:
            if commande['Process'] == nom:
                commandes_ram.append(commande['Args'])

        chemins_retrouves = len(chemins_ram) > 0
        for chemin in chemins_ram:
            if chemin not in fichiers:
                chemins_retrouves = False

        correlations.append({
            'programme': nom,
            'processus_ram_apres': apres,
            'present_ram_avant': len(avant) > 0,
            'pids_psscan': [processus['PID'] for processus in scan],
            'commandes_ram': commandes_ram,
            'chemins_modules_ram_normalises': chemins_ram,
            'fichier_lancement': origine,
            'copie_installee': copie,
            'chemin_ram_retrouve_sur_disque': chemins_retrouves,
            'empreinte_executable_ram_calculee': False,
        })
    return correlations
