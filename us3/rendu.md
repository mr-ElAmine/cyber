# US3 — Analyse statique

*Résultats du 10 septembre 2026.*

J’ai examiné `Res.exe` et `Env.exe` sans les exécuter : **pefile** pour la structure et les imports, **objdump** pour les instructions du programme.

## Résultats

| Élément | Résultat de la lecture du code |
| --- | --- |
| Structure | Deux exécutables Windows 32 bits (PE32 x86), huit sections chacun. Aucune section déclarée à la fois inscriptible et exécutable. |
| `Res.exe` | Interroge le clavier avec `GetAsyncKeyState` et `GetKeyState`, écrit dans `C:\WindSyst\log.txt` et prévoit l’installation des fichiers et des valeurs de démarrage. |
| `Env.exe` | Lit le journal et prépare son envoi par courriel chiffré vers `smtp.laposte.net:465`. |

L’appel à `GetAsyncKeyState` est visible à l’adresse **`0x40167e`**, via l’entrée d’import **`0x409368`**. La conclusion s’appuie donc sur une instruction qui appelle cette fonction.

Les principaux indicateurs sont :

- Les fichiers `Res.exe`, `Env.exe` et `log.txt` dans `C:\WindSyst`.
- Les valeurs `Res` et `Env` dans `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Le serveur configuré `smtp.laposte.net:465`, qui reste un service légitime : ce domaine seul ne prouve pas une infection.

**US3 validée : fonctions principales, structure et indicateurs identifiés.** Ces résultats décrivent le code ; ils ne prouvent ni une collecte complète des touches ni un envoi réussi. L’US4 confronte ces capacités à l’exécution.

## Commande utile

Depuis le projet, avec Docker et le volume d’échantillons disponibles :

```bash
# Préparer les outils et analyser les fichiers sans les lancer.
bash us3/analyse.sh
```

Le script prépare l’image, crée le dossier de sortie, puis lance l’analyse. Il remplace les résultats automatiques. Les réglages sont dans [compose.yaml](compose.yaml), le traitement dans [analyse.py](analyse.py).

[Résultats](resultats/analyse.json) · [Indicateurs](iocs.csv) · [Instructions de Res.exe](resultats/Res.exe.asm.txt) · [Instructions d’Env.exe](resultats/Env.exe.asm.txt) · [Référence détaillée](../V1/us3/rendu.md).
