# US 2 - Vérification de la reconnaissance

**Date de consultation : 10 septembre 2026.**  
**État : US 2 validée ; empreintes calculées et comparaison VirusTotal / MalwareBazaar réalisée.**

## Objectif

En tant qu’analyste SOC, vérifier si le malware est déjà connu afin de distinguer un échantillon déjà référencé d’une menace qui ne l’est pas dans les bases consultées.

Critères du backlog : hash calculé, résultats de détection documentés, comparaison avec des bases existantes.

## 1. Identifier exactement les fichiers

Source : [dépôt pédagogique, commit figé](https://github.com/Waelmeg/Malware/tree/056490ff588f3191a9edef6353d89c85398e7fca).

L’archive originale est conservée dans le volume Docker `cyber-malware-samples`. Le script [hashes.py](hashes.py) lit le ZIP et les deux exécutables qu’il contient. Il calcule leurs SHA-256, SHA-1 et MD5 sans extraire ni exécuter les programmes.

Le SHA-256 est l’identifiant principal de la recherche. Les autres empreintes permettent de recouper les fiches des plateformes. Une empreinte ne constitue pas, à elle seule, un verdict antivirus.

| Fichier | Taille en octets | SHA-256 |
| --- | ---: | --- |
| Malware.zip | 9156591 | `a1af8eeaa7fda7ced591a72c572a12c2298ddb763defaa36ce5b17be1411c2be` |
| VIRUS/Env.exe | 53248 | `e09ec2098363a129de143fdaf73ad6e2e61266fba3f638a25214af3a8bc8f2f2` |
| VIRUS/Res.exe | 25088 | `49f091ade48890bfa22d2b455494be95e52392c478b67e10626222b6aee37e1e` |

Les valeurs complètes et la date de calcul figurent dans [hashes.json](hashes.json). Les tailles ainsi que les trois empreintes correspondent aux informations affichées dans les fiches VirusTotal.

## 2. Rapports de détection existants

Les rapports ont été consultés par empreinte, dans le navigateur du Mac. Aucun fichier n’a été envoyé et aucune réanalyse n’a été demandée. La VM Windows est restée arrêtée.

| Fichier | Détections affichées | Première soumission sur VirusTotal (UTC) | Date de l’analyse affichée (UTC) |
| --- | ---: | --- | --- |
| [Res.exe](https://www.virustotal.com/gui/file/49f091ade48890bfa22d2b455494be95e52392c478b67e10626222b6aee37e1e) | 49/71 | 2020-08-10 18:23:39 | 2026-01-22 21:10:26 |
| [Env.exe](https://www.virustotal.com/gui/file/e09ec2098363a129de143fdaf73ad6e2e61266fba3f638a25214af3a8bc8f2f2) | 29/70 | 2021-03-28 17:12:53 | 2026-09-09 13:08:43 |
| [Malware.zip](https://www.virustotal.com/gui/file/a1af8eeaa7fda7ced591a72c572a12c2298ddb763defaa36ce5b17be1411c2be) | 45/65 | 2022-10-13 07:43:41 | 2026-09-09 11:12:18 |

**Les fichiers exacts sont déjà référencés dans VirusTotal.** La première soumission de `Res.exe` remonte à 2020, celle d’`Env.exe` à 2021 et celle du ZIP à 2022.

Les ratios proviennent de rapports établis à des dates différentes. Ils ne sont ni des probabilités de malveillance ni une mesure permettant de comparer la dangerosité des fichiers. La première soumission indique une présence dans cette base, pas une date de création ou de première infection.

## 3. Comparaison des moteurs

Exemples relevés dans les rapports existants :

| Moteur | Res.exe | Env.exe |
| --- | --- | --- |
| Microsoft | `Trojan:Win32/Phonzy.A!ml` | `Trojan:Win32/Malgent!MSR` |
| ESET-NOD32 | `Win32/Spy.KeyLogger.RHK Trojan` | `Win32/Spy.KeyLogger.RHK Trojan` |
| DrWeb | `Trojan.KeyLogger.43162` | `Trojan.KeyLogger.44789` |

Les moteurs ci-dessus signalent les deux fichiers. Les libellés convergent vers des catégories de cheval de Troie et de logiciel espion, avec plusieurs mentions de keylogger, mais ne donnent pas une attribution de famille unique et certaine.

Ces observations proviennent de plusieurs moteurs regroupés par VirusTotal. La comparaison avec une deuxième plateforme figure dans la section suivante. Le relevé daté, ses liens et la méthode sont conservés dans [virustotal.json](virustotal.json) ; ce fichier est une transcription des champs consultés, pas une réponse API.

## 4. Deuxième plateforme : MalwareBazaar

Après validation manuelle du CAPTCHA, les trois SHA-256 ont été recherchés avec la syntaxe `sha256:<empreinte>`.

| Fichier | VirusTotal | MalwareBazaar, consultation du 10/09/2026 |
| --- | --- | --- |
| Res.exe | Fiche propre ; 49/71 détections | Zéro fiche en recherche directe ; identifié dans le contenu du ZIP |
| Env.exe | Fiche propre ; 29/70 détections | Zéro fiche en recherche directe ; identifié dans le contenu du ZIP |
| Malware.zip | Fiche propre ; 45/65 détections | Une fiche propre, présente depuis le 11/02/2025 à 08:53:34 UTC |

La [fiche MalwareBazaar du ZIP](https://bazaar.abuse.ch/sample/a1af8eeaa7fda7ced591a72c572a12c2298ddb763defaa36ce5b17be1411c2be/) confirme son identité et liste les deux exécutables avec les mêmes SHA-256, MD5 et tailles que nos fichiers.

Sa classification principale indique `Threat unknown`. Les avis associés divergent : Hatching Triage indique `Malicious`, ReversingLabs `Win32.Trojan.Malgent` et Nucleon Malprob `Benign`. Aucun nom de famille unique n’est retenu.

**Le ZIP est connu des deux plateformes et ses exécutables sont référencés individuellement sur VirusTotal et comme contenus d’archive sur MalwareBazaar.** Zéro résultat en recherche directe ne signifie donc pas « fichier inconnu ». La date de présence dans une base ne prouve pas une date d’infection. Le relevé et les liens des recherches sont conservés dans [malwarebazaar.json](malwarebazaar.json).

## 5. Refaire le calcul

Depuis la racine du projet, avec Docker Desktop lancé et l’infrastructure de l’US 1 déjà construite :

```bash
bash us2/hash.sh
```

Le script affiche les résultats et actualise `us2/hashes.json`. Il utilise un conteneur temporaire sans réseau, avec l’archive et le script montés en lecture seule. L’image locale de la console fournit déjà Python ; Windows n’est pas lancé.

Pour la démonstration : lancer cette commande, ouvrir une fiche VirusTotal par SHA-256 et montrer son ratio et sa date. Comparer les noms de détection, puis ouvrir la fiche MalwareBazaar du ZIP et déplier « Potential files of interest » pour retrouver les deux exécutables.

## 6. Avancement

- [x] Empreintes calculées dans Docker et enregistrées.
- [x] Résultats de détection existants documentés et datés.
- [x] Libellés de plusieurs moteurs comparés via VirusTotal.
- [x] Comparaison avec une deuxième plateforme : fiche du ZIP et contenu vérifiés sur MalwareBazaar.

Les trois critères de l’US 2 sont remplis : empreintes calculées, résultats documentés et comparaison avec des bases existantes. Ces échantillons sont déjà référencés ; nous ne les présentons pas comme une menace nouvelle. L’analyse du code et la confirmation des comportements restent du ressort des US 3 et 4.
