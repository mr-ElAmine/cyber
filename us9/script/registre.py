"""Lire une valeur ou une clé facultative, sans masquer les erreurs de lecture."""

from dissect.regf.exceptions import RegistryKeyNotFoundError, RegistryValueNotFoundError

GUID_PROPRIETES = '{83da6326-97a6-4088-9453-a1923f573b29}'


def ouvrir_cle(ruche, chemin):
    try:
        return ruche.open(chemin)
    except RegistryKeyNotFoundError:
        return None


def valeur(cle, nom, defaut=None):
    if cle is None:
        return defaut
    try:
        return cle.value(nom).value
    except RegistryValueNotFoundError:
        return defaut


def lire_propriete(ruche, appareil, numero):
    chemin = appareil + '\\Properties\\' + GUID_PROPRIETES + '\\' + numero
    cle = ouvrir_cle(ruche, chemin)
    return valeur(cle, '(Default)')
