import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path


# Identifiants du noyau et du pilote reseau lus dans notre capture Windows.
symboles = []
for nom, identifiant in [
    ('ntkrnlmp.pdb', 'CA8E2F01B822EDE6357898BFBF8629971'),
    ('tcpip.pdb', 'E4E0EE7832FBC6E1BE2D05BD43FA6EC61'),
]:
    url = f'https://msdl.microsoft.com/download/symbols/{nom}/{identifiant}/{nom}'
    pdb = Path('/symboles') / nom
    dossier = Path('/symboles/windows') / nom
    dossier.mkdir(parents=True, exist_ok=True)
    sortie = dossier / f'{identifiant}.json'

    print(f'Telechargement des symboles Microsoft : {nom}...', flush=True)
    with urllib.request.urlopen(url, timeout=60) as reponse, pdb.open('wb') as fichier:
        total = int(reponse.headers.get('Content-Length', 0))
        recus = 0
        while bloc := reponse.read(1024 * 1024):
            fichier.write(bloc)
            recus += len(bloc)
            print(f'\r{recus / 1024**2:.1f} / {total / 1024**2:.1f} Mio', end='', flush=True)
    print('\nConversion pour Volatility...', flush=True)
    with (Path('/cache') / f'conversion-{nom}.log').open('w') as journal:
        subprocess.run(['python', '-m', 'volatility3.framework.symbols.windows.pdbconv',
                        '-f', str(pdb), '-p', nom, '-o', str(sortie)], check=True,
                       stdout=journal, stderr=subprocess.STDOUT)
    empreintes = {}
    for chemin in (pdb, sortie):
        with chemin.open('rb') as fichier:
            empreintes[chemin.name] = hashlib.file_digest(fichier, 'sha256').hexdigest()
    symboles.append({'url': url, 'identifiant_pdb': identifiant, 'sha256': empreintes})
Path('/resultats/symboles.json').write_text(json.dumps(symboles, indent=2) + '\n')
print('Symboles prets.', flush=True)
