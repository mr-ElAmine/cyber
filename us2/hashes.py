"""Calculer les empreintes du ZIP et des EXE qu'il contient."""

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


chemin_archive = Path('/samples/Waelmeg-056490ff.zip')


def calculer_empreintes(nom, contenu):
    # Chaque empreinte est calculée sur les octets du fichier, pas sur son nom.
    return {
        'fichier': nom,
        'octets': len(contenu),
        'sha256': hashlib.sha256(contenu).hexdigest(),
        'sha1': hashlib.sha1(contenu).hexdigest(),
        'md5': hashlib.md5(contenu).hexdigest(),
    }


# Identifier d'abord l'archive entière.
resultats = [calculer_empreintes('Malware.zip', chemin_archive.read_bytes())]

# Lire ensuite chaque EXE dans le ZIP. Ses octets restent en mémoire :
# aucun exécutable n'est extrait sur le disque ou lancé.
with zipfile.ZipFile(chemin_archive) as archive:
    for nom in archive.namelist():
        if nom.lower().endswith('.exe'):
            resultats.append(calculer_empreintes(nom, archive.read(nom)))

# hash.sh enregistre ce JSON dans hashes.json, puis affiche le fichier.
print(json.dumps({
    'date_utc': datetime.now(timezone.utc).isoformat(),
    'fichiers': resultats,
}, indent=2))
