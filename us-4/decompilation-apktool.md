# US 4 : Décompilation avec Apktool

## User Story

**EN TANT QUE** auditeur
**JE VEUX** décompiler l'APK avec Apktool
**AFIN DE** accéder aux ressources et au manifest

## Commandes utilisées

```bash
# Installation d'Apktool via Homebrew
brew install apktool

# Décompilation de l'APK
apktool d app.apk -o us-4/app_src -f
```

## Structure du dossier `app_src/`

| Dossier/Fichier | Description |
|-----------------|-------------|
| `AndroidManifest.xml` | Manifest décodé (lisible en XML) |
| `apktool.yml` | Métadonnées Apktool |
| `assets/` | Fichiers assets de l'application |
| `lib/` | Bibliothèques natives (.so) |
| `original/` | Fichiers originaux non modifiés |
| `res/` | Ressources (layouts, strings, drawables, etc.) |
| `smali/` | Code Smali (bytecode Dalvik lisible) |
| `unknown/` | Fichiers non identifiés |

## Contenu principal

- **AndroidManifest.xml** : 15.8 KB (lisible)
- **Ressources** : 152 dossiers dans `res/`
- **Code Smali** : 13 dossiers de packages

---

## Definition of Done (DoD)

- [x] APK décompilé avec Apktool
- [x] Dossier `app_src/` livré
- [x] AndroidManifest.xml accessible en clair
- [x] Ressources accessibles
