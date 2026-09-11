# US 7 — Acquisition du disque dur

**Acquisition et analyse du 10 septembre 2026. Les trois critères de l’US 7 sont validés.**

Une image RAW du disque du premier essai a été réalisée et comparée intégralement au snapshot source : **68 719 476 736 octets, soit 64 Gio, sans aucune différence**. L’analyse de cette copie retrouve les deux exécutables suspects `Res.exe` et `Env.exe`, leurs copies dans `C:\WindSyst` et le journal `log.txt`.

## 1. Objectif et source

L’US 7, page 13 du backlog, demande une image disque forensique pour examiner les fichiers et les traces laissées par l’attaquant.

La source est le **snapshot interne `malware-first-run`, ID 2**, du fichier `windows.qcow2`, conservé dans le volume Docker `cyber-windows_windows-disk`. Sa date enregistrée est le **10 septembre 2026 à 12:50:44 UTC**, selon l’horloge hôte. Les [métadonnées de la source](resultats/source.json) identifient le snapshot et la capacité du disque.

Ce snapshot conserve le disque après le premier essai, déjà utilisé en US 4. Il appartient à la même séance que les dumps RAM de l’US 6, mais à un instant ultérieur : la capture RAM après lancement avait été demandée vers 12:37 UTC, horloge hôte. Les deux acquisitions ne sont pas simultanées.

La VM est restée arrêtée pendant cette US. Le snapshot a été lu directement, sans restaurer cet état dans le disque actif et sans lancer les exécutables.

## 2. Image bit-à-bit

L’image produite est conservée localement dans `us7/images/windows-first-run.raw`. Elle représente **tous les secteurs logiques du disque virtuel sélectionné**, y compris les zones hors fichiers alloués du système de fichiers. La portée de l’acquisition est le disque Windows virtuel dans l’état de ce snapshot.

La commande principale, exécutée dans Docker, est :

```bash
qemu-img convert -p -f qcow2 -l snapshot.name=malware-first-run \
  -O raw -S 4k /storage/windows.qcow2 /images/windows-first-run.raw
```

