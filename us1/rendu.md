# US1 — Mon environnement d’analyse sécurisé

*Support de présentation à la première personne, à partir des observations du 10 septembre 2026. Cette réécriture ne correspond pas à une nouvelle séance de test.*

## Pourquoi j’ai commencé par l’isolation

Avant d’étudier le malware, j’avais besoin d’un endroit où le lancer sans travailler directement sur mon ordinateur. Le but de cette première story était donc de préparer le laboratoire : un Windows séparé de mon système principal, sans accès réseau non contrôlé.

Je voulais aussi pouvoir revenir à un état propre après un essai. Sinon, les modifications laissées par le programme auraient pu fausser les observations de la séance suivante.

## Comment mon laboratoire fonctionne

Mon ordinateur est un Mac avec un processeur ARM64, alors que j’ai installé un Windows x64. J’ai utilisé QEMU pour émuler le PC sur lequel Windows s’exécute. Docker me sert à regrouper les outils et à définir leurs accès.

```mermaid
flowchart LR
    M["Mon Mac ARM64"] -->|héberge| D["Docker Desktop"]
    D -->|lance le conteneur vm| Q["QEMU : PC x64 émulé"]
    Q -->|exécute| W["Windows 10"]
```

Windows dispose de **2 processeurs virtuels, 4 Gio de RAM et un disque virtuel de 64 Gio**. Le fichier du disque est au format QCOW2, qui permet notamment de conserver des snapshots, c’est-à-dire des états du disque auxquels je peux revenir.

J’ai séparé le lancement de Windows et son affichage dans deux services définis dans [compose.yaml](../infrastructure/windows/compose.yaml) :

- **`vm`** lance QEMU et utilise le disque Windows.
- **`console`** me permet de voir le bureau Windows et de le contrôler depuis mon navigateur, avec noVNC.

