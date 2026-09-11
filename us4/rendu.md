# US 4 — Analyse dynamique

## Objectif

Observer les actions réelles des deux exécutables du lot étudié en US 2 et US 3 : modifications du système, fichiers et processus créés, et activité réseau. L'analyse porte sur les fichiers originaux, sans modifier leur code ni compléter leurs dépendances.

## Méthode et preuves

Windows 10 x64 est émulé par QEMU dans Docker. Le service VM utilise `network_mode: none` et QEMU `-nic none`. Les fichiers sont apportés sur un DVD virtuel en lecture seule. La console noVNC est accessible sur le Mac à l'adresse locale `127.0.0.1:6085`.

La première capture est conservée dans le snapshot `malware-first-run`. Le script [analyse.py](analyse.py) lit ce snapshot et le snapshot de référence `windows-clean-us1` directement, sans démarrer Windows. Le volume est monté en lecture seule dans un conteneur sans réseau. Dissect lit QCOW2, NTFS et le registre ; `procmon-parser` décode la trace PML. Les versions sont consignées dans [resume.json](resultats/resume.json).

Process Monitor enregistre les opérations sur les fichiers, le registre et les processus ; une opération réussie constitue une preuve plus précise que la seule présence d'un nom de fonction dans les imports. [Documentation Microsoft](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon).

## Premier essai : `Res.exe`

Trace `C:\Lab\trace.pml`, 80 058 537 octets, **218 035 événements**.

SHA-256 : `0853884c7af540bab2252ac4491070614d0851909804555252be073d24be5bae`.

La fenêtre enregistrée va de 10:32:32 à 10:36:32 le 10 septembre 2026, selon les horodatages Windows convertis en UTC. L'horloge invitée n'est pas considérée comme synchronisée avec celle du Mac. Les valeurs FILETIME originales sont conservées dans le CSV.

| Observation | Preuve | Interprétation |
|---|---|---|
| Démarrage de `Res.exe`, PID 6064 | Événement 100806 | L'exécutable a effectivement été lancé. |
| 15 créations de `cmd.exe`, puis 13 de `xcopy.exe` | Arbre de 29 processus et lignes de commande du résumé JSON | Le programme lance ses commandes d'installation. |
| Valeur Run `Res` = `C:\WindSyst\Res.exe` | `RegSetValue` réussi, événement 142639 | Configuration d'un lancement à l'ouverture de session. |
| Valeur Run `Env` = `C:\WindSyst\Env.exe` | `RegSetValue` réussi, événement 142667 | Même mécanisme pour le second exécutable. |
| Deux EXE et sept DLL dans `C:\WindSyst` | Comparaison NTFS avant/après et empreintes | Les copies finales sont présentes ; les EXE correspondent aux originaux. |
| Neuf écritures d'un octet dans `C:\WindSyst\log.txt` | `WriteFile` réussis par `Res.exe` | Une écriture du journal est observée pendant la capture. |

Les numéros d'événements commencent à 1 dans [evenements.csv](resultats/evenements.csv). Ce fichier contient 529 événements sélectionnés ; la trace complète reste dans le snapshot.

Neuf processus `xcopy.exe` terminent avec le code 0, quatre avec le code 4. Les quatre commandes concernent `Qt5Cored.dll` et trois plugins Qt absents de l'archive. Le code 4 signale une erreur d'initialisation, dont la cause précise ne se déduit pas du seul code. [Codes de retour Microsoft](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/xcopy).

Dans le snapshot final, `log.txt` mesure **82 octets**. La phrase synthétique complète `LAB TEST 12345` n'y est pas présente. Les neuf octets écrits pendant la fenêtre PML, le relevé intermédiaire de 40 octets en US 1 et les 82 octets du snapshot final correspondent à des instants différents. La trace ne contient pas la fin du processus : elle ne couvre donc pas toute sa durée de vie.

## Second essai : lancement explicite de `Res.exe` et `Env.exe`

L'essai repart du snapshot propre. [preparer.cmd](preparer.cmd) copie les outils, extrait l'archive originale, relève les empreintes et la configuration réseau, puis ouvre Process Monitor. Après contrôle de l'isolation, [tester.cmd](tester.cmd) lance `Res.exe`, attend 15 secondes, lance `Env.exe`, puis attend 60 secondes avant de relever l'état et d'arrêter les processus encore présents. Ce sont des délais demandés, pas une garantie de durée exacte sous émulation.

La capture a été arrêtée, puis Process Monitor fermé avant l'arrêt normal de Windows. Le nouvel état est conservé dans le snapshot **`us4-controlled-run`**.

Trace `C:\Lab\us4.pml`, **199 710 415 octets**, **472 737 événements**, de 13:57:58 à 14:04:50 selon l'horloge Windows convertie en UTC. L'essai lui-même est journalisé de 16:02:42 à 16:04:03 en heure locale Windows dans [essai.txt](resultats/essai.txt).

SHA-256 : `512cb0d2e493fba7664c7334d4a3181870b51ff707a8c4b49df9d84ad06f1c12`.

| Observation | Événement de la seconde trace |
|---|---|
| Démarrage de `Res.exe`, PID 3332 | 314408 |
| Écriture réussie des valeurs Run `Res` et `Env` | 362327 et 362350 |
| Démarrage explicite d'`Env.exe`, PID 5832 | 372582 |
| Échec d'ouverture de `C:\Lab\sample\VIRUS\platforms`, statut `0xc0000034` | 376769 |
| Création de `WerFault.exe` après l'erreur d'Env | 397254 |
| Sortie d'`Env.exe` avec **Exit Status 3** | 432152 |
| Sortie de `Res.exe` avec **Exit Status 1**, après le `taskkill` du script | 457712 |

