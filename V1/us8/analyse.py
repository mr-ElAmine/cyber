import csv
import hashlib
import json
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path, PureWindowsPath

from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.ntfs import NTFS
from dissect.regf import RegistryHive
from dissect.volume.disk import Disk


def lire(chemin):
    return json.loads(Path(chemin).read_text())


def sauver(nom, valeur):
    Path('/resultats', nom).write_text(json.dumps(valeur, indent=2, ensure_ascii=False) + '\n')


def normaliser(chemin):
    return str(PureWindowsPath(chemin.strip('"'))).casefold()


def volume_windows(flux):
    return NTFS(max(Disk(flux).partitions, key=lambda p: p.size).open())


def lire_run(ntfs):
    entree = ntfs.mft.get('Users/Analyste/NTUSER.DAT')
    sha256 = hashlib.file_digest(entree.open(), 'sha256').hexdigest()
    ruche = RegistryHive(entree.open())
    cle = ruche.open(r'Software\Microsoft\Windows\CurrentVersion\Run')
    return {'ruche_sha256': sha256, 'sequence1': ruche.header.Sequence1,
            'sequence2': ruche.header.Sequence2, 'en_transaction': ruche.in_transaction,
            'cle_modifiee_windows_utc': cle.timestamp.isoformat(),
            'valeurs': {v.name: {'type': int(v.type), 'donnee': v.value} for v in cle.values()}}


debut = datetime.now(timezone.utc).isoformat()
image = Path('/images/windows-first-run.raw')
attendu = lire('/disque/integrite.json')['sha256_image_raw']
print('Controle SHA-256 de l image disque complete (64 Gio)...', flush=True)
empreinte = hashlib.sha256()
lus = 0
with image.open('rb') as flux:
    while bloc := flux.read(16 * 1024**2):
        empreinte.update(bloc)
        lus += len(bloc)
        if lus % (8 * 1024**3) == 0:
            print(f'{lus // 1024**3} / 64 Gio controles', flush=True)
assert lus == 64 * 1024**3 and empreinte.hexdigest() == attendu

print('Lecture des fichiers et du registre sur la copie RAW...', flush=True)
ntfs = volume_windows(image.open('rb'))
fichiers = {}
for reference in lire('/disque/analyse.json')['fichiers']:
    chemin = PureWindowsPath(reference['chemin'])
    if chemin.name.lower() not in ('res.exe', 'env.exe', 'log.txt', 'ntuser.dat', 'trace.pml'):
        continue
    entree = ntfs.mft.get('/'.join(chemin.parts[1:]))
    sha256 = hashlib.file_digest(entree.open(), 'sha256').hexdigest()
    assert sha256 == reference['sha256'] and entree.size() == reference['octets']
    fichiers[normaliser(str(chemin))] = {
        'chemin': str(chemin), 'octets': entree.size(), 'sha256': sha256}

qcow = QCow2(Path('/source/windows.qcow2'))
propre = next(s for s in qcow.snapshots if s.name == 'windows-clean-us1')
avant = lire_run(volume_windows(propre.open()))
apres = lire_run(ntfs)
assert not avant['en_transaction'] and not apres['en_transaction']

print('Croisement avec les resultats memoire et la trace du premier essai...', flush=True)
ram_avant = lire('/ram/avant-pslist.json')
ram_apres = lire('/ram/apres-pslist.json')
ram_scan = lire('/ram/apres-psscan.json')
commandes = lire('/ram/apres-cmdline.json')
modules = lire('/ram/apres-dlllist.json')
trace = lire('/dynamique/resume.json')
assert trace['snapshot'] == 'malware-first-run'
assert trace['trace_sha256'] == fichiers[normaliser('C:/Lab/trace.pml')]['sha256']
with Path('/dynamique/evenements.csv').open() as flux:
    evenements = list(csv.DictReader(flux))
processus_trace = {p['pid']: p for p in trace['processus']}

correlations = []
for nom in ('Res.exe', 'Env.exe'):
    processus = [p for p in ram_apres if p['ImageFileName'] == nom]
    origine = fichiers[normaliser('C:/Lab/sample/virus/' + nom)]
    copie = fichiers[normaliser('C:/WindSyst/' + nom)]
    assert origine['sha256'] == copie['sha256']
    chemins_ram = sorted({normaliser(m['Path']) for m in modules if m['Name'] == nom})
    commandes_ram = [c['Args'] for c in commandes if c['Process'] == nom]
    correlations.append({
        'programme': nom, 'processus_ram_apres': processus,
        'present_ram_avant': any(p['ImageFileName'] == nom for p in ram_avant),
        'pids_psscan': [p['PID'] for p in ram_scan if p['ImageFileName'] == nom],
        'commandes_ram': commandes_ram, 'chemins_modules_ram_normalises': chemins_ram,
        'fichier_lancement': origine, 'copie_installee': copie,
        'chemin_ram_retrouve_sur_disque': bool(chemins_ram) and all(c in fichiers for c in chemins_ram),
        'empreinte_executable_ram_calculee': False,
    })

