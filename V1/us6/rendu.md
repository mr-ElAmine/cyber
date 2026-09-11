# US 6 — Acquisition mémoire vive

**Analyse du 10 septembre 2026. Les quatre critères de l’US 6 sont traités.**

Les deux captures RAM du premier essai sont intègres et exploitables. Volatility permet d’identifier **79 processus actifs avant le lancement et 101 après**, dont **`Res.exe`, PID 6064**. Aucune connexion réseau suspecte n’est relevée dans les structures examinées.

## 1. Objectif et périmètre

L’US 6, page 12 du backlog, demande d’acquérir la mémoire vive pour retrouver des processus malveillants ou des traces d’attaque. La RAM conserve notamment l’état des processus et des connexions au moment de la capture : elle permet ici de confirmer que `Res.exe` était en cours d’exécution.

Nous réutilisons les dumps pris **avant et pendant le premier essai**, déjà conservés dans le laboratoire. L’US 6 réalise leur contrôle et leur analyse ; elle n’effectue aucune nouvelle exécution du malware. Ces captures ne correspondent pas au second essai de l’US 4, dans lequel les PID étaient différents.

## 2. Acquisition et conservation

L’acquisition a été effectuée depuis **QEMU 10.0.11**, via son moniteur HMP et `socat`. Volatility intervient ensuite pour lire les captures ; il ne réalise pas lui-même l’acquisition. Voir la [documentation Windows de Volatility](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html).

Commandes exécutées lors de l’acquisition initiale :

```bash
docker exec -i cyber-windows-vm-1 socat -t 2 - UNIX-CONNECT:/tmp/qemu-monitor.sock <<'EOF'
dump-guest-memory -d /storage/windows-before-malware.elf
info dump
EOF
```

Puis, pendant que `Res.exe` était actif :

```bash
docker exec -i cyber-windows-vm-1 socat -t 2 - UNIX-CONNECT:/tmp/qemu-monitor.sock <<'EOF'
dump-guest-memory -d /storage/windows-after-malware.elf
info dump
EOF
```

