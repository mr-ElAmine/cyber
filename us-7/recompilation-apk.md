# US 7 : Recompilation de l'APK

## User Story

**EN TANT QUE** développeur
**JE VEUX** recompiler l'APK avec Apktool
**AFIN DE** vérifier que la décompilation est réversible

---

## Recompilation effectuée

```bash
apktool b us-4/app_src -o us-7/rebuilt.apk
```

## Log de build

```
I: Using Apktool 3.0.1 on app.apk with 8 threads
I: Smaling smali folder into classes.dex...
I: Building resources with aapt2...
I: Building apk file...
I: Importing assets...
I: Importing lib...
I: Importing unknown files...
I: Built apk into: us-7/rebuilt.apk
```

---

## Résultat

| Propriété | Valeur |
|-----------|--------|
| **Fichier** | `rebuilt.apk` |
| **Taille** | 23 MB |
| **Hash SHA256** | `afb2f055b71b3e33e83db5df1afe5a69082dd06fe789070139d78169f0662354` |

---

## Comparaison avec l'APK original

| APK | Taille | Hash SHA256 |
|-----|--------|-------------|
| Original (`app.apk`) | 23 MB | `f01f08c8b6e2fe4612e81bc7e3a3ba9440dad0d7a962f4e67640390dd721d528` |
| Recompilé (`rebuilt.apk`) | 23 MB | `afb2f055b71b3e33e83db5df1afe5a69082dd06fe789070139d78169f0662354` |

> Les hash sont différents car Apktool reconstruit l'APK avec une nouvelle signature et compression.

---

## Conclusion

La décompilation est **réversible**. L'APK a été recompilé avec succès.

Cela signifie qu'un attaquant peut :
- Modifier le code Smali
- Recompiler l'APK
- Le resigner et le distribuer

---

## Fichiers livrés

- `rebuilt.apk` - APK recompilé
- `build.log` - Log de compilation

---

## Definition of Done (DoD)

- [x] APK recompilé avec Apktool
- [x] Fichier livré
- [x] Log de build documenté
