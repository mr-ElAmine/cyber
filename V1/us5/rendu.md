# US 5 - Évaluation des risques

**Évaluation du 10 septembre 2026. Les trois critères de l'US 5 sont traités.**

Le risque principal est la **perte de confidentialité des saisies** sur un poste Windows exécutant `Res.exe`. Le risque est jugé **élevé si des informations sensibles y sont saisies**. Les modifications locales sont confirmées ; le vol effectif d'identifiants et l'envoi du journal vers l'extérieur ne le sont pas.

## 1. Périmètre et méthode

Objectif du backlog, page 11 : évaluer l'impact sur la machine afin de définir des mesures de mitigation adaptées. Cette étape exploite les preuves des US 2, 3 et 4. Elle ne nécessite pas de nouvelle exécution de l'échantillon.

Fichiers étudiés, identiques à ceux des essais précédents :

| Fichier | SHA-256 |
|---|---|
| `Res.exe` | `49f091ade48890bfa22d2b455494be95e52392c478b67e10626222b6aee37e1e` |
| `Env.exe` | `e09ec2098363a129de143fdaf73ad6e2e61266fba3f638a25214af3a8bc8f2f2` |

L'évaluation suppose que le programme a été exécuté sur le poste. Le mode d'infection initial, la fréquence des infections et la sensibilité réelle des données d'une organisation sont inconnus.

Nous utilisons une échelle qualitative propre à ce dossier : **faible** pour une conséquence limitée dans les observations disponibles ; **modéré** pour une altération locale nécessitant une remise en état ; **élevé** pour un scénario crédible pouvant exposer des données sensibles ou des comptes. Chaque niveau est accompagné de ses conditions et de l'état des preuves. Il ne s'agit ni d'un score CVSS, ni d'une probabilité calculée à partir des détections antivirus.

## 2. Preuves utilisées

