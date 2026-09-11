"""Lire les deux exécutables et produire des traces textuelles pour l'US3."""

import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pefile

ARCHIVE = Path('/samples/Waelmeg-056490ff.zip')
RESULTATS = Path('/resultats')
EXECUTABLES = ('VIRUS/Res.exe', 'VIRUS/Env.exe')

# On retient les indices utiles au rendu. Un export de toutes les chaînes
# publierait aussi les identifiants SMTP présents dans les fichiers.
INDICES = re.compile(
    r'WindSyst|CurrentVersion\\Run|^smtp\.|^mkdir |^XCOPY |'
    r'^SMTP Example$|^AUTH |^EHLO |^HELO |^MAIL FROM|^RCPT TO|'
    r'^DATA$|^QUIT$|^STARTTLS$|^Subject:|^Res$|^Env$', re.IGNORECASE
)


def lire_imports(pe):
    # Fonctions et données demandées aux DLL, avec leurs adresses dans la table des imports.
    imports = []
    for dll in pe.DIRECTORY_ENTRY_IMPORT:
        fonctions = []
        for entree in dll.imports:
            nom = entree.name.decode() if entree.name else f'ordinal:{entree.ordinal}'
            fonctions.append({'nom': nom, 'iat_va': hex(entree.address)})
        imports.append({'dll': dll.dll.decode(), 'fonctions': fonctions})
    return imports


def lire_sections(pe):
    # Chaque section a des droits : R = lecture, W = écriture, X = exécution.
    sections = []
    for section in pe.sections:
        permissions = ''
        for bit, lettre in ((0x40000000, 'R'), (0x80000000, 'W'), (0x20000000, 'X')):
            if section.Characteristics & bit:
                permissions += lettre
        sections.append({
            'nom': section.Name.rstrip(b'\x00').decode(),
            'va': hex(pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress),
            'taille_virtuelle': section.Misc_VirtualSize,
            'taille_fichier': section.SizeOfRawData,
            'entropie': round(section.get_entropy(), 3),
            'permissions': permissions,
        })
    return sections


def relever_chaines(pe, donnees):
    chaines = []
    # Les chaînes Windows peuvent être en ASCII ou en UTF-16 little-endian.
    for motif, encodage in ((rb'[\x20-\x7e]{3,}', 'ascii'),
                            (rb'(?:[\x20-\x7e]\x00){3,}', 'utf-16le')):
        for correspondance in re.finditer(motif, donnees):
            texte = correspondance.group().decode(encodage)
            if not INDICES.search(texte):
                continue
            texte = re.sub(r'[\w.+-]+@[\w.-]+', '[ADRESSE MASQUEE]', texte)
            offset = correspondance.start()
            adresse = pe.OPTIONAL_HEADER.ImageBase + pe.get_rva_from_offset(offset)
            chaines.append({
                'offset': hex(offset), 'va': hex(adresse),
                'encodage': encodage, 'texte': texte,
            })
    return chaines


def desassembler(nom, donnees):
    # objdump lit un fichier. Cette copie ne vit que dans le /tmp du conteneur,
    # monté en mémoire avec noexec dans compose.yaml.
    copie = Path('/tmp') / nom
    copie.write_bytes(donnees)
    try:
        with (RESULTATS / f'{nom}.asm.txt').open('w') as sortie:
            subprocess.run(
                ['i686-w64-mingw32-objdump', '-d', '-Mintel', str(copie)],
                stdout=sortie, check=True,
            )
    finally:
        copie.unlink()


def main():
    fichiers = []
    with zipfile.ZipFile(ARCHIVE) as archive:
        for chemin in EXECUTABLES:
            nom = Path(chemin).name
            donnees = archive.read(chemin)
            print(f'{nom} : lecture des sections, des imports et des chaînes…')
            pe = pefile.PE(data=donnees)
            base = pe.OPTIONAL_HEADER.ImageBase
            fichiers.append({
                'fichier': nom,
                'octets': len(donnees),
                'sha256': hashlib.sha256(donnees).hexdigest(),
                'machine': hex(pe.FILE_HEADER.Machine),
                'format': 'PE32' if pe.OPTIONAL_HEADER.Magic == 0x10b else 'PE32+',
                'base_image': hex(base),
                'point_entree_va': hex(base + pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                # Ce champ est fourni par le binaire et peut avoir été falsifié.
                'horodatage_entete_utc_non_fiable': datetime.fromtimestamp(
                    pe.FILE_HEADER.TimeDateStamp, timezone.utc).isoformat(),
                'taille_table_certificats': pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size,
                'debut_overlay': pe.get_overlay_data_start_offset(),
                'sections': lire_sections(pe),
                'imports': lire_imports(pe),
                'chaines_selectionnees': relever_chaines(pe, donnees),
            })
            pe.close()
            print(f'{nom} : désassemblage des instructions…')
            desassembler(nom, donnees)

    rapport = {
        'date_utc': datetime.now(timezone.utc).isoformat(),
        'pefile_version': pefile.__version__,
        'objdump_version': subprocess.check_output(
            ['i686-w64-mingw32-objdump', '--version'], text=True).splitlines()[0],
        'fichiers': fichiers,
    }
    (RESULTATS / 'analyse.json').write_text(
        json.dumps(rapport, indent=2, ensure_ascii=False) + '\n')
    print('Terminé. Le JSON décrit les fichiers ; les .asm.txt permettent de suivre les appels.')


if __name__ == '__main__':
    main()
