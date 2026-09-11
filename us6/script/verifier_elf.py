"""Lire les régions mémoire déclarées dans une capture ELF et vérifier leurs limites."""

from elftools.elf.elffile import ELFFile


def lire_regions(chemin):
    taille_capture = chemin.stat().st_size
    regions = []

    with chemin.open('rb') as fichier:
        elf = ELFFile(fichier)
        if elf.elfclass != 64 or not elf.little_endian:
            raise ValueError('La capture doit être au format ELF 64 bits little-endian.')
        if elf['e_type'] != 'ET_CORE' or elf['e_machine'] != 'EM_X86_64':
            raise ValueError('La capture doit décrire la mémoire d’un système x86-64.')

        for segment in elf.iter_segments():
            debut_fichier = segment['p_offset']
            taille_region = segment['p_filesz']
            if debut_fichier + taille_region > taille_capture:
                raise ValueError('Un segment dépasse la fin du fichier : capture tronquée.')

            # PT_LOAD désigne une région mémoire exportée par QEMU.
            if segment['p_type'] != 'PT_LOAD':
                continue
            if taille_region != segment['p_memsz']:
                raise ValueError('Une région mémoire est partiellement absente du fichier.')

            regions.append({
                'adresse_physique': segment['p_paddr'],
                'offset_fichier': debut_fichier,
                'octets': taille_region,
            })

    regions.sort(key=lambda region: region['adresse_physique'])
    for position in range(1, len(regions)):
        precedente = regions[position - 1]
        suivante = regions[position]
        fin_precedente = precedente['adresse_physique'] + precedente['octets']
        if fin_precedente > suivante['adresse_physique']:
            raise ValueError('Deux régions mémoire se chevauchent.')

    total = sum(region['octets'] for region in regions)
    if total < 4 * 1024**3:
        raise ValueError('La capture contient moins de 4 Gio de régions physiques.')

    return regions