| Référence | Constat vérifiable | Limite |
|---|---|---|
| E1 - [Analyse statique](../us3/rendu.md) | `Res.exe` interroge le clavier : appel à `GetAsyncKeyState` en `0x40167e`, puis logique d'écriture du journal. | Le code ne prouve pas que toutes les touches sont correctement capturées. |
| E2 - [Premier essai, CSV](../us4/resultats/evenements.csv) et [résumé](../us4/resultats/resume.json) | Neuf `WriteFile` réussis d'un octet dans `C:\WindSyst\log.txt`, événements 155195 à 210754, non consécutifs. Le journal final mesure 82 octets. | La phrase complète `LAB TEST 12345` n'est pas présente. Les neuf écritures et le fichier final correspondent à des instants différents. |
| E3 - [Deuxième essai, CSV](../us4/resultats/second-evenements.csv) et [résumé](../us4/resultats/second-resume.json) | Valeurs Run `Res` et `Env` écrites avec succès, événements 362327 et 362350 ; deux EXE et sept DLL copiés dans `C:\WindSyst`. | Le lancement automatique lors d'une nouvelle ouverture de session n'a pas été validé. |
| E4 - [Code d'Env](../us3/rendu.md) | Lecture du journal, préparation du message et appel à `connectToHostEncrypted` en `0x40243d`, pour `smtp.laposte.net:465`. | Ni authentification réussie ni réception d'un courriel démontrée. |
| E5 - [Erreur Qt](../us4/resultats/observation-env.json), [trace](../us4/resultats/second-resume.json) et [réseau](../us4/resultats/reseau-apres.txt) | `Env.exe` échoue au démarrage, plugin Qt « windows » manquant ; sortie avec le code 3, événement 432152. Zéro événement réseau dans la seconde trace. | Programme bloqué et VM sans réseau : aucune conclusion sur un envoi dans un autre environnement. |
| E6 - [Isolation](../us4/resultats/isolation.json) et [restauration](../us4/resultats/restauration.json) | QEMU sans carte réseau, Docker sans réseau ; état propre restauré après sauvegarde des traces. | La restauration de la VM n'est pas un audit de sécurité complet du Mac. |

Les deux traces complètes totalisent respectivement 218 035 et 472 737 événements. Leurs empreintes, leurs fenêtres temporelles et les conditions d'acquisition restent documentées dans le [rendu US 4](../us4/rendu.md). Les horloges du Mac et de Windows ne sont pas supposées synchronisées.

## 3. Impacts et niveaux de risque

La [matrice CSV](risques.csv) reprend les quatre scénarios avec leurs conditions, preuves et mesures associées.

| Risque | Impact sur la machine ou son utilisateur | Évaluation et justification |
|---|---|---|
| **R1 - Collecte des saisies** | Des textes confidentiels ou des identifiants saisis pourraient être enregistrés localement. Une récupération ultérieure du journal pourrait exposer des comptes. | **Élevé**, si des secrets sont saisis pendant l'exécution. Scénario plausible, soutenu par E1 et E2 ; confiance moyenne sur la qualité de la collecte. Aucun vol de mot de passe démontré. |
| **R2 - Installation et persistance** | La configuration de démarrage du compte est altérée et des exécutables sont installés. Un simple arrêt du processus peut laisser les moyens d'un prochain lancement. | **Modéré** pour l'altération locale constatée, qui peut prolonger R1. Installation confirmée, confiance élevée ; relancement automatique non testé, dépendances partiellement absentes (E3, E5). |
| **R3 - Envoi du journal par SMTP** | Des informations pourraient quitter le poste si le composant d'envoi fonctionnait et disposait d'un accès réseau. | **Élevé conditionnel** : gravité potentielle importante, réalisation indéterminée hors laboratoire. Dans les essais, l'envoi n'est pas observé et `Env.exe` échoue au démarrage (E4, E5). |
| **R4 - Perturbation du fonctionnement** | Les processus et copies ajoutent de l'activité ; `Env.exe` provoque une erreur applicative. | **Faible au vu des observations**, avec confiance limitée pour le long terme. Aucune interruption du système ni destruction de données établie. La lenteur de l'émulation QEMU n'est pas attribuée au malware. |

La **confidentialité** concentre donc l'impact potentiel majeur ; l'**intégrité** des fichiers et de la configuration utilisateur est effectivement altérée. Un impact majeur sur la **disponibilité** n'est pas démontré. Le niveau global élevé vient de R1 ; ce n'est pas une moyenne des lignes ni la preuve que R3 a réussi.

Aucune propagation autonome, élévation de privilèges, injection de processus ou fonction de rançongiciel n'a été établie dans le périmètre analysé. Ces capacités ne sont pas ajoutées au scénario sans preuve.

Pour situer les mécanismes : la collecte correspond à [MITRE ATT&CK T1056.001](https://attack.mitre.org/techniques/T1056/001/) et les valeurs Run à [T1547.001](https://attack.mitre.org/techniques/T1547/001/). MITRE décrit aussi SMTP comme un protocole possible d'exfiltration dans [T1048](https://attack.mitre.org/techniques/T1048/). Ce dernier rapprochement reste indicatif : aucun échange ni canal de commande distinct n'a été observé ici. Ces références ne constituent pas des preuves supplémentaires sur nos fichiers.

## 4. Mesures de mitigation

Les mesures suivantes concernent un **poste réellement suspecté d'infection**. Elles sont proposées, pas déclarées comme déployées sur une organisation.

| Priorité / mesure | Action concrète | Risque traité et contrôle attendu |
|---|---|---|
| **Immédiat - M1 : contenir** | Isoler le poste du réseau et interrompre les usages sensibles, notamment la saisie d'identifiants. | R1, R3. Vérifier que les communications non autorisées sont bloquées ; l'isolement réseau seul n'arrête pas la collecte locale. |
| **Avant remise en état - M2 : préserver** | Conserver les processus, traces, fichiers et valeurs Run utiles avec leurs empreintes. Préserver les éléments volatils avant arrêt, selon la procédure d'incident. | R1 à R4. Disposer de copies lisibles et identifiées avant quarantaine ou réinstallation. Les captures RAM existantes restent à examiner dans l'US 6. |
| **Après préservation - M3 : assainir** | Arrêter et mettre en quarantaine les fichiers identifiés ; supprimer seulement les valeurs Run attribuées à l'incident. Pour retrouver un état de confiance, restaurer une image saine connue ou réinstaller selon la procédure du poste. | R1, R2, R4. Contrôler l'absence des artefacts et de leur réapparition après ouverture de session, avec un antivirus à jour. Supprimer seulement `log.txt` est insuffisant. |
| **Si des secrets ont pu être saisis - M4 : protéger les comptes** | Depuis un appareil sain, changer les secrets potentiellement exposés, révoquer les sessions concernées lorsque le service le permet et examiner les connexions inhabituelles. Renforcer l'authentification multifacteur disponible. | R1, R3. Vérifier le remplacement des secrets et la révocation effective. L'authentification multifacteur ne retire pas le keylogger et ne protège pas tous les textes saisis. |
| **Avant reconnexion - M5 : détecter et limiter les sorties** | Corréler les empreintes des EXE avec les chemins `C:\WindSyst`, les valeurs Run et les processus auteurs. Limiter le SMTP sortant aux applications et relais approuvés, et journaliser les refus. | R2, R3. Valider les règles avec des tests bénins et examiner les alertes. `smtp.laposte.net` est un service légitime ; le domaine ou la clé Run seuls ne justifient pas un verdict malveillant. |
| **Prévention - M6 : limiter l'exécution** | Maintenir les protections et correctifs, encadrer l'exécution de logiciels non approuvés et réserver les privilèges élevés aux tâches nécessaires. | R1, R2. Vérifier les politiques applicatives et leur application. Un compte standard peut encore subir une collecte de ses saisies et une persistance HKCU. |

Microsoft documente l'[isolement d'un appareil, la collecte d'éléments d'investigation et les actions de réponse](https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts). Sa procédure de [récupération d'un compte compromis](https://support.microsoft.com/en-us/accounts-billing/manage/how-to-recover-a-hacked-or-compromised-microsoft-account) souligne l'assainissement du poste avant d'y changer le mot de passe. Les mesures ci-dessus sont adaptées à nos observations ; elles ne supposent pas que Defender for Endpoint est installé dans le laboratoire.

## 5. Situation du laboratoire et risque résiduel

La VM est restée arrêtée pendant cette US ; le contrôle Docker confirme une sortie propre avec le code 0 et `network_mode: none`. Le retour au snapshot propre et l'absence des artefacts dans le disque actif ont été vérifiés en US 4 (E6). Les deux états d'essai et leurs preuves sont conservés.

Ces mesures réduisent l'exposition du Mac et empêchent les sorties réseau de la VM dans la configuration testée. Elles ne rendent pas les échantillons inoffensifs : les archives et snapshots d'essai restent à traiter comme contenant du malware. La capture clavier pourrait toujours concerner les saisies effectuées dans une future session d'essai. L'analyse réseau incomplète ne justifie donc pas une reconnexion à Internet.

Le risque résiduel du laboratoire dépend du maintien de l'isolation, de l'usage de données de test et du retour à l'état propre. Il n'est pas extrapolé à un poste de production et aucune garantie d'absence de vulnérabilité de l'hyperviseur n'est formulée.

## 6. Validation de l'US 5

- [x] Description claire des impacts : confidentialité, intégrité et disponibilité, avec les limites des preuves.
- [x] Niveau de risque évalué : échelle qualitative, conditions d'exposition et justification de chaque scénario.
- [x] Recommandations de sécurité formulées : mesures M1 à M6, ordonnées et reliées aux risques.

L'US 5 est validée comme **évaluation argumentée des risques**. La limite réseau de l'US 4 reste inchangée ; les mesures proposées ne sont pas présentées comme toutes testées.

Pour la présentation : montrer une écriture Run, puis une écriture du journal ; expliquer le risque pour les saisies ; montrer l'erreur Qt pour distinguer l'exfiltration possible d'un envoi prouvé ; terminer par les mesures prioritaires.
