"""Les chemins Docker et les références du premier essai."""

from pathlib import Path

DISQUE_SOURCE = Path('/storage/windows.qcow2')
IMAGE_RAW = Path('/images/windows-first-run.raw')
RESULTATS = Path('/resultats')
SNAPSHOT = 'malware-first-run'

TAILLE_DISQUE = 64 * 1024**3  # 64 Gio.
TAILLE_BLOC = 16 * 1024**2    # Comparaison par blocs de 16 Mio.

# Empreintes calculées en US2 pour reconnaître les deux exécutables.
EMPREINTES_US2 = {
    'Res.exe': '49f091ade48890bfa22d2b455494be95e52392c478b67e10626222b6aee37e1e',
    'Env.exe': 'e09ec2098363a129de143fdaf73ad6e2e61266fba3f638a25214af3a8bc8f2f2',
}
