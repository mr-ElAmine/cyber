"""Étape 5 : sélectionner les événements et relier les copies à Res.exe."""

from fichiers import normaliser


def remonter_parents(pid, processus):
    filiation = []
    deja_vus = set()
    while pid not in deja_vus:
        deja_vus.add(pid)
        if pid not in processus:
            raise ValueError(f'Le PID {pid} manque dans la trace des processus.')
        filiation.append({'pid': pid, 'nom': processus[pid]['nom']})
        if pid == 6064:
            return filiation
        pid = processus[pid]['parent_pid']
    raise ValueError('La chaîne des parents boucle sans rejoindre Res.exe, PID 6064.')


def reconstituer_scenario(evenements, trace, fichiers, persistance):
    processus = {}
    for entree in trace['processus']:
        processus[entree['pid']] = entree

    ecritures_registre = []
    for entree in persistance:
        ecritures_registre.append(entree['ecriture_procmon']['evenement'])

    chemins_copies = [normaliser('C:/WindSyst/Res.exe'), normaliser('C:/WindSyst/Env.exe')]
    chemin_journal = normaliser('C:/WindSyst/log.txt')
    selection = []
    copies = []
    ecritures_journal = 0

    for evenement in evenements:
        chemin = normaliser(evenement['chemin'])
        operation = evenement['operation']
        copie_executable = operation == 'WriteFile' and chemin in chemins_copies
        ecriture_journal = operation == 'WriteFile' and chemin == chemin_journal
        lancement = operation == 'Process_Start' and evenement['pid'] == '6064'
        ecriture_registre = evenement['evenement'] in ecritures_registre

        if not (copie_executable or ecriture_journal or lancement or ecriture_registre):
            continue
        if evenement['resultat_ntstatus'] != '0x00000000':
            raise ValueError(f"L’événement {evenement['evenement']} signale un échec.")
        selection.append(evenement)

        if ecriture_journal:
            ecritures_journal += 1
        if copie_executable:
            filiation = remonter_parents(int(evenement['pid']), processus)
            copies.append({
                'evenement': evenement['evenement'],
                'chemin': evenement['chemin'],
                'filiation': filiation,
            })

    scenario = {
        'copies': copies,
        'evenements_selectionnes': len(selection),
        'ecritures_journal': ecritures_journal,
        'journal_disque': fichiers[chemin_journal],
    }
    return selection, scenario