`-l` sélectionne le snapshot ; `-O raw` produit une image brute ; `-p` affiche la progression. `-S 4k` économise l’espace occupé par les suites de zéros, tout en conservant leur lecture comme des zéros. Ces options sont décrites dans la [documentation de qemu-img](https://www.qemu.org/docs/master/tools/qemu-img.html).

| Propriété | Résultat |
|---|---|
| Outil d’acquisition | QEMU / `qemu-img` **10.0.11** |
| Début de conversion, UTC hôte | **10/09/2026 19:08:33** |
| Fin de conversion, UTC hôte | **10/09/2026 19:08:48** |
| Format | RAW, fichier à allocation clairsemée (*sparse*) |
| Taille logique | **68 719 476 736 octets — 64 Gio** |
| Espace réellement alloué sur le Mac | **9 260 417 024 octets — environ 8,6 Gio** |
| Contrôle QCOW2 avant acquisition | `qemu-img check`, **0 erreur**, sans option de réparation |

Preuves : [version QEMU](resultats/qemu-version.txt), [début](resultats/acquisition-debut.txt), [fin](resultats/acquisition-fin.txt), [image RAW](resultats/image.json), [contrôle de la source](resultats/controle-source.json).

L’allocation clairsemée économise uniquement le stockage des zones nulles sur le Mac. Les **64 Gio du contenu logique ont été relus et comparés**.

## 3. Intégrité et protection des preuves

Le script [verifier.py](verifier.py) lit le snapshot avec **Dissect**, puis lit l’image RAW séparément. Il compare les deux flux par blocs de 16 Mio, calcule leurs SHA-256 et contrôle la taille ainsi que la fin du fichier. Cette vérification complète s’est terminée à **19:10:41 UTC**.

Les deux empreintes sont identiques :

```text
SHA-256 du disque logique source et de la copie RAW :
9b0b50283470c02c0a26ec6af766f85c40589fb447d33395bed392b5c06e70a4
```

Le [résultat d’intégrité](resultats/integrite.json) confirme `identique_octet_par_octet: true` pour les **68 719 476 736 octets comparés**. Le fichier [SHA256SUMS](resultats/SHA256SUMS) permet un contrôle ultérieur de l’image.

Pendant l’acquisition, le volume source est monté en lecture seule. Pendant la vérification et l’analyse, source et image sont également en lecture seule. Les conteneurs n’ont aucun réseau, leur racine est en lecture seule et toutes leurs capacités Linux sont retirées. Les sorties sont écrites dans `us7/resultats`.

L’image est protégée en lecture seule sur le Mac, mode `0444`, et exclue de Git. Les preuves de configuration sont dans [environnement.json](resultats/environnement.json) et l’[état de la VM](resultats/etat-vm.json). Le script d’acquisition refuse une VM en cours d’exécution et refuse d’écraser une image existante.

## 4. Lecture du système de fichiers

L’analyse s’effectue directement sur la copie RAW, à l’aide de **dissect.volume 3.18** et **dissect.ntfs 3.16**. Aucun montage Windows ni démarrage de la VM n’est nécessaire. **dissect.hypervisor 3.21** sert à la lecture indépendante du snapshot QCOW2 pour la comparaison.

Trois partitions sont retrouvées :

| Partition | Décalage en octets | Taille en octets | Type relevé |
|---|---:|---:|---|
| 1 | 1 048 576 | 52 428 800 | `0x07` |
| 2 — volume Windows analysé | 53 477 376 | 68 115 153 920 | `0x07` |
| 3 | 68 168 974 336 | 548 405 248 | `0x27` |

Les [valeurs brutes des partitions](resultats/partitions.json) sont conservées. L’accès aux enregistrements NTFS de la partition 2 et le calcul des empreintes des fichiers confirment que l’image est exploitable.

## 5. Fichiers suspects et traces retrouvés

L’inventaire ciblé couvre `C:\Lab\sample\virus`, `C:\WindSyst`, la trace du premier essai et la ruche du compte Analyste. Il contient **21 fichiers**, avec chemin, taille, SHA-256 et rôle : [fichiers.csv](resultats/fichiers.csv), [résultats JSON](resultats/analyse.json).

| Fichier | Emplacements retrouvés | Taille | Interprétation |
|---|---|---:|---|
| **`Res.exe`** | `C:\Lab\sample\virus\Res.exe` et `C:\WindSyst\Res.exe` | **25 088 octets** par copie | Exécutable suspect étudié en US 3 et observé en US 4. |
| **`Env.exe`** | `C:\Lab\sample\virus\Env.exe` et `C:\WindSyst\Env.exe` | **53 248 octets** par copie | Composant d’envoi étudié en US 3 ; sa présence sur disque ne prouve pas un envoi réussi. |
| **`log.txt`** | `C:\WindSyst\log.txt` | **82 octets** | Journal associé au malware par les observations dynamiques de l’US 4. |
| Sept DLL, chacune dans les deux dossiers | `Qt5Core`, `Qt5Gui`, `Qt5Network`, `Qt5Widgets`, `libgcc_s_dw2-1`, `libstdc++-6`, `libwinpthread-1` | Tailles et empreintes dans le CSV | Bibliothèques accompagnant les exécutables ; leur présence seule n’en fait pas des malwares. |
| `trace.pml` | `C:\Lab\trace.pml` | **80 058 537 octets** | Trace Process Monitor créée par l’analyste, utile comme preuve. |
| `NTUSER.DAT` | `C:\Users\Analyste\NTUSER.DAT` | **786 432 octets** | Ruche utilisateur préservée pour examiner les valeurs de démarrage en US 8. |

Empreintes des exécutables :

```text
Res.exe : 49f091ade48890bfa22d2b455494be95e52392c478b67e10626222b6aee37e1e
Env.exe : e09ec2098363a129de143fdaf73ad6e2e61266fba3f638a25214af3a8bc8f2f2
```

Pour chaque programme, les copies du dossier de test et de `C:\WindSyst` correspondent exactement aux [empreintes de référence de l’US 2](../us2/hashes.json). Ces empreintes permettent d’identifier le contenu des fichiers retrouvés.

Le journal a pour SHA-256 `c105fab312066173c97a49f27da7306425cd7f4c184201bfd0b159af6b4edf38`. La trace PML a pour SHA-256 `0853884c7af540bab2252ac4491070614d0851909804555252be073d24be5bae`. Ces valeurs correspondent aux [relevés du premier essai en US 4](../us4/resultats/resume.json).

Les exécutables sont lus pour calculer leurs empreintes ; ils restent dans l’image. Cet inventaire ciblé n’est pas une recherche exhaustive de tous les fichiers supprimés ou de tous les emplacements de persistance du disque. La présence d’un fichier ne démontre pas, à elle seule, son exécution ni une exfiltration.

## 6. Scripts et démonstration

Depuis la racine du projet, l’acquisition initiale a été réalisée avec :

```bash
bash us7/acquerir.sh
```

L’image existe maintenant. Pour relancer seulement son analyse :

```bash
bash us7/analyse.sh
```

Les scripts ne prennent aucun argument. Docker doit être démarré. L’analyse utilise l’image Docker construite pendant l’acquisition et remplace les relevés de fichiers dans `resultats` ; l’image RAW est montée en lecture seule.

Pour la démonstration, montrer la comparaison intégrale et le SHA-256, ouvrir le CSV, puis comparer les deux chemins de `Res.exe` et leurs empreintes. Cela illustre la différence entre le programme introduit dans le laboratoire et sa copie installée dans Windows.

## 7. Critères d’acceptation

- [x] **Image disque bit-à-bit réalisée** : image RAW du snapshot sélectionné, 64 Gio de contenu logique comparés intégralement, sans différence.
- [x] **Les outils utilisés** : QEMU 10.0.11, Docker, Dissect et SHA-256 ; versions et scripts conservés.
- [x] **Fichiers suspects identifiés** : `Res.exe` et `Env.exe` retrouvés aux deux emplacements, identiques aux échantillons de référence ; journal et traces associés inventoriés.
