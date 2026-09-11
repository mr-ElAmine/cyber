from pathlib import Path
from urllib.request import urlretrieve

url = "https://software-download.microsoft.com/download/pr/19044.1288.211006-0501.21h2_release_svc_refresh_CLIENT_LTSC_EVAL_x64FRE_fr-fr.iso"
destination = Path(__file__).resolve().parent / "media" / "windows.iso"
destination.parent.mkdir(parents=True, exist_ok=True)

last_percent = -1


def show_progress(blocks, block_size, total_size):
    global last_percent
    if total_size <= 0:
        return
    percent = min(100, blocks * block_size * 100 // total_size)
    if percent != last_percent:
        print(f"\rTéléchargement : {percent} %", end="", flush=True)
        last_percent = percent


print("Téléchargement de Windows (environ 4,9 Go)...", flush=True)
urlretrieve(url, destination, reporthook=show_progress)
print(f"\nISO téléchargée : {destination}")
