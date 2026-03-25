# US 5 : Analyse de strings.xml

## User Story

**EN TANT QUE** analyste sécurité
**JE VEUX** analyser strings.xml
**AFIN DE** repérer secrets ou informations critiques en clair

---

## Découvertes sensibles

### 1. Clé API Google (CRITIQUE)

| Champ | Valeur |
|-------|--------|
| **Nom** | `google_api_key` |
| **Valeur** | `AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg` |
| **Risque** | Clé API exposée, utilisable pour accéder aux services Google |

```
AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg
```

---

### 2. Configuration Firebase (HAUT)

| Champ | Valeur |
|-------|--------|
| `firebase_database_url` | `https://application-client-nickel.firebaseio.com` |
| `google_storage_bucket` | `application-client-nickel.appspot.com` |
| `project_id` | `application-client-nickel` |
| `google_app_id` | `1:717748501407:android:e0cdeb712e27275d` |

**Risque** : Base Firebase potentiellement accessible sans authentification (à vérifier dans US 9)

---

### 3. Endpoints API internes (MOYEN)

| Service | URL |
|---------|-----|
| Account API | `https://api.nickel.eu/customer-banking-api` |
| Auth API | `https://api.nickel.eu/customer-authentication-api` |
| Personal Space API | `https://api.nickel.eu/personal-space-api` |

**Risque** : Révélation de l'architecture backend

---

### 4. Identifiants de services tiers (MOYEN)

| Service | ID |
|---------|-----|
| **PushWoosh** | `DDF11-D1BF9` |
| **GCM Project** | `246766419677` |
| **GCM Sender** | `717748501407` |
| **Crashlytics Build ID** | `9ad6d741-4e10-4abd-9f12-163a0e3fb0b2` |

---

### 5. Informations diverses

| Champ | Valeur |
|-------|--------|
| `ENVIRONMENT` | `production` |
| `app_name` | `Nickel` |
| `build_config_package` | `com.fpe.comptenickel` |

---

## Résumé des risques

| Sévérité | Nombre | Type |
|----------|--------|------|
| **CRITIQUE** | 1 | Clé API Google |
| **HAUT** | 4 | Configuration Firebase |
| **MOYEN** | 7 | Endpoints + IDs tiers |

---

## Definition of Done (DoD)

- [x] Fichier strings.xml analysé
- [x] Secrets identifiés et documentés
- [x] Risques associés évalués
