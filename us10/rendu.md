# US10 — Chronologie de l’utilisation USB

J’ai relevé les dates de la **SanDisk Cruzer Blade `4C530000281008116284`**, identifiée en US9, dans les mêmes fichiers du registre.

## Résultat

**3 février 2020 — heures UTC, affichées à la seconde.**

| Heure | Trace retrouvée |
| --- | --- |
| **12:12:31** | Première installation du périphérique USB. |
| **12:12:32** | Première installation de son disque dans USBSTOR. |
| **12:44:21** | Dernière connexion enregistrée, corroborée par la modification du volume dans `MountPoints2`. |
| **12:45:00** | Dernier retrait enregistré, identique dans USB et USBSTOR. |

La dernière connexion documentée dure **environ 39 secondes**. Les propriétés `0065`, `0066` et `0067` donnent respectivement la première installation, la dernière arrivée et le dernier retrait. `0064` date la dernière installation ; je ne l’utilise pas comme une connexion supplémentaire. La correspondance vient du [fichier Microsoft devpkey.h](https://github.com/tpn/winsdk-10/blob/master/Include/10.0.16299.0/shared/devpkey.h).

**Critères US10 atteints : horodatages extraits et chronologie établie.** Une fuite reste **non démontrée** : aucune date supposée de fuite ni preuve de copie n’est fournie. Le registre conserve des premières/dernières dates, pas chaque connexion.

Les fichiers présentent une écriture inachevée, sans journaux de récupération. Leurs horloges ne sont pas vérifiées. Ces événements de 2020 ne sont pas ceux du laboratoire de 2026.

## Relancer

Après l’US9 :

```bash
bash us10/analyse.sh
```

Le script relit l’archive hors réseau, vérifie l’identification, puis trie les dates en UTC. [Les 9 traces détaillées](resultats/chronologie.csv) conservent les chemins et valeurs brutes ; [le bilan](resultats/bilan.json) précise les limites.
