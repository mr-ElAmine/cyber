"""Relier la clé au volume, à sa lettre et au registre utilisateur fourni."""

from registre import ouvrir_cle, valeur

CLE_MONTAGES = r'Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2'
CLE_PORTABLES = r'Microsoft\Windows Portable Devices\Devices'


def correspond_au_stockage(texte, appareil):
    # Comparer le modèle ET l’instance entière ; éviter un simple sous-texte du numéro.
    identifiant = appareil['cle_usbstor'].split('\\Enum\\')[1].replace('\\', '#')
    return (identifiant + '#').casefold() in texte.casefold()


def relier_volume(registres, appareil):
    montages = []
    for entree in registres['SYSTEM'].open('MountedDevices').values():
        try:
            texte = entree.value.decode('utf-16-le')
        except UnicodeDecodeError:
            continue
        if correspond_au_stockage(texte, appareil):
            montages.append({'nom': entree.name, 'donnee': texte})

    profils = []
    for montage in montages:
        if not montage['nom'].startswith('\\??\\Volume{'):
            continue
        volume = montage['nom'].removeprefix('\\??\\Volume')
        chemin = CLE_MONTAGES + '\\' + volume
        cle = ouvrir_cle(registres['NTUSER.DAT'], chemin)
        if cle is not None:
            profils.append({
                'registre': 'NTUSER.DAT', 'cle': chemin,
                'derniere_modification_utc': cle.timestamp.isoformat(),
                'sens': 'Trace de montage dans ce profil ; ne prouve pas une copie de fichiers.',
            })

    noms = []
    portables = ouvrir_cle(registres['SOFTWARE'], CLE_PORTABLES)
    if portables is not None:
        for cle in portables.subkeys():
            if correspond_au_stockage(cle.name, appareil):
                noms.append({'cle': CLE_PORTABLES + '\\' + cle.name,
                             'nom': valeur(cle, 'FriendlyName')})
    return {'montages': montages, 'noms_volume': noms, 'traces_profil': profils}
