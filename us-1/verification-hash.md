# US 1 : Téléchargement et vérification de l'APK

## User Story

**EN TANT QUE** testeur
**JE VEUX** recevoir l'APK vulnérable déjà fourni par le PO
**AFIN DE** travailler sur une base commune

## Vérification du hash SHA256

### Fichier analysé
- **Nom** : app.apk
- **Emplacement** : `/Users/aisaa/Documents/ecole/cyber/app.apk`

### Commande utilisée

```bash
shasum -a 256 app.apk
```

### Hash SHA256 calculé

```
f01f08c8b6e2fe4612e81bc7e3a3ba9440dad0d7a962f4e67640390dd721d528
```


### Résultat

| Fichier | Hash SHA256 |
|---------|-------------|
| app.apk | `f01f08c8b6e2fe4612e81bc7e3a3ba9440dad0d7a962f4e67640390dd721d528` |

---

## Definition of Done (DoD)

- [x] Hash SHA256 vérifié avec `shasum -a 256 app.apk`
- [x] Résultat documenté
