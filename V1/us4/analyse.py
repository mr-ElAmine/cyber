import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from importlib.metadata import version
from pathlib import Path

from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.ntfs import NTFS
from dissect.regf import RegistryHive
from dissect.volume.disk import Disk
from procmon_parser import ProcmonLogsReader


def heure(filetime):
    # FILETIME Windows : intervalles de 100 ns depuis 1601, conversion en UTC.
    date = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=filetime // 10)
    return date.isoformat()


def windows(snapshot):
    partitions = Disk(snapshot.open()).partitions
    return NTFS(max(partitions, key=lambda p: p.size).open())


def etat(ntfs):
    hive = RegistryHive(ntfs.mft.get('Users/Analyste/NTUSER.DAT').open())
    valeurs = hive.open(r'Software\Microsoft\Windows\CurrentVersion\Run').values()
    fichiers = []
    try:
        dossier = ntfs.mft.get('WindSyst')
    except FileNotFoundError:
        return {'valeurs_run': {v.name: v.value for v in valeurs}, 'fichiers': []}
    for fichier in dossier.iterdir(dereference=True, ignore_dos=True):
        info = {'nom': fichier.filename, 'dossier': fichier.is_dir()}
        if fichier.is_file():
            info['octets'] = fichier.size()
            info['sha256'] = hashlib.file_digest(fichier.open(), 'sha256').hexdigest()
        if fichier.filename == 'log.txt':
            info['phrase_test_complete_presente'] = b'lab test 12345' in fichier.open().read().lower()
        fichiers.append(info)
    return {'valeurs_run': {v.name: v.value for v in valeurs}, 'fichiers': fichiers}


sortie = Path('/resultats')
disque = QCow2(Path('/storage/windows.qcow2'))
snapshots = {s.name: s for s in disque.snapshots}
avant = etat(windows(snapshots['windows-clean-us1']))


def analyser(snapshot, chemin_trace, prefixe, attendue=None):
    apres = windows(snapshots[snapshot])
    trace = apres.mft.get(chemin_trace)
    empreinte = hashlib.file_digest(trace.open(), 'sha256').hexdigest()
    if attendue is not None:
        assert empreinte == attendue
    lecteur = ProcmonLogsReader(trace.open())
    print(f'Lecture des {len(lecteur)} evenements du snapshot {snapshot}...')

    processus = {}
    identites = set()
    classes = Counter()
    operations = Counter()
    candidats = []
    premier = dernier = None
    for numero, evenement in enumerate(lecteur, 1):
        p = evenement.process
        identites.add((p.pid, p.start_time))
        processus[p.pid] = {'pid': p.pid, 'parent_pid': p.parent_pid, 'nom': p.process_name,
                            'image': p.image_path, 'commande': p.command_line,
                            'debut_filetime': p.start_time}
        operation = evenement.operation.name
        classes[evenement.event_class.name] += 1
        operations[(p.pid, operation)] += 1
        premier = evenement.date_filetime if premier is None else premier
        dernier = evenement.date_filetime
        chemin = evenement.path or ''
        if (operation in ('Process_Start', 'Process_Create', 'Process_Exit', 'RegSetValue')
                or p.process_name.lower() == 'env.exe'
                or 'windsyst' in chemin.lower() or evenement.event_class.name == 'Network'):
            # Ne pas exporter les variables d'environnement ni les piles completes.
            details = {k: v for k, v in evenement.details.items() if k != 'Environment'}
            candidats.append({'evenement': numero, 'heure_windows_utc': heure(dernier),
                              'filetime': dernier, 'pid': p.pid, 'processus': p.process_name,
                              'classe': evenement.event_class.name, 'operation': operation,
                              'chemin': chemin, 'resultat_ntstatus': f'0x{evenement.result:08x}',
                              'details': json.dumps(details, ensure_ascii=False, default=str)})
        if numero % 50000 == 0:
            print(f'{numero}/{len(lecteur)} evenements lus')

    assert numero == len(lecteur)
    assert len(identites) == len(processus), 'PID reutilise : attribution a revoir avec les heures de creation'
    racines = {pid for pid, p in processus.items() if p['nom'].lower() in ('res.exe', 'env.exe')}
    famille = set(racines)
    while True:
        enfants = {pid for pid, p in processus.items() if p['parent_pid'] in famille}
        if enfants <= famille:
            break
        famille |= enfants
    evenements = [e for e in candidats if e['pid'] in famille]
    with (sortie / f'{prefixe}evenements.csv').open('w', newline='') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(evenements[0]))
        writer.writeheader()
        writer.writerows(evenements)

    resume = {
        'analyse_utc': datetime.now(timezone.utc).isoformat(),
        'versions': {nom: version(nom) for nom in ('dissect.hypervisor', 'dissect.volume',
                                                 'dissect.ntfs', 'dissect.regf', 'procmon-parser')},
        'snapshot': snapshot, 'trace': 'C:\\' + chemin_trace.replace('/', '\\'),
        'trace_octets': trace.size(), 'trace_sha256': empreinte,
        'total_evenements': numero, 'classes': dict(classes),
        'premier_evenement_windows_utc': heure(premier), 'dernier_evenement_windows_utc': heure(dernier),
        'racines_pid': sorted(racines), 'processus': [processus[pid] for pid in sorted(famille)],
        'operations_par_processus': [{'pid': pid, 'operation': op, 'nombre': nombre}
                                    for (pid, op), nombre in sorted(operations.items()) if pid in famille],
        'evenements_selectionnes': len(evenements),
        'evenements_reseau_famille': sum(e['classe'] == 'Network' for e in evenements),
        'avant': avant, 'apres': etat(apres),
    }
    (sortie / f'{prefixe}resume.json').write_text(json.dumps(resume, indent=2, ensure_ascii=False) + '\n')
    print(f'Termine : {len(famille)} processus de la famille, {len(evenements)} evenements selectionnes.')


analyser('malware-first-run', 'Lab/trace.pml', '',
         '0853884c7af540bab2252ac4491070614d0851909804555252be073d24be5bae')
analyser('us4-controlled-run', 'Lab/us4.pml', 'second-',
         '512cb0d2e493fba7664c7334d4a3181870b51ff707a8c4b49df9d84ad06f1c12')

ntfs = windows(snapshots['us4-controlled-run'])
releves = []
for nom in ('essai.txt', 'reseau-avant.txt', 'reseau-apres.txt', 'hashes-avant.txt'):
    contenu = ntfs.mft.get('Lab/' + nom).open().read()
    (sortie / nom).write_bytes(contenu)
    releves.append({'fichier': nom, 'octets': len(contenu),
                    'sha256': hashlib.sha256(contenu).hexdigest()})
(sortie / 'releves.json').write_text(json.dumps(releves, indent=2) + '\n')
