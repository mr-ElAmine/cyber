"""Les fichiers et les identifiants du premier essai du laboratoire."""

from pathlib import Path

# Ces chemins sont ceux des conteneurs Docker.
RESULTATS = Path('/resultats')
DOSSIER_SYMBOLES = Path('/symboles')

CAPTURES = {
    'avant': {
        'chemin': Path('/avant/windows-before-malware.elf'),
        'sha256': '2663c98d783404068dbba24ee62f166a0f9417d2cf649a20b053ff5e16b5e9a1',
    },
    'apres': {
        'chemin': Path('/storage/windows-after-malware.elf'),
        'sha256': 'f1c5d532807b5ffba91b8dbb2c4ed0cb1edcb5912ac1d4083da83fd3fc945cc9',
    },
}

# PID de Res.exe relevé dans Process Monitor pendant le premier essai.
PID_RES = 6064

# Symboles correspondant au noyau Windows et à son pilote réseau.
SYMBOLES = {
    'ntkrnlmp.pdb': 'CA8E2F01B822EDE6357898BFBF8629971',
    'tcpip.pdb': 'E4E0EE7832FBC6E1BE2D05BD43FA6EC61',
}
SERVEUR_MICROSOFT = 'https://msdl.microsoft.com/download/symbols'
