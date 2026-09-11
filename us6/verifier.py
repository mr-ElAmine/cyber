import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from elftools.elf.elffile import ELFFile


captures = [
    ('avant', Path('/avant/windows-before-malware.elf'),
     '2663c98d783404068dbba24ee62f166a0f9417d2cf649a20b053ff5e16b5e9a1'),
    ('apres', Path('/storage/windows-after-malware.elf'),
     'f1c5d532807b5ffba91b8dbb2c4ed0cb1edcb5912ac1d4083da83fd3fc945cc9'),
]
resultats = []
for nom, chemin, attendu in captures:
    print(f'Verification de la capture {nom} : SHA-256...', flush=True)
    taille = chemin.stat().st_size
    with chemin.open('rb') as fichier:
        empreinte = hashlib.file_digest(fichier, 'sha256').hexdigest()
        assert empreinte == attendu, 'Empreinte differente du releve initial'
        fichier.seek(0)
        elf = ELFFile(fichier)
        assert elf.elfclass == 64 and elf.little_endian
        assert elf['e_type'] == 'ET_CORE' and elf['e_machine'] == 'EM_X86_64'
        segments = []
        for segment in elf.iter_segments():
            assert segment['p_offset'] + segment['p_filesz'] <= taille, 'Segment tronque'
            if segment['p_type'] == 'PT_LOAD':
                assert segment['p_filesz'] == segment['p_memsz'], 'Segment partiel'
                segments.append({'adresse_physique': segment['p_paddr'],
                                 'offset_fichier': segment['p_offset'],
                                 'octets': segment['p_filesz']})
    segments.sort(key=lambda s: s['adresse_physique'])
    for a, b in zip(segments, segments[1:]):
        assert a['adresse_physique'] + a['octets'] <= b['adresse_physique']
    total = sum(s['octets'] for s in segments)
    assert total >= 4 * 1024**3, 'Moins de 4 Gio de regions physiques'
    resultats.append({'capture': nom, 'fichier': chemin.name, 'octets': taille,
                      'sha256': empreinte, 'format': 'ELF64 little-endian x86-64 ET_CORE',
                      'segments': segments, 'octets_physiques': total,
                      'segments_declares_complets': True})
    print(f'{nom} : empreinte conforme, {len(segments)} segments complets.', flush=True)

Path('/resultats/integrite.json').write_text(json.dumps({
    'verification_utc': datetime.now(timezone.utc).isoformat(),
    'captures': resultats,
}, indent=2) + '\n')
