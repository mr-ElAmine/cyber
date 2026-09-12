"""Retrouver le stockage USB et vérifier son lien avec le périphérique parent."""

from registre import lire_propriete, ouvrir_cle, valeur


def identifier_usb(systeme):
    numero = systeme.open('Select').value('Current').value
    controle = f'ControlSet{numero:03d}'
    chemin = controle + r'\Enum\USBSTOR'
    racine = ouvrir_cle(systeme, chemin)
    appareils = []
    if racine is None:
        return controle, appareils

    for modele in racine.subkeys():
        for instance in modele.subkeys():
            stockage = chemin + '\\' + modele.name + '\\' + instance.name
            parent_brut = lire_propriete(systeme, stockage, '000A')
            if not isinstance(parent_brut, bytes):
                raise ValueError('Le lien vers le périphérique parent est absent.')
            parent = parent_brut.decode('utf-16-le').rstrip('\0')
            chemin_usb = controle + '\\Enum\\' + parent
            usb = systeme.open(chemin_usb)

            # Le parent fournit le numéro sans le suffixe de disque « &0 ».
            serie = parent.split('\\')[-1]
            container = valeur(instance, 'ContainerID')
            lien_confirme = (
                parent.startswith('USB\\')
                and valeur(usb, 'Service') == 'USBSTOR'
                and instance.name == serie + '&0'
                and container is not None
                and container == valeur(usb, 'ContainerID')
                and bool(valeur(usb, 'Capabilities', 0) & 0x10)
            )
            if not lien_confirme:
                raise ValueError('Le numéro de série doit être vérifié manuellement.')

            appareils.append({
                'modele': valeur(instance, 'FriendlyName', modele.name),
                'numero_serie': serie,
                'instance_usbstor': instance.name,
                'identifiant_usb': parent.split('\\')[1],
                'container_id': container,
                'cle_usbstor': stockage,
                'cle_usb': chemin_usb,
                'parent_confirme': lien_confirme,
            })
    return controle, appareils
