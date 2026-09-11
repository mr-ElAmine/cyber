import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pefile


sortie = Path('/resultats')
resultats = []
# Selection volontaire : ne pas publier les identifiants SMTP du binaire.
indices = re.compile(
    r'WindSyst|CurrentVersion\\Run|^smtp\.|^mkdir |^XCOPY |'
    r'^SMTP Example$|^AUTH |^EHLO |^HELO |^MAIL FROM|^RCPT TO|'
    r'^DATA$|^QUIT$|^STARTTLS$|^Subject:|^Res$|^Env$', re.IGNORECASE
)

with zipfile.ZipFile('/samples/Waelmeg-056490ff.zip') as archive:
    for chemin in ('VIRUS/Res.exe', 'VIRUS/Env.exe'):
        donnees = archive.read(chemin)
        nom = Path(chemin).name
        pe = pefile.PE(data=donnees)
        base = pe.OPTIONAL_HEADER.ImageBase
        imports = []
        for dll in pe.DIRECTORY_ENTRY_IMPORT:
            imports.append({
                'dll': dll.dll.decode(),
                'fonctions': [{
                    'nom': entree.name.decode() if entree.name else f'ordinal:{entree.ordinal}',
                    'iat_va': hex(entree.address),
                } for entree in dll.imports],
            })

        chaines = []
        for motif, encodage in ((rb'[\x20-\x7e]{3,}', 'ascii'),
                                (rb'(?:[\x20-\x7e]\x00){3,}', 'utf-16le')):
            for chaine in re.finditer(motif, donnees):
                valeur = chaine.group().decode(encodage)
                if indices.search(valeur):
                    valeur = re.sub(r'[\w.+-]+@[\w.-]+', '[ADRESSE MASQUEE]', valeur)
                    chaines.append({'offset': hex(chaine.start()),
                                    'va': hex(base + pe.get_rva_from_offset(chaine.start())),
                                    'encodage': encodage, 'texte': valeur})

        resultats.append({
            'fichier': nom, 'octets': len(donnees),
            'sha256': hashlib.sha256(donnees).hexdigest(),
            'machine': hex(pe.FILE_HEADER.Machine),
            'format': 'PE32' if pe.OPTIONAL_HEADER.Magic == 0x10b else 'PE32+',
            'base_image': hex(base),
            'point_entree_va': hex(base + pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            'horodatage_entete_utc_non_fiable': datetime.fromtimestamp(
                pe.FILE_HEADER.TimeDateStamp, timezone.utc).isoformat(),
            'taille_table_certificats': pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size,
            'debut_overlay': pe.get_overlay_data_start_offset(),
            'sections': [{
                'nom': section.Name.rstrip(b'\x00').decode(),
                'va': hex(base + section.VirtualAddress),
                'taille_virtuelle': section.Misc_VirtualSize,
                'taille_fichier': section.SizeOfRawData,
                'entropie': round(section.get_entropy(), 3),
                'permissions': ''.join(lettre for bit, lettre in
                    ((0x40000000, 'R'), (0x80000000, 'W'), (0x20000000, 'X'))
                    if section.Characteristics & bit),
            } for section in pe.sections],
            'imports': imports, 'chaines_selectionnees': chaines,
        })

        # Copie ephemere sur tmpfs noexec pour le desassembleur, jamais sur le Mac.
        copie = Path('/tmp') / nom
        copie.write_bytes(donnees)
        with (sortie / f'{nom}.asm.txt').open('w') as fichier:
            subprocess.run(['i686-w64-mingw32-objdump', '-d', '-Mintel', str(copie)],
                           stdout=fichier, check=True)
        copie.unlink()
        print(f'{nom} : structure PE, imports, chaines selectionnees et desassemblage enregistres.')

(sortie / 'analyse.json').write_text(json.dumps({
    'date_utc': datetime.now(timezone.utc).isoformat(),
    'pefile_version': pefile.__version__,
    'objdump_version': subprocess.check_output(
        ['i686-w64-mingw32-objdump', '--version'], text=True).splitlines()[0],
    'fichiers': resultats,
}, indent=2, ensure_ascii=False) + '\n')
