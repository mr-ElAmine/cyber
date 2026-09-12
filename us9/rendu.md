# US9 — Identification de la clé USB

J’ai examiné les fichiers du registre fournis dans [Dump_memoire](https://github.com/Waelmeg/Dump_memoire/tree/c2741e9bfed329c780a07f230b4ce548ee3806a7). Cette source est distincte de la VM utilisée pour les US1 à US8.

## Résultat

| Élément | Valeur retrouvée |
| --- | --- |
| Clé | **SanDisk Cruzer Blade** |
| Numéro de série | **`4C530000281008116284`** |
| Instance disque dans USBSTOR | `4C530000281008116284&0` |
| Identifiant USB | `VID_0781&PID_5567` |
| Volume associé | **New Volume**, lecteur **E:** |

Le numéro apparaît dans `SYSTEM\ControlSet001\Enum\USB`. Le lien parent et le même `ContainerID` le rattachent à l’entrée `USBSTOR`. `MountedDevices` associe cette entrée au lecteur E:, et le même volume apparaît dans `NTUSER.DAT\…\MountPoints2`.

**Critère US9 atteint : le numéro de série est extrait et recoupé.** Ces traces ne permettent pas d’identifier le propriétaire de la clé ni de prouver une copie de fichiers.

Les trois fichiers du registre présentent une écriture inachevée. Aucun journal de récupération n’est fourni : les résultats portent sur les valeurs encore lisibles, sans reconstitution des dernières écritures.

## Relancer

Depuis le projet, avec Docker lancé :

```bash
# Récupérer l’archive publique.
bash us9/telecharger.sh

# Identifier la clé dans un conteneur hors réseau.
bash us9/analyse.sh
```

L’analyse vérifie le SHA-256 de l’archive, la lit sans la modifier et remplace `resultats/`. Le code est découpé dans [script/](script/).

[Identification et chemins exacts](resultats/usb.json) · [Source et empreintes](resultats/provenance.json).
