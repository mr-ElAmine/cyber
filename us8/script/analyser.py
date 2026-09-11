"""Le déroulement de l’US8 : disque, registre, RAM, persistance et scénario."""

import csv
from datetime import datetime, timezone
from pathlib import Path

from chercher_persistance import chercher_persistance
from correler_processus import correler_processus, lire_resultats_memoire
from enregistrer_preuves import enregistrer_evenements, enregistrer_provenance
from fichiers import enregistrer_json, lire_json, normaliser
from lire_disque import ouvrir_windows, relever_fichiers
from lire_registre import CLE_RUN, SNAPSHOT_PROPRE, lire_etat_propre, lire_run
from reconstituer_scenario import reconstituer_scenario
from verifier_image import verifier_image
from verifier_lancement import verifier_lancement


def main():
    debut = datetime.now(timezone.utc).isoformat()
    image = Path('/images/windows-first-run.raw')

    # 1. Retrouver exactement l’image validée en US7.
    controle_image = verifier_image(image)

    # 2. Relire les fichiers et le registre, avant et après l’essai.
    print('Lecture des fichiers et du registre…')
    with image.open('rb') as contenu:
        ntfs = ouvrir_windows(contenu)
        fichiers = relever_fichiers(ntfs)
        registre_avant = lire_etat_propre()
        registre_apres = lire_run(ntfs)

    # 3. Vérifier la trace du premier essai, puis la croiser avec la RAM.
    trace = lire_json('/dynamique/resume.json')
    if trace['snapshot'] != 'malware-first-run':
        raise ValueError('La trace doit provenir du premier essai.')
    fichier_trace = fichiers[normaliser('C:/Lab/trace.pml')]
    if trace['trace_sha256'] != fichier_trace['sha256']:
        raise ValueError('La trace du disque diffère du relevé Process Monitor.')
    with Path('/dynamique/evenements.csv').open() as contenu:
        evenements = list(csv.DictReader(contenu))

    print('Comparaison des processus et du lancement de Res.exe…')
    memoire = lire_resultats_memoire()
    correlations = correler_processus(fichiers, memoire)
    verifier_lancement(correlations[0], evenements)  # Res.exe est le premier programme comparé.

    # 4. Retrouver les écritures qui expliquent les valeurs Run du registre.
    persistance = chercher_persistance(registre_avant, registre_apres, fichiers, evenements)

    # 5. Relier lancement, copies, registre et écritures du journal.
    selection, scenario = reconstituer_scenario(evenements, trace, fichiers, persistance)

    enregistrer_json('correlations.json', correlations)
    enregistrer_json('persistance.json', {
        'cle': CLE_RUN,
        'snapshot_propre': SNAPSHOT_PROPRE,
        'avant': registre_avant,
        'apres': registre_apres,
        'entrees': persistance,
    })
    enregistrer_json('scenario.json', scenario)
    enregistrer_evenements(selection)
    enregistrer_provenance(debut, controle_image, fichiers)
    print('Comparaison terminée. Les résultats sont dans resultats/.')


if __name__ == '__main__':
    main()