Pour accéder à Windows, j’ouvre [la console locale](http://127.0.0.1:6085/vnc.html). La console échange avec QEMU par un socket Unix, un canal local pour l’affichage et les entrées clavier/souris. Windows n’a pas besoin d’une carte réseau pour cela.

## Comment j’ai limité les accès

J’ai coupé le réseau à deux endroits. Dans la commande QEMU, j’ai mis :

```text
-nic none
```

Cette option retire la carte réseau virtuelle de Windows. Dans le service Docker `vm`, j’ai également mis :

```yaml
network_mode: none
```

Le conteneur qui héberge QEMU n’a donc pas non plus d’interface réseau externe. La console possède un réseau d’administration séparé, auquel le service `vm` n’est pas connecté.

L’accès à cette console est publié ainsi :

```yaml
ports:
  - "127.0.0.1:6085:6080"
```

Cela signifie que le port **6085 de mon Mac** donne accès au port **6080 du conteneur console**. L’adresse `127.0.0.1` limite cette publication à mon ordinateur.

J’ai aussi limité les permissions des conteneurs : ils utilisent un compte non root, leur système de fichiers principal est en lecture seule et leurs capacités Linux supplémentaires sont retirées. Le disque Windows reste inscriptible, puisque je veux pouvoir observer les fichiers et paramètres modifiés pendant les essais.

Pour apporter des fichiers à Windows, j’utilise un DVD virtuel en lecture seule. Je ne partage pas de dossier du Mac directement avec Windows et je ne lui transmets aucun périphérique USB physique. Le périphérique `usb-tablet` de QEMU est simplement une souris virtuelle, utile pour la console.

## Comment j’ai vérifié que le réseau était coupé

Je ne me suis pas arrêté à la configuration. Dans Windows, j’ai utilisé ces trois commandes :

```powershell
ipconfig /all
route print
ping 1.1.1.1
```

`ipconfig /all` me montre les interfaces réseau. Lors de la séance, je n’ai trouvé aucun adaptateur externe utilisable. `route print` me montre les chemins que Windows peut emprunter pour communiquer : je n’ai trouvé aucune route par défaut, seulement la boucle locale.

Avec `ping 1.1.1.1`, j’ai essayé de joindre une adresse extérieure. La commande a échoué avec le message « défaillance générale ». Cet échec complète les autres contrôles : à lui seul, un ping qui échoue ne suffirait pas à prouver l’isolation.

Du côté du Mac, cette commande permet de lire le mode réseau et le niveau de privilège réellement appliqués au conteneur :

```bash
docker inspect cyber-windows-vm-1 --format \
  '{{.HostConfig.NetworkMode}} {{.HostConfig.Privileged}}'
```

Le résultat relevé était **`none false`** : réseau désactivé et conteneur non privilégié. Pour vérifier l’adresse de publication de la console, j’ai utilisé :

```bash
docker port cyber-windows-console-1
```

Le port était bien lié à **`127.0.0.1:6085`**. Un essai de connexion TCP depuis un conteneur temporaire du même service vers `1.1.1.1:443` a également échoué avec `Network is unreachable`.

Les sorties Docker du 10 septembre sont conservées dans [preuves.txt](preuves.txt). Les observations faites dans Windows sont celles de la séance ; ce fichier ne contient pas une nouvelle capture de ces commandes Windows.

## Comment je reviens à un état propre

Avant d’introduire le malware, j’ai créé un snapshot nommé **`windows-clean-us1`**. Il me sert de point de retour.

J’ai testé la restauration sur une copie du disque : j’ai introduit une modification, constaté que la copie différait de la référence, puis appliqué le snapshot. La comparaison a confirmé le retour au contenu initial.

Après le premier essai, j’ai conservé le disque modifié dans `malware-first-run`, puis restauré l’état propre. Le relevé du 10 septembre indique que la VM était ensuite arrêtée correctement, avec un code de sortie `0`. C’est l’état constaté à cette date, pas un contrôle effectué pendant cette réécriture.

## Ce que je peux conclure pour l’US1

Les deux critères sont remplis **pour le laboratoire hors réseau testé** :

- J’ai un Windows isolé, avec son propre disque et des accès limités.
- Les contrôles Windows et Docker confirment l’absence de sortie réseau dans cette configuration.

Cela me donne une base pour observer les changements locaux du malware. En revanche, je ne peux pas y observer un échange abouti avec un serveur distant. Ce sera une limite à garder en tête quand je présenterai l’analyse réseau.

L’isolation ne constitue pas une garantie absolue contre une évasion de VM ; je n’ai pas testé ce type d’attaque. L’émulation peut aussi ralentir Windows. Enfin, j’ai utilisé **Windows 10 Enterprise LTSC Evaluation x64 en français** : l’évaluation affichait une expiration, et l’activation n’a pas été validée. Cette story couvre Windows ; l’environnement Linux envisagé au départ reste à réaliser.

---

## Mes repères pour montrer le code

Les fichiers de l’US1 sont dans [infrastructure/windows](../infrastructure/windows/). Chaque fichier a un rôle précis :

| Fichier | Ce que j’explique en le montrant |
| --- | --- |
| [compose.yaml](../infrastructure/windows/compose.yaml) | Je définis les deux services, le disque, la mémoire et les restrictions d’accès. |
| [Dockerfile](../infrastructure/windows/Dockerfile) | Je prépare une image avec QEMU et une autre avec la console noVNC. |
| [download_windows.py](../infrastructure/windows/download_windows.py) | Je télécharge l’ISO Microsoft dans `media/windows.iso`, avec un pourcentage de progression. |
| [install.sh](../infrastructure/windows/install.sh) | Je télécharge l’ISO, construis les images, crée le disque et démarre l’installation. **Ce script recrée le disque : il est réservé à la première installation.** |
| [start.sh](../infrastructure/windows/start.sh) | Je démarre le Windows déjà installé et sa console. |

### Démarrer une installation existante

Depuis la racine du projet, avec Docker Desktop lancé :

```bash
bash infrastructure/windows/start.sh
```

Le script se place dans son propre dossier avec `cd "$(dirname "$0")"`. Docker y retrouve ainsi `compose.yaml`, quel que soit le dossier depuis lequel je lance le script. Puis `docker compose up -d` démarre les services en arrière-plan : je peux continuer à utiliser le terminal.

`set -e` arrête le script si une commande échoue. Je garde ces scripts courts : ils enchaînent les commandes nécessaires, sans arguments à renseigner.

### Montrer le snapshot après l’arrêt de Windows

Dans Windows, je peux demander un arrêt normal avec :

```powershell
shutdown /s /t 0
```

`/s` demande l’arrêt et `/t 0` supprime le délai d’attente. Ensuite, depuis le Mac :

```bash
docker wait cyber-windows-vm-1
docker compose -f infrastructure/windows/compose.yaml \
  run --rm --no-deps vm \
  qemu-img snapshot -l /storage/windows.qcow2
```

La première commande attend la fin du conteneur et affiche son code de sortie. La suivante liste les snapshots du disque : `-l` signifie ici « lister ». Je dois y retrouver `windows-clean-us1`.

Dans cette commande, `run` lance un conteneur temporaire avec l’outil `qemu-img` à la place de Windows. `--no-deps` évite de démarrer les autres services et `--rm` supprime ce conteneur à la fin. Je fais cette lecture après l’arrêt complet de la VM ; lister les snapshots ne restaure pas le disque.

## Documents sur lesquels je m’appuie

- [Preuves Docker de la séance](preuves.txt) et [version initiale du rendu](../V1/us1/rendu.md), conservées pour retrouver les observations d’origine.
- Backlog fourni, `Backlog - Reverse engineering.pdf`, US1 page 7.
- [Options de lancement de QEMU](https://www.qemu.org/docs/master/system/invocation.html), [réseau Docker « none »](https://docs.docker.com/engine/network/drivers/none/) et [publication des ports Docker](https://docs.docker.com/engine/network/port-publishing/), références déjà utilisées dans le rendu initial.
