import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


archive = Path('/samples/Waelmeg-056490ff.zip')
fichiers = [("Malware.zip", archive.read_bytes())]

# Lire les exécutables dans le ZIP, sans les extraire ni les exécuter.
with zipfile.ZipFile(archive) as contenu:
    for nom in contenu.namelist():
        if nom.lower().endswith('.exe'):
            fichiers.append((nom, contenu.read(nom)))

resultats = []
for nom, donnees in fichiers:
    resultats.append({
        'fichier': nom,
        'octets': len(donnees),
        'sha256': hashlib.sha256(donnees).hexdigest(),
        'sha1': hashlib.sha1(donnees).hexdigest(),
        'md5': hashlib.md5(donnees).hexdigest(),
    })

print(json.dumps({
    'date_utc': datetime.now(timezone.utc).isoformat(),
    'fichiers': resultats,
}, indent=2))
