# US 9 : Test de la base Firebase

## User Story

**EN TANT QUE** pentester
**JE VEUX** tester si la base Firebase est accessible publiquement
**AFIN DE** vérifier une fuite de données potentielle

---

## Identifiants Firebase extraits (US 5)

| Champ | Valeur |
|-------|--------|
| `google_api_key` | `AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg` |
| `firebase_database_url` | `https://application-client-nickel.firebaseio.com` |
| `google_storage_bucket` | `application-client-nickel.appspot.com` |
| `project_id` | `application-client-nickel` |
| `google_app_id` | `1:717748501407:android:e0cdeb712e27275d` |

---

## Commandes utilisées

```bash
# Test 1: Accès avec paramètre 'key' (clé API Google)
curl -s "https://application-client-nickel.firebaseio.com/.json?key=AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg"

# Test 2: Accès avec paramètre 'auth'
curl -s "https://application-client-nickel.firebaseio.com/.json?auth=AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg"

# Test 3: Accès sans authentification
curl -s "https://application-client-nickel.firebaseio.com/.json"

# Test 4: Endpoint utilisateurs
curl -s "https://application-client-nickel.firebaseio.com/users.json?key=AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg"

# Test 5: Tentative de création de compte anonyme
curl -s "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg" \
  -H "Content-Type: application/json" \
  -d '{"returnSecureToken":true}'

# Test 6: Accès au bucket Google Storage
curl -s "https://www.googleapis.com/storage/v1/b/application-client-nickel.appspot.com/o?key=AIzaSyBTgztvImsUfMWDa41PCrDWAj7dmyIDhUg"
```

---

## Résultats des tests

### 1. Firebase Realtime Database

| Test | Endpoint | Réponse | Code |
|------|----------|---------|------|
| Avec `key` | `/.json?key=API_KEY` | `{"error": "Permission denied"}` | 401 |
| Avec `auth` | `/.json?auth=API_KEY` | `{"error": "Permission denied"}` | 401 |
| Sans auth | `/.json` | `{"error": "Permission denied"}` | 401 |
| Users | `/users.json?key=API_KEY` | `{"error": "Permission denied"}` | 401 |

**Conclusion** : Base **non accessible** ✓

### 2. Firebase Authentication API

| Test | Réponse |
|------|---------|
| `signupNewUser` (anonyme) | `ADMIN_ONLY_OPERATION` - Création de compte non autorisée |
| `getAccountInfo` | `MISSING_ID_TOKEN` - Requiert un token valide |

**Conclusion** : Authentification **non bypassable** ✓

### 3. Google Cloud Storage

| Test | Réponse | Code |
|------|---------|------|
| List objects avec API key | `Anonymous caller does not have storage.objects.list access` | 401 |

**Conclusion** : Bucket **non accessible** ✓

---

## Analyse

### Risque évalué : **FAIBLE**

Bien que les identifiants Firebase soient exposés dans `strings.xml` :

- Les règles de sécurité Firebase sont **correctement configurées**
- La clé API Google ne permet pas d'accéder aux données sans authentification valide
- Le bucket Storage n'autorise pas l'accès anonyme
- La création de comptes anonymes est désactivée

### Ce qui a été testé

| Vecteur d'attaque | Résultat |
|-------------------|----------|
| Accès direct sans auth | Bloqué |
| Accès avec clé API | Bloqué |
| Création de compte anonyme | Bloqué |
| Accès Storage | Bloqué |

---

## Definition of Done (DoD)

- [x] Identifiants Firebase extraits de strings.xml
- [x] Tests avec clé API effectués
- [x] Tests sans authentification effectués
- [x] Résultats documentés
- [x] Risque évalué
