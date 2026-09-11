from pathlib import Path
from urllib.request import urlretrieve

# L'ISO est enregistrée à côté du script, dans le dossier media.
url = "https://software-download.microsoft.com/download/pr/19044.1288.211006-0501.21h2_release_svc_refresh_CLIENT_LTSC_EVAL_x64FRE_fr-fr.iso"
destination = Path(__file__).resolve().parent / "media" / "windows.iso"
destination.parent.mkdir(parents=True, exist_ok=True)

dernier_pourcentage = -1


def afficher_progression(blocs, taille_bloc, taille_totale):
    # urlretrieve appelle cette fonction après chaque bloc reçu.
    global dernier_pourcentage
    if taille_totale <= 0:
        return
    pourcentage = min(100, blocs * taille_bloc * 100 // taille_totale)
    # Réafficher la même ligne seulement quand le pourcentage change.
    if pourcentage != dernier_pourcentage:
        print(f"\rTéléchargement : {pourcentage} %", end="", flush=True)
        dernier_pourcentage = pourcentage


print("Téléchargement de Windows (environ 4,9 Go)...", flush=True)
urlretrieve(url, destination, reporthook=afficher_progression)
print(f"\nISO téléchargée : {destination}")
