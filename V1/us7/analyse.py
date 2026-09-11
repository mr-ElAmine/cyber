import csv
import hashlib
import json
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from dissect.ntfs import NTFS
from dissect.volume.disk import Disk


sortie = Path('/resultats')
image = Path('/images/windows-first-run.raw').open('rb')
disque = Disk(image)
partitions = [{'numero': p.number, 'offset_octets': p.offset, 'octets': p.size,
               'type': str(p.type), 'nom': p.name} for p in disque.partitions]
(sortie / 'partitions.json').write_text(json.dumps(partitions, indent=2) + '\n')
partition = max(disque.partitions, key=lambda p: p.size)
ntfs = NTFS(partition.open())

connus = {
    'Res.exe': '49f091ade48890bfa22d2b455494be95e52392c478b67e10626222b6aee37e1e',
    'Env.exe': 'e09ec2098363a129de143fdaf73ad6e2e61266fba3f638a25214af3a8bc8f2f2',
}
fichiers = []


def relever(chemin, role):
    entree = ntfs.mft.get(chemin)
    with entree.open() as contenu:
        sha256 = hashlib.file_digest(contenu, 'sha256').hexdigest()
    attendu = connus.get(entree.filename)
    fichiers.append({'chemin': 'C:\\' + chemin.replace('/', '\\'),
                     'octets': entree.size(), 'sha256': sha256, 'role': role,
                     'echantillon_us2_identique': sha256 == attendu if attendu else None})


def parcourir(chemin):
    for entree in ntfs.mft.get(chemin).iterdir(dereference=True, ignore_dos=True):
        enfant = chemin + '/' + entree.filename
        if entree.is_dir():
            parcourir(enfant)
        elif entree.is_file():
            role = 'fichier a examiner'
            if entree.filename in connus:
                role = 'executable suspect'
            elif entree.filename == 'log.txt':
                role = 'journal associe au malware'
            elif entree.filename.lower().endswith('.dll'):
                role = 'bibliotheque accompagnant les executables'
            relever(enfant, role)


for dossier in ('Lab/sample/virus', 'WindSyst'):
    print(f'Inventaire de C:\\{dossier}...', flush=True)
    parcourir(dossier)
relever('Lab/trace.pml', 'trace Process Monitor du laboratoire')
relever('Users/Analyste/NTUSER.DAT', 'ruche utilisateur a examiner pour la persistance')
fichiers.sort(key=lambda f: f['chemin'].lower())
with (sortie / 'fichiers.csv').open('w', newline='') as fichier:
    writer = csv.DictWriter(fichier, fieldnames=list(fichiers[0]))
    writer.writeheader()
    writer.writerows(fichiers)
(sortie / 'analyse.json').write_text(json.dumps({
    'analyse_utc': datetime.now(timezone.utc).isoformat(),
    'image': 'windows-first-run.raw', 'partition_windows': partition.number,
    'versions': {nom: version(nom) for nom in ('dissect.hypervisor', 'dissect.volume', 'dissect.ntfs')},
    'fichiers': fichiers,
}, indent=2, ensure_ascii=False) + '\n')
print(f'Analyse terminee : {len(fichiers)} fichiers identifies, sans extraction des executables.', flush=True)
