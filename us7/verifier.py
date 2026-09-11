import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from dissect.hypervisor.disk.qcow2 import QCow2


debut = datetime.now(timezone.utc).isoformat()
disque = QCow2(Path('/storage/windows.qcow2'))
snapshot = next(s for s in disque.snapshots if s.name == 'malware-first-run')
source = snapshot.open()
image = Path('/images/windows-first-run.raw')
taille = source.size
assert image.stat().st_size == taille == 64 * 1024**3
empreinte_source = hashlib.sha256()
empreinte_image = hashlib.sha256()
lus = 0
with image.open('rb') as copie:
    while lus < taille:
        bloc_source = source.read(16 * 1024**2)
        bloc_image = copie.read(len(bloc_source))
        assert bloc_source, 'Fin de source prematuree'
        assert bloc_source == bloc_image, f'Difference a partir de l octet {lus}'
        empreinte_source.update(bloc_source)
        empreinte_image.update(bloc_image)
        lus += len(bloc_source)
        if lus % (1024**3) == 0:
            print(f'Comparaison : {lus / 1024**3:.0f} / {taille / 1024**3:.0f} Gio', flush=True)
    assert copie.read(1) == b''

resultat = {
    'debut_verification_utc': debut,
    'fin_verification_utc': datetime.now(timezone.utc).isoformat(),
    'source': 'cyber-windows_windows-disk:/windows.qcow2',
    'snapshot': snapshot.name, 'snapshot_id': snapshot.id,
    'image': image.name, 'octets_compares': lus,
    'sha256_source_logique': empreinte_source.hexdigest(),
    'sha256_image_raw': empreinte_image.hexdigest(),
    'identique_octet_par_octet': True,
    'methode': 'Lecture du snapshot avec Dissect et de la copie RAW, comparaison integrale par blocs de 16 Mio.',
}
Path('/resultats/integrite.json').write_text(json.dumps(resultat, indent=2) + '\n')
Path('/resultats/SHA256SUMS').write_text(f'{empreinte_image.hexdigest()}  {image.name}\n')
print('Copie conforme sur les 64 Gio. SHA-256 :', empreinte_image.hexdigest(), flush=True)
