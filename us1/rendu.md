# US1 — Environnement sécurisé

*Résultats du 10 septembre 2026.*

J’ai installé Windows 10 x64 dans QEMU, lancé avec Docker sur mon Mac ARM64 : **2 processeurs virtuels, 4 Gio de RAM et un disque de 64 Gio**.

## Résultats

| Contrôle | Résultat |
| --- | --- |
| Isolation réseau | Carte réseau Windows désactivée (`-nic none`) et conteneur sans réseau (`network_mode: none`). |
| Vérifications Windows | Aucun adaptateur externe utilisable, aucune route par défaut et échec du ping extérieur. |
| Sortie réseau du conteneur | Connexion vers `1.1.1.1:443` impossible : `Network is unreachable`. |
| Accès au laboratoire | Console sur `127.0.0.1:6085`, sans dossier partagé avec Windows ni USB physique transmis. |
| Retour à l’état propre | Snapshot `windows-clean-us1` créé avant le malware ; restauration testée sur une copie. |

**US1 validée pour une utilisation hors réseau.** Le disque a été restauré à l’état propre après l’essai.

Limites : aucun échange avec un serveur distant ni test d’évasion de VM. La licence Windows d’évaluation affichait une expiration ; l’activation n’est pas validée.

## Commandes utiles

Depuis le projet, avec Docker lancé :

```bash
# Démarrer le Windows déjà installé.
bash infrastructure/windows/start.sh
```

Ouvrir [la console Windows](http://127.0.0.1:6085/vnc.html), puis vérifier le réseau dans Windows :

```powershell
# Afficher les interfaces réseau.
ipconfig /all

# Afficher les routes disponibles.
route print

# Tester une sortie vers Internet : échec attendu.
ping 1.1.1.1
```

[Configuration Docker](../infrastructure/windows/compose.yaml) · [Preuves Docker](preuves.txt).
