# US6 — Analyse de la mémoire vive

*Résultats du 10 septembre 2026.*

J’ai analysé avec **Volatility 3 (2.28.0)** les captures mémoire prises par **QEMU** avant et pendant le premier essai du malware.

## Résultats

| Contrôle | Résultat |
| --- | --- |
| Intégrité | Deux captures ELF64, empreintes SHA-256 conformes et six segments mémoire complets chacune. |
| Avant l’essai | **79 processus actifs**, aucun `Res.exe` ni `Env.exe`. |
| Pendant l’essai | **101 processus actifs sur 102 entrées**, dont `Res.exe`, PID **6064**, avec deux threads. |
| Identification | `Res.exe` lancé depuis `C:\lab\sample\virus`, parent PowerShell **5236** : cohérent avec Process Monitor. |
| `Env.exe` | Absent des listes de processus et du scan mémoire. |
| Réseau | Aucune connexion suspecte retrouvée avec `netscan` et `netstat`, aucune entrée attribuée à `Res.exe`. |

La liste après lancement contient aussi un processus terminé, d’où la différence entre 102 entrées et 101 processus actifs.

**US6 validée : captures exploitables, processus identifiés et connexions recherchées.** La complétude concerne les régions mémoire déclarées, pas le fichier d’échange Windows. L’absence de connexion dans ces captures ne prouve pas l’absence de toute communication passée.

## Commandes utiles

Depuis le projet, avec Docker lancé et les captures conservées :

```bash
# Préparer Volatility et les symboles Microsoft.
bash us6/preparer.sh

# Vérifier les captures et analyser leur contenu.
bash us6/analyse.sh
```

La préparation télécharge les symboles sans accéder aux captures. L’analyse est hors réseau et remplace les résultats ; les captures restent en lecture seule. Après préparation, seule la deuxième commande est nécessaire.

## Organisation du code

Dans `script/`, les étapes se lisent dans cet ordre :

1. [Télécharger](script/telecharger_symboles.py) les symboles Microsoft.
2. [Convertir](script/convertir_symboles.py) ces fichiers pour Volatility.
3. [Vérifier](script/verifier_captures.py) les captures mémoire.
4. [Analyser](script/analyser_memoire.py) les processus et le réseau.

[references.py](script/references.py) contient les chemins et les identifiants ; [verifier_elf.py](script/verifier_elf.py) contrôle le format mémoire ; [volatility.py](script/volatility.py) lance les commandes et enregistre les résultats.

[Configuration Docker](compose.yaml) · [Acquisition](resultats/acquisition.json) · [Intégrité](resultats/integrite.json) · [Processus avant](resultats/avant-pslist.json) · [Processus après](resultats/apres-pslist.json) · [Réseau](resultats/apres-netstat.json).
