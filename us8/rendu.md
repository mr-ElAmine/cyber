# US8 — Analyse croisée RAM / disque

*Résultats du 10 septembre 2026.*

J’ai croisé les relevés **Process Monitor de l’US4**, la **RAM de l’US6** et le **disque de l’US7** pour reconstituer le premier essai.

## Résultats

| Élément | Constat |
| --- | --- |
| `Res.exe` | PID **6064**, parent PowerShell **5236**. Le chemin en RAM correspond au fichier lancé depuis `C:\Lab\sample\virus`. |
| Copies | `Res.exe` et `Env.exe` retrouvés dans `C:\WindSyst`, identiques aux originaux. Les copies sont attribuées à des descendants de `Res.exe`. |
| Persistance | Valeurs **Run\Res** et **Run\Env** absentes du registre propre, présentes après l’essai ; écritures attribuées à `Res.exe`. |
| Journal | **9 écritures** observées dans `log.txt` ; fichier de **82 octets** dans le snapshot ultérieur. |
| `Env.exe` | Présent sur disque et dans les valeurs Run, absent des résultats mémoire examinés. |

Le scénario rassemble **14 événements** : lancement depuis PowerShell, copies vers `WindSyst`, configuration du démarrage automatique, puis écritures du journal.

**US8 validée : correspondance RAM/disque établie et persistance détectée.** Le lancement automatique à la prochaine connexion n’a pas été testé. Le code en RAM n’a pas été comparé par empreinte au fichier disque. Aucun envoi SMTP réussi n’est démontré. RAM et disque correspondent à deux instants différents du même essai.

## Commande utile

Depuis le projet, avec Docker lancé, la VM arrêtée et les preuves précédentes conservées :

```bash
bash us8/analyse.sh
```

Le script vérifie l’image, relit fichiers et registre, puis croise les relevés. Il utilise un conteneur hors réseau, garde les sources en lecture seule et remplace les résultats de l’US8.

Le déroulement se lit dans [script/analyser.py](script/analyser.py). Chaque étape appelle un fichier dédié.

[Corrélations](resultats/correlations.json) · [Persistance](resultats/persistance.json) · [Chronologie](resultats/evenements.csv) · [Provenance](resultats/provenance.json).
