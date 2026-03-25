# US 8 : Signature de l'APK recompilé

## User Story

**EN TANT QUE** développeur
**JE VEUX** signer l'APK recompilé
**AFIN DE** pouvoir l'installer sur un appareil Android

---

## Commandes utilisées

```bash
# Génération d'un keystore de test
keytool -genkey -v \
  -keystore us-8/debug.keystore \
  -alias debug \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass android \
  -keypass android \
  -dname "CN=Debug, OU=Test, O=Test, L=Paris, ST=Paris, C=FR"

# Signature de l'APK
jarsigner -verbose \
  -keystore us-8/debug.keystore \
  -storepass android \
  -keypass android \
  us-7/rebuilt.apk debug

# Vérification de la signature
jarsigner -verify -verbose -certs us-8/signed.apk
```

---

## Fichiers générés

| Fichier | Description |
|---------|-------------|
| `debug.keystore` | Keystore de test (mot de passe: `android`) |
| `signed.apk` | APK recompilé et signé |

---

## Résultat

| Propriété | Valeur |
|-----------|--------|
| **Fichier** | `signed.apk` |
| **Taille** | 23 MB |
| **Hash SHA256** | `9322407486373590273ac014dffed3298f45f181de2d6143dcfa7f005c51e0a3` |
| **Algorithme** | SHA384withRSA |
| **Clé** | RSA 2048-bit |
| **Validité** | 10000 jours (expire en 2053) |

---

## Vérification

```
jar verified.

Warning: The signer certificate is self-signed.
```

> L'APK est correctement signé et peut être installé sur un appareil Android (après activation des sources inconnues).

---

## Comparaison des APK

| APK | Hash SHA256 |
|-----|-------------|
| Original (`app.apk`) | `f01f08c8...` |
| Recompilé (`rebuilt.apk`) | `afb2f055...` |
| Signé (`signed.apk`) | `93224074...` |

---

## Notes de sécurité

- Le keystore de test ne doit **jamais** être utilisé pour une application en production
- La signature originale de l'APK a été remplacée
- Un attaquant peut ainsi distribuer une version modifiée de l'application

---

## Definition of Done (DoD)

- [x] Keystore de test généré
- [x] APK signé avec jarsigner
- [x] Signature vérifiée
- [x] Fichiers livrés
