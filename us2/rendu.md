# US2 — Reconnaissance des fichiers

*Relevés du 10 septembre 2026, sans nouvelle consultation.*

J’ai calculé les empreintes **SHA-256, SHA-1 et MD5** du ZIP, de `Res.exe` et d’`Env.exe`, puis comparé leurs fiches sur VirusTotal et MalwareBazaar. Aucun exécutable n’a été lancé pour cette étape.

## Résultats

| Fichier | VirusTotal : détections | MalwareBazaar |
| --- | ---: | --- |
| `Res.exe` | **49 / 71** | Identifié dans le contenu du ZIP. |
| `Env.exe` | **29 / 70** | Identifié dans le contenu du ZIP. |
| `Malware.zip` | **45 / 65** | Fiche propre à l’archive. |

Les recherches directes des deux EXE sur MalwareBazaar donnaient zéro résultat, mais leurs empreintes correspondaient aux fichiers listés dans le ZIP.

Les détections orientent vers un **cheval de Troie / keylogger**, sans famille unique certaine. Les ratios viennent de rapports de dates différentes et ne mesurent pas la dangerosité.

**US2 validée : empreintes calculées, détections documentées et deux plateformes comparées.** Le lot était déjà référencé ; son comportement reste à confirmer par l’analyse.

## Commande utile

Depuis le projet, avec Docker, l’image de l’US1 et le volume d’échantillons disponibles :

```bash
# Calculer les empreintes, les enregistrer et les afficher.
bash us2/hash.sh
```

Le script remplace `hashes.json`. Les accès Docker sont définis dans [compose.yaml](compose.yaml) et le calcul dans [hashes.py](hashes.py).

[Empreintes](hashes.json) · [Relevé VirusTotal](virustotal.json) · [Relevé MalwareBazaar](malwarebazaar.json) · [Échantillons d’origine](https://github.com/Waelmeg/Malware/tree/056490ff588f3191a9edef6353d89c85398e7fca).
