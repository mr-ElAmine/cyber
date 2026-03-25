# US 3 : Extraction de fichiers

## User Story

**EN TANT QUE** reverse-engineer
**JE VEUX** extraire `classes.dex` et `AndroidManifest.xml` de l'APK
**AFIN DE** préparer une décompilation

## Fichiers extraits

| Fichier | Type | Taille |
|---------|------|--------|
| `classes.dex` | Dalvik dex file version 035 | 7.1 MB |
| `AndroidManifest.xml` | Android binary XML | 14 KB |

## Hash SHA256

| Fichier | Hash SHA256 |
|---------|-------------|
| `classes.dex` | `57898c5978715da96560ed2692b4a8fa1a8e914b37988dcf369cc59951f6c429` |
| `AndroidManifest.xml` | `80b9b101e3bf02f03eec4f2c9c9ccf4d61403612e1435949b51cec8b85d7a276` |

## Commandes utilisées

```bash
# Extraction depuis l'APK (fichier ZIP)
unzip -j app.apk classes.dex AndroidManifest.xml -d us-3/

# Calcul des hash SHA256
shasum -a 256 us-3/classes.dex us-3/AndroidManifest.xml
```

## Notes

- Le fichier `AndroidManifest.xml` est au format **binaire Android** (pas lisible directement)
- Le fichier `classes.dex` contient le bytecode Dalvik compilé

---

## Definition of Done (DoD)

- [x] Fichier `classes.dex` extrait
- [x] Fichier `AndroidManifest.xml` extrait
- [x] Hash SHA256 calculés et documentés
