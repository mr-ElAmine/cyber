# US 2 : Analyse automatisée avec MobSF

## User Story

**EN TANT QUE** analyste
**JE VEUX** scanner l'APK avec MobSF
**AFIN DE** identifier rapidement métadonnées et vulnérabilités

## Commandes utilisées

```bash
# Téléchargement de l'image Docker MobSF
docker pull opensecurity/mobile-security-framework-mobsf:latest

# Lancement du conteneur MobSF
docker run -d --name mobsf -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```

**Accès Web** : http://127.0.0.1:8000
**Identifiants** : `mobsf` / `mobsf`

---

## Informations de l'application

- **Package** : `com.fpe.comptenickel`
- **Min SDK** : 19 (Android 4.4-4.4.4)

## Résumé des vulnérabilités

| Sévérité | Nombre |
|----------|--------|
| **HIGH** | 2 |
| **WARNING** | 9 |
| **TOTAL** | 11 |

---

## Vulnérabilités HIGH (2)

### 1. Version Android vulnérable (minSdk=19)

| Critère | Valeur |
|---------|--------|
| **Sévérité** | HIGH |
| **Problème** | L'app peut être installée sur Android 4.4-4.4.4 (API 19) |
| **Risque** | Ces versions ont des vulnérabilités non corrigées |
| **Recommandation** | Supporter Android >= 10 (API 29) |

### 2. Cleartext Traffic activé

| Critère | Valeur |
|---------|--------|
| **Sévérité** | HIGH |
| **Problème** | `android:usesCleartextTraffic=true` |
| **Risque** | Le trafic HTTP non chiffré peut être intercepté/modifié (MITM) |
| **Recommandation** | Désactiver le cleartext traffic, utiliser HTTPS uniquement |

---

## Vulnérabilités WARNING (9)

### Composants exportés non protégés

| # | Type | Composant | Problème |
|---|------|-----------|----------|
| 3 | Broadcast Receiver | `RNDeviceReceiver` | `exported=true` sans protection |
| 4 | Broadcast Receiver | `PushAmazonReceiver` | Permission à vérifier |
| 5 | Broadcast Receiver | `BootReceiver` | Permission à vérifier |
| 6 | Service | `FcmRegistrationService` | Intent-filter exposé |
| 7 | Service | `PushFcmIntentService` | Intent-filter exposé |
| 8 | Content Provider | `PushwooshSharedDataProvider` | `exported=true` sans protection |
| 9 | Broadcast Receiver | `FirebaseInstanceIdReceiver` | Permission à vérifier |
| 10 | Broadcast Receiver | `AppMeasurementInstallReferrerReceiver` | Permission à vérifier |
| 11 | Service | `SystemJobService` | Permission à vérifier |

---

## Recommandations prioritaires

1. **Désactiver le cleartext traffic** → Forcer HTTPS
2. **Augmenter le minSdk** → API 29 minimum
3. **Protéger les composants exportés** → Ajouter des permissions ou définir `exported=false`

## Definition of Done (DoD)

- [x] APK scanné avec MobSF
- [x] Rapport CSV exporté
- [x] Résumé des vulnérabilités rédigé