L’option `-d` lance l’export en arrière-plan : le premier `info dump` peut donc annoncer `active`. Le contrôle a été répété jusqu’à **`Status: completed` pour chaque fichier**. Aucune plage de mémoire restreinte n’a été demandée. Le format utilisé est ELF, conformément à la commande [QEMU `dump-guest-memory`](https://www.qemu.org/docs/master/interop/qemu-qmp-ref.html#command-dump-guest-memory).

| Capture | Demande dans l’historique hôte, UTC | Fin constatée, UTC | Horloge Windows lue en mémoire |
|---|---|---|---|
| Avant | 10/09/2026 12:20:19.850 | 12:20:34.734 | 10:20:18, valeur `SystemTime` |
| Après | 10/09/2026 12:37:04.822 | 12:37:51.318 | 10:36:59, valeur `SystemTime` |

Les dates hôte sont celles des messages de demande et de constat de fin, pas une mesure exacte de l’instant de capture. Les horloges hôte et Windows sont distinctes ; leurs valeurs ne sont pas mélangées. La [fiche d’acquisition](resultats/acquisition.json) conserve cette provenance.

Les deux fichiers mesurent chacun **4 311 943 347 octets** :

| Capture | SHA-256, recalculé et conforme au relevé initial |
|---|---|
| `windows-before-malware.elf` | `2663c98d783404068dbba24ee62f166a0f9417d2cf649a20b053ff5e16b5e9a1` |
| `windows-after-malware.elf` | `f1c5d532807b5ffba91b8dbb2c4ed0cb1edcb5912ac1d4083da83fd3fc945cc9` |

La capture initiale est conservée dans `infrastructure/windows/results/windows-before-malware.elf`. Son déplacement hors du volume Docker, avec contrôle d’empreinte, est documenté dans la [preuve US 4](../us4/resultats/deplacement-memoire.json). La capture après exécution reste dans le volume `cyber-windows_windows-disk`, fichier `/windows-after-malware.elf`. Les dumps et les symboles téléchargés sont exclus de Git.

## 3. Contrôle du dump et environnement d’analyse

Le script [verifier.py](verifier.py) recalcule les SHA-256 et inspecte les en-têtes avec **pyelftools 0.32**. Pour chaque capture :

- ELF 64 bits, little-endian, type `ET_CORE`, architecture x86-64 ;
- six segments physiques `PT_LOAD`, entièrement présents dans le fichier ;
- tailles fichier et mémoire identiques pour chaque segment, sans chevauchement des plages physiques ;
- **4 311 941 120 octets** de régions physiques exportées, pour une VM configurée avec 4 Gio de RAM et ses mappages supplémentaires.

Les résultats et les plages exactes sont dans [integrite.json](resultats/integrite.json). Le fichier ELF décrit des régions physiques discontinues : les intervalles non mappés ne sont pas assimilés à une troncature du fichier. Le contrôle valide la complétude des régions déclarées par QEMU, pas la présence des pages qui auraient été déplacées vers le fichier d’échange Windows.

L’analyse utilise **Volatility 3, version 2.28.0**. Les versions exactes des dépendances sont conservées dans [versions.json](resultats/versions.json). `windows.info` reconstruit les couches `FileLayer → Elf64Layer → WindowsIntel32e`, reconnaît Windows 10 x64 et retrouve les deux processeurs virtuels. Cela prouve que le contenu est effectivement interprétable, au-delà d’un simple fichier de la bonne taille. Voir les sorties [avant](resultats/avant-info.json) et [après](resultats/apres-info.json).

Les symboles Microsoft correspondant au noyau `ntkrnlmp.pdb` et au pilote `tcpip.pdb` ont été téléchargés et convertis dans un conteneur de préparation **sans aucun dump monté**. Leurs identifiants et empreintes figurent dans [symboles.json](resultats/symboles.json). Ils servent à reconnaître les structures Windows en mémoire.

L’analyse s’exécute dans Docker avec `--network none`, `vol --offline`, les captures montées en lecture seule, une racine en lecture seule et toutes les capacités Linux retirées. Seuls les résultats et le cache sont inscriptibles. La VM Windows reste arrêtée ; son [état contrôlé](resultats/environnement.json) indique une sortie propre et un réseau Docker `none`.

## 4. Processus identifiés

| Lecture | Résultat | Preuve |
|---|---|---|
| `windows.pslist`, avant | 79 processus ; aucun `Res.exe` ni `Env.exe` | [Liste avant](resultats/avant-pslist.json) |
| `windows.pslist`, après | 102 entrées, dont 101 processus actifs et `Res.exe` | [Liste après](resultats/apres-pslist.json) |
| `windows.psscan`, après | 107 objets processus, dont le même `Res.exe` | [Scan mémoire](resultats/apres-psscan.json) |

Le décompte actif retient les entrées sans date de sortie et avec au moins un thread. La liste après contient aussi `userinit.exe`, PID 3636, déjà terminé à 10:21:07 selon `ExitTime`, avec zéro thread : ses 102 entrées correspondent donc à **101 processus actifs** selon ces champs.

Les cinq objets supplémentaires du scan sont également des processus terminés : leurs champs `ExitTime` sont renseignés et ils ont zéro thread. Ce sont `WmiPrvSE.exe` (2576), `MicrosoftEdgeU` (3416, nom tel que relevé) et trois `svchost.exe` (4748, 5524, 2972). Le nombre d’objets retrouvés par scan n’est donc pas le nombre de processus encore actifs.

Pour `Res.exe`, les lectures se recoupent :

| Champ | Observation |
|---|---|
| PID / parent | **6064**, parent **5236 — `powershell.exe`** |
| Création, horloge Windows | **10/09/2026 10:33:34 UTC** |
| État | Dans la liste active, deux threads, aucune date de sortie |
| Architecture | Processus 32 bits sous Windows x64 (`Wow64: true`) |
| Chemin | `Res.exe` dans le répertoire `C:\lab\sample\virus` |
| Modules | 38 lignes dans `dlllist`, notamment `Qt5Core.dll`, `USER32.dll` et `WS2_32.dll` |

La [ligne de commande](resultats/apres-cmdline.json) et les [modules chargés](resultats/apres-dlllist.json) confirment le chemin du programme. Le PID, le parent et l’heure de création correspondent au démarrage relevé par Process Monitor dans le premier essai : événement **100806**, décrit dans le [rendu US 4](../us4/rendu.md). L’identification ne repose donc pas uniquement sur un nom de processus. Aucun `Env.exe` n’est retrouvé par `pslist` ou `psscan` dans ces captures.

La présence de `USER32.dll` ou de `WS2_32.dll` ne prouve respectivement ni une capture clavier ni une communication réseau : l’interprétation malveillante s’appuie aussi sur les analyses statique et dynamique précédentes.

## 5. Recherche de connexions suspectes

Deux méthodes sont utilisées : [`windows.netscan`](https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.netscan.html) recherche les objets réseau dans la mémoire ; [`windows.netstat`](https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.netstat.html) parcourt les structures de suivi réseau de Windows.

| Capture / méthode | Lignes relevées | Observation |
|---|---:|---|
| Avant, `netscan` | 33 | Écoutes TCP et objets UDP ; aucune destination distante concrète |
| Après, `netscan` | 30 | Même constat ; aucune entrée attribuée à `Res.exe` |
| Après, `netstat` | 28 | 22 lignes TCP `LISTENING` et six lignes UDP ; aucune connexion TCP établie |

Preuves : [avant-netscan.json](resultats/avant-netscan.json), [apres-netscan.json](resultats/apres-netscan.json), [apres-netstat.json](resultats/apres-netstat.json).

Ces nombres comptent des lignes de résultats, avec des doublons et des vues IPv4/IPv6 ; ils ne désignent pas autant de connexions actives. Les adresses distantes affichées sont uniquement `0.0.0.0`, `::` ou `*`, avec un port distant nul. Elles n’identifient aucun serveur extérieur. Les propriétaires relevés sont des processus Windows tels que `svchost.exe`, `lsass.exe`, `wininit.exe`, `spoolsv.exe` et `services.exe`.

**Aucune connexion suspecte n’est identifiée dans les résultats examinés**, aucune entrée n’est attribuée au PID 6064 et aucun port 465 n’apparaît. Ce constat porte sur les structures récupérées à ces instants, dans une VM isolée. Il ne permet pas d’exclure une connexion passée dont les traces auraient disparu, ni de prouver un envoi SMTP dans un autre environnement. La limite réseau documentée en US 4 reste donc présente.

## 6. Reproduire l’analyse

Depuis la racine du projet, avec Docker démarré et les deux captures conservées à leur emplacement :

```bash
bash us6/preparer.sh
bash us6/analyse.sh
```

La première commande construit l’image et prépare les symboles publics. Une fois la préparation effectuée, **`bash us6/analyse.sh` suffit** pour relancer le contrôle des empreintes et l’analyse hors réseau. Aucun argument à fournir. Les scripts correspondent à ces captures et à leur premier essai, notamment le PID 6064.

Le [journal des commandes](resultats/commandes.json) conserve les dix appels Volatility, leurs horaires et leurs codes de sortie. Ils se terminent tous avec le code 0 et des résultats JSON lisibles ; les journaux associés ne signalent pas d’erreur. Les résultats sont remplacés lors d’une nouvelle analyse, les dumps restent en lecture seule.

## 7. Critères d’acceptation

- [x] **Les outils/commandes utilisés** : acquisition QEMU/HMP, contrôle SHA-256 et ELF, analyse Volatility dans Docker, commandes conservées.
- [x] **Le dump RAM est complet et exploitable** : captures terminées, empreintes conformes, segments déclarés complets et structures Windows effectivement lues. La portée exclut le fichier d’échange.
- [x] **Les processus actifs sont identifiés** : listes avant/après et identification recoupée de `Res.exe`, PID 6064.
- [x] **Les connexions réseau suspectes sont relevées** : recherche effectuée par deux méthodes ; aucune connexion suspecte retrouvée dans les captures, avec les limites précisées ci-dessus.

Pour la démonstration, montrer les empreintes, comparer les deux listes de processus, ouvrir la ligne de commande de `Res.exe`, puis expliquer pourquoi une écoute `LISTENING` n’est pas une preuve d’envoi vers Internet.