La console affiche une erreur indiquant que le plugin de plateforme Qt **« windows »** est introuvable ou ne peut pas être chargé. [Observation de la boîte de dialogue](resultats/observation-env.json). Le blocage au démarrage concorde avec l'absence de plugins dans l'archive et l'échec d'accès au dossier `platforms`. Aucun plugin n'a été ajouté au lot.

Le snapshot final contient les deux EXE et les sept DLL copiés dans `C:\WindSyst`, avec les mêmes empreintes que lors du premier essai. Il ne contient pas de `log.txt` : aucune phrase de test n'a été saisie pendant ce second essai. Les écritures du journal observées lors du premier essai restent une preuve distincte.

Le parseur référence également le PID 4772 sous le nom `Env.exe`, uniquement dans neuf événements de profilage, sans événement de démarrage associé. Ces entrées ne suffisent pas à conclure à un second lancement autonome du malware. Les modifications de la clé Windows `bam` enregistrées à la fermeture ne sont pas assimilées aux valeurs Run posées par son code.

Les détails sont dans [second-resume.json](resultats/second-resume.json) et [second-evenements.csv](resultats/second-evenements.csv), qui contient **2 419 événements sélectionnés**.

## Réseau : résultat et limite

Aucun événement `Env.exe` n'apparaît dans la première trace, et aucune entrée de classe réseau n'y est enregistrée, tous processus confondus. Cela ne démontre ni l'absence de capacité réseau du malware, ni l'activation de cette catégorie dans la première capture.

Lors du second essai, les catégories de capture, dont le réseau, étaient activées dans Process Monitor ; l'option `Drop Filtered Events` était décochée. [Contrôles de l'isolation et observations de la console](resultats/isolation.json).

- [Avant l'essai](resultats/reseau-avant.txt) : routes sur l'interface de boucle locale, aucune route par défaut IPv4 ou IPv6. Les miniports logiciels listés par `Get-NetAdapter -IncludeHidden` ne constituent pas une carte réseau fournie par QEMU.
- [Après l'essai](resultats/reseau-apres.txt) : `netstat -ano` ne montre aucune connexion TCP établie ni socket attribuée aux PID de `Res.exe` ou d'`Env.exe`. Les ports en écoute et les sockets UDP des services Windows ne sont pas attribués au malware. Ce relevé est ponctuel ; `Env.exe` avait déjà quitté.
- La seconde trace complète contient **zéro événement de classe réseau**. Aucun échange SMTP ni transfert de données n'a été observé dans ces conditions.

L'US 3 a établi une capacité SMTP/TLS visant `smtp.laposte.net:465` dans le code d'`Env.exe`. Cette capacité statique ne constitue pas une connexion observée. L'erreur de démarrage et l'absence de réseau empêchent ici de valider ce comportement à l'exécution. L'absence de trafic dans cet essai ne prouve pas que le programme est dépourvu de fonctions réseau.

## Critères d'acceptation

| Critère | État | Justification |
|---|---|---|
| Modifications système observées | **Validé** | Valeurs Run et copies confirmées par les traces et la comparaison avant/après. |
| Création de fichiers / processus détectée | **Validé** | EXE, DLL, journal du premier essai et arbres de processus documentés. |
| Activités réseau identifiées | **Partiellement validé** | Absence d'activité observée dans les conditions isolées documentée ; fonctionnement SMTP non validé, car `Env.exe` échoue au démarrage. |

Le rendu documente donc l'analyse effectuée, avec **deux critères validés et une limite explicite sur le réseau**.

## Rejouer l'analyse des deux essais

Depuis la racine du projet :

```bash
bash us4/analyse.sh
```

Cette commande analyse les deux snapshots existants et vérifie les empreintes des PML avant de produire les résultats. La construction de l'image télécharge les bibliothèques si nécessaire ; le conteneur qui lit les preuves est sans réseau. Les scripts Windows sont apportés par le DVD créé avec `bash us4/dvd.sh`. Ils sont destinés exclusivement à la VM isolée, depuis un état propre et avec Process Monitor actif avant `tester.cmd`.

## Conservation

La VM est **arrêtée**, avec retour réussi à `windows-clean-us1`. La lecture du disque actif confirme l'absence de `C:\Lab`, de `C:\WindSyst` et des valeurs Run : [contrôle de restauration](resultats/restauration.json). `qemu-img check` ne signale aucune erreur. Les trois snapshots sont conservés.

Pour libérer de l'espace dans Docker, la capture mémoire antérieure a été transférée dans `infrastructure/windows/results/windows-before-malware.elf`. Sa taille et son SHA-256 ont été vérifiés avant retrait de la copie du volume. [Manifeste de déplacement](resultats/deplacement-memoire.json). Le fichier reste local et ignoré par Git.

Les dumps mémoire, le disque Windows, les exécutables et le contenu brut du journal ne sont pas inclus dans ce rendu.

Les relevés texte sont copiés sans transformation depuis NTFS ; leurs empreintes sont consignées dans [releves.json](resultats/releves.json). Certains utilisent l'encodage de la console Windows : une mauvaise détection UTF-8 peut déformer les accents à l'ouverture.
