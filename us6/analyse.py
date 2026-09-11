import json
import subprocess
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


subprocess.run(['python', '/travail/verifier.py'], check=True)
sortie = Path('/resultats')
commandes = []
for nom, fichier, plugins in [
    ('avant', '/avant/windows-before-malware.elf', ['info', 'pslist', 'netscan']),
    ('apres', '/storage/windows-after-malware.elf',
     ['info', 'pslist', 'psscan', 'netscan', 'netstat', 'cmdline', 'dlllist']),
]:
    for plugin in plugins:
        commande = ['vol', '--offline', '-q', '-s', '/symboles', '-r', 'json',
                    '-f', fichier, 'windows.' + plugin]
        if not commandes:
            # Prendre en compte les symboles ajoutes ou corriges depuis le dernier lancement.
            commande.insert(1, '--clear-cache')
        if plugin in ('cmdline', 'dlllist'):
            # PID de Res.exe dans le premier essai, releve dans Process Monitor.
            commande += ['--pid', '6064']
        print(f'{nom} : windows.{plugin}...', flush=True)
        debut = datetime.now(timezone.utc).isoformat()
        with (sortie / f'{nom}-{plugin}.json').open('w') as resultat, \
                (sortie / f'{nom}-{plugin}.log').open('w') as journal:
            retour = subprocess.run(commande, stdout=resultat, stderr=journal)
        commandes.append({'commande': commande, 'debut_utc': debut,
                          'fin_utc': datetime.now(timezone.utc).isoformat(),
                          'code_sortie': retour.returncode})
        (sortie / 'commandes.json').write_text(json.dumps(commandes, indent=2) + '\n')
        retour.check_returncode()
        # Certains plugins signalent une erreur tout en retournant le code 0.
        journal = (sortie / f'{nom}-{plugin}.log').read_text()
        if any(ligne.startswith('ERROR') for ligne in journal.splitlines()):
            raise RuntimeError(f'{nom}-{plugin} : consulter le journal dans resultats.')
        json.loads((sortie / f'{nom}-{plugin}.json').read_text())

(sortie / 'versions.json').write_text(json.dumps({
    nom: version(nom) for nom in ('volatility3', 'pyelftools', 'pefile', 'jsonschema')
}, indent=2) + '\n')
print('Analyse terminee. Resultats dans us6/resultats.', flush=True)
