# US4 — Analyse dynamique

*Résultats du 10 septembre 2026.*

J’ai observé les programmes dans la VM Windows isolée avec **Process Monitor**. Les deux essais ont produit des traces de **218 035** et **472 737 événements**.

## Résultats

| Élément | Observation |
| --- | --- |
| Processus | Premier essai : `Res.exe` (PID 6064) lance 15 `cmd.exe` et 13 `xcopy.exe`. |
| Installation | Deux EXE et sept DLL copiés dans `C:\WindSyst`, avec des empreintes conformes. |
| Persistance | Valeurs `Res` et `Env` écrites dans la clé Run de l’utilisateur, vers les copies installées. Relancement automatique non testé. |
| Journal | Premier essai : neuf écritures d’un octet dans `log.txt`. Le fichier final mesure 82 octets, à un instant ultérieur. La phrase de test complète est absente. |
| `Env.exe` | Second essai : échec au démarrage, plugin Qt « windows » manquant, sortie avec le code 3. Aucun `log.txt` dans cet essai. |
| Réseau | Aucun événement réseau dans la seconde trace, capture réseau activée. Aucun envoi SMTP observé. |

**Deux critères validés : modifications système et création de fichiers/processus. Le critère réseau reste partiellement validé** : la VM est hors réseau et `Env.exe` échoue au démarrage.

Le disque a été restauré à l’état propre après conservation des essais.

## Commande utile

Depuis le projet, avec Docker lancé, la VM arrêtée et les snapshots conservés :

```bash
# Analyser les traces existantes sans relancer le malware.
bash us4/analyse.sh
```

Les résultats automatiques sont remplacés. La configuration est dans [compose.yaml](compose.yaml), le traitement dans [analyse.py](analyse.py).

[Premier essai](resultats/resume.json) · [Second essai](resultats/second-resume.json) · [Erreur Qt](resultats/observation-env.json) · [Restauration](resultats/restauration.json).