res = correlations[0]
assert len(res['processus_ram_apres']) == 1
processus_res = res['processus_ram_apres'][0]
assert processus_res['PID'] == 6064 and processus_res['ExitTime'] is None
assert res['chemin_ram_retrouve_sur_disque']
assert all(normaliser(c) == normaliser(res['fichier_lancement']['chemin']) for c in res['commandes_ram'])
demarrage = next(e for e in evenements if e['operation'] == 'Process_Start' and e['pid'] == '6064')
assert json.loads(demarrage['details'])['Parent PID'] == processus_res['PPID']
assert datetime.fromisoformat(demarrage['heure_windows_utc']).replace(microsecond=0) == datetime.fromisoformat(processus_res['CreateTime'])

persistance = []
for nom, valeur in apres['valeurs'].items():
    cible = fichiers[normaliser(valeur['donnee'])]
    ecritures = [e for e in evenements if e['operation'] == 'RegSetValue'
                and normaliser(e['chemin']) == normaliser('HKCU/Software/Microsoft/Windows/CurrentVersion/Run/' + nom)]
    assert len(ecritures) == 1 and ecritures[0]['resultat_ntstatus'] == '0x00000000'
    assert normaliser(json.loads(ecritures[0]['details'])['Data']) == normaliser(valeur['donnee'])
    persistance.append({'nom': nom, 'donnee': valeur['donnee'], 'type': valeur['type'],
                        'absente_etat_propre': nom not in avant['valeurs'],
                        'fichier_cible': cible, 'ecriture_procmon': ecritures[0],
                        'relancement_automatique_teste': False})

selection = []
copies = []
for e in evenements:
    chemin = normaliser(e['chemin'])
    copie_exe = e['operation'] == 'WriteFile' and chemin in {
        normaliser('C:/WindSyst/Res.exe'), normaliser('C:/WindSyst/Env.exe')}
    journal = e['operation'] == 'WriteFile' and chemin == normaliser('C:/WindSyst/log.txt')
    lancement = e['operation'] == 'Process_Start' and e['pid'] == '6064'
    registre = any(e['evenement'] == p['ecriture_procmon']['evenement'] for p in persistance)
    if not (copie_exe or journal or lancement or registre):
        continue
    assert e['resultat_ntstatus'] == '0x00000000'
    selection.append(e)
    if copie_exe:
        chaine = []
        pid = int(e['pid'])
        while pid not in chaine:
            chaine.append(pid)
            if pid == 6064:
                break
            pid = processus_trace[pid]['parent_pid']
        assert chaine[-1] == 6064
        copies.append({'evenement': e['evenement'], 'chemin': e['chemin'],
                       'filiation': [{'pid': p, 'nom': processus_trace[p]['nom']} for p in chaine]})

with Path('/resultats/evenements.csv').open('w', newline='') as flux:
    writer = csv.DictWriter(flux, fieldnames=list(selection[0]))
    writer.writeheader()
    writer.writerows(selection)
sauver('correlations.json', correlations)
sauver('persistance.json', {'cle': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run',
                          'snapshot_propre': propre.name, 'avant': avant, 'apres': apres,
                          'entrees': persistance})
sauver('scenario.json', {'copies': copies, 'evenements_selectionnes': len(selection),
                       'ecritures_journal': sum(e['operation'] == 'WriteFile' and
                           normaliser(e['chemin']) == normaliser('C:/WindSyst/log.txt') for e in selection),
                       'journal_disque': fichiers[normaliser('C:/WindSyst/log.txt')]})

entrees = {}
for chemin in ['/ram/avant-pslist.json', '/ram/apres-pslist.json', '/ram/apres-psscan.json',
               '/ram/apres-cmdline.json', '/ram/apres-dlllist.json', '/ram/integrite.json',
               '/ram/apres-info.json', '/ram/acquisition.json', '/disque/analyse.json',
               '/disque/integrite.json', '/dynamique/resume.json', '/dynamique/evenements.csv']:
    with Path(chemin).open('rb') as flux:
        entrees[chemin] = hashlib.file_digest(flux, 'sha256').hexdigest()
sauver('provenance.json', {'debut_utc': debut, 'fin_utc': datetime.now(timezone.utc).isoformat(),
                         'image_raw_sha256_recalcule': empreinte.hexdigest(),
                         'image_raw_octets': lus, 'fichiers_disque_relus': list(fichiers.values()),
                         'sha256_resultats_utilises': entrees,
                         'memoire': 'Resultats Volatility reutilises de l US6 ; aucune nouvelle extraction RAM.',
                         'versions': {p: version(p) for p in ['dissect.hypervisor', 'dissect.volume',
                                                           'dissect.ntfs', 'dissect.regf']}})
print('Termine : correlations RAM/disque, registre avant/apres et scenario dans resultats.', flush=True)
