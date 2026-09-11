# US7 — Acquisition du disque dur

*Résultats du 10 septembre 2026.*

J’ai créé une copie RAW du disque Windows depuis le snapshot **`malware-first-run`**, VM arrêtée, puis examiné les fichiers avec **Dissect** dans Docker.

## Résultats

| Contrôle | Résultat |
| --- | --- |
| Acquisition | **64 Gio**, soit 68 719 476 736 octets, copiés avec QEMU **10.0.11**. |
| Intégrité | Comparaison complète avec le snapshot : **aucune différence**, SHA-256 identiques. |
| Lecture du disque | Trois partitions retrouvées ; Windows analysé sur la partition **2**. |
| Exécutables | `Res.exe` et `Env.exe` présents dans `C:\Lab\sample\virus` et `C:\WindSyst`, conformes aux empreintes de l’US2. |
| Traces | `log.txt` (**82 octets**), trace Process Monitor et registre utilisateur retrouvés. **21 fichiers** inventoriés au total. |

**US7 validée : image bit-à-bit réalisée, outils documentés et fichiers suspects identifiés.** L’inventaire est ciblé, pas exhaustif. La présence des exécutables sur disque ne prouve pas leur exécution. Le snapshot provient du premier essai, après la capture RAM de l’US6.

## Commandes utiles

Depuis le projet, avec Docker lancé et les images Docker du laboratoire disponibles :

```bash
# Acquisition initiale : la VM doit être arrêtée et la copie absente.
bash us7/acquerir.sh

# Avec la copie déjà présente : relire uniquement les fichiers.
bash us7/analyse.sh
```

L’analyse fonctionne hors réseau, lit la copie sans la modifier et remplace les relevés dans `resultats/`.

Le dossier `script/` sépare les étapes : [copier le disque](script/acquerir_disque.sh), [vérifier la copie](script/verifier_image.py), puis [inventorier les fichiers](script/analyser_disque.py).

[Comparaison et SHA-256](resultats/integrite.json) · [Inventaire](resultats/fichiers.csv) · [Configuration Docker](compose.yaml).
