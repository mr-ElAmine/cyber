# US 6 : Analyse statique du code decompile

## User Story

**EN TANT QUE** ingenieur securite  
**JE VEUX** analyser le bytecode decompile (Smali)  
**AFIN DE** identifier des vulnerabilites logiques, des composants exposes et des mauvaises pratiques de securite

---

## Perimetre analyse

Les verifications ont ete faites dans les sources decompilees presentes dans `us-4/app_src/` :

- `AndroidManifest.xml`
- `apktool.yml`
- `smali/com/fpe/comptenickel/BuildConfig.smali`
- `smali/com/fpe/comptenickel/RSA.smali`
- `smali/com/fpe/comptenickel/MainApplication$1.smali`
- `smali/com/RNFetchBlob/*`
- `smali/com/pushwoosh/PushwooshSharedDataProvider.smali`
- `smali/com/learnium/RNDeviceInfo/RNDeviceReceiver.smali`
- `assets/index.android.bundle`

Approche :

1. verification manuelle des composants declares dans le manifest ;
2. lecture du Smali pour confirmer l'impact reel ;
3. reclassification des points faibles en separant les vrais risques, les risques conditionnels et les simples indicateurs de surface d'attaque.

---

## Synthese executive

| Severite | Nombre | Resume |
|----------|--------|--------|
| **HAUT** | 2 | Bug logique RSA sur Android 4.4-5.1, cleartext traffic globalement autorise |
| **MOYEN** | 3 | Provider exporte exposant un identifiant, receiver spoofable, bypass TLS dormant via RNFetchBlob |
| **FAIBLE** | 1 | Activite DevSettings laissee dans le manifest |
| **INFO** | 2 | Endpoints hardcodes, points positifs sur l'usage du keystore |

---

## Findings detailles

### 1. Bug logique RSA sur Android 4.4 a 5.1 (HAUT)

**Fichiers**

- `apktool.yml` : min SDK 19
- `RSA.smali` : `generateKeys()` et `sign()`

**Preuves**

Le binaire supporte Android 4.4+ :

```yml
minSdkVersion: 19
```

Dans `generateKeys()`, l'alias complet `keyTag + "_" + suffixe` est prepare, puis ignore dans la branche API < 23 au profit de `keyTag` seul :

```smali
invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
...
iget-object v7, p0, Lcom/fpe/comptenickel/RSA;->keyTag:Ljava/lang/String;
invoke-virtual {v6, v7}, Landroid/security/KeyPairGeneratorSpec$Builder;->setAlias(Ljava/lang/String;)Landroid/security/KeyPairGeneratorSpec$Builder;
```

Mais `sign()` reconstruit bien l'alias complet avant l'appel a `getPrivateKey()` :

```smali
iget-object v1, p0, Lcom/fpe/comptenickel/RSA;->keyTag:Ljava/lang/String;
invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
...
invoke-direct {p0, p2}, Lcom/fpe/comptenickel/RSA;->getPrivateKey(Ljava/lang/String;)Ljava/security/PrivateKey;
```

**Constat**

Sur les appareils API 19 a 22, la cle est generee sous un alias et relue sous un autre. Cette branche est atteignable car `minSdkVersion` vaut 19.

**Impact**

- echec probable de signature sur Android 4.4 a 5.1 ;
- indisponibilite potentielle d'un parcours d'authentification ou d'enrolement ;
- creation de cles orphelines dans le keystore.

**Recommendation**

Utiliser le meme alias dans toutes les branches (`generateKeys`, `sign`, lecture de cle privee), puis tester explicitement sur API 19-22 si ce support doit etre conserve.

---

### 2. Cleartext traffic active globalement (HAUT)

**Fichier** : `AndroidManifest.xml` ligne 36

```xml
<application ... android:usesCleartextTraffic="true">
```

**Constat**

L'application autorise globalement le trafic HTTP non chiffre et aucun `networkSecurityConfig` n'a ete retrouve dans les sources decompilees.

**Impact**

- interception/modification de trafic si un flux HTTP existe encore ;
- exposition accrue en cas de redirection ou de mauvaise configuration serveur ;
- attenuation des garanties TLS sur un perimetre qui devrait etre force en HTTPS.

**Recommendation**

Passer `usesCleartextTraffic` a `false` et declarer une politique reseau explicite avec `networkSecurityConfig` si une exception precise est reellement necessaire.

---

### 3. Content Provider exporte exposant un identifiant device Pushwoosh (MOYEN)

**Fichiers**

- `AndroidManifest.xml` ligne 97
- `PushwooshSharedDataProvider.smali`
- `com/pushwoosh/internal/platform/utils/a.smali`

**Preuves**

Le provider est exporte :

```xml
<provider android:authorities="com.fpe.comptenickel.PushwooshSharedDataProvider" android:enabled="true" android:exported="true" ... />
```

URI attendue :

```text
content://com.fpe.comptenickel.PushwooshSharedDataProvider/hwid
```

Il repond sur la route `hwid` :

```smali
const-string v0, "hwid"
invoke-virtual {p2, p4, v0, v1}, Landroid/content/UriMatcher;->addURI(Ljava/lang/String;Ljava/lang/String;I)V
```

Et peut renvoyer un identifiant device stocke par Pushwoosh :

```smali
invoke-virtual {v0}, Lcom/pushwoosh/repository/RegistrationPrefs;->deviceId()Lcom/pushwoosh/internal/preference/PreferenceStringValue;
invoke-virtual {v0}, Lcom/pushwoosh/internal/preference/PreferenceStringValue;->get()Ljava/lang/String;
```

**Constat**

N'importe quelle application locale capable d'interroger ce provider peut tenter d'obtenir un identifiant de device utilise par le SDK Pushwoosh. La logique de comparaison dans `query()` ressemble a une obscurcification legere, pas a un vrai controle d'acces.

**Impact**

- fuite d'un identifiant exploitable pour le tracking inter-app local ;
- augmentation de la surface d'attaque liee au push/analytics ;
- exposition inutile d'un composant qui pourrait etre prive.

**Recommendation**

Passer `android:exported="false"` si aucun partage inter-app n'est attendu. Sinon, proteger le provider avec une permission applicative dediee.

---

### 4. BroadcastReceiver exporte et spoofable sur `INSTALL_REFERRER` (MOYEN)

**Fichiers**

- `AndroidManifest.xml` ligne 49
- `RNDeviceReceiver.smali`

**Preuves**

```xml
<receiver android:enabled="true" android:exported="true" android:name="com.learnium.RNDeviceInfo.RNDeviceReceiver">
    <intent-filter>
        <action android:name="com.android.vending.INSTALL_REFERRER"/>
    </intent-filter>
</receiver>
```

Le receiver persiste directement la valeur recue dans les preferences :

```smali
invoke-virtual {p2, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;
invoke-interface {p1, v0, p2}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
```

**Constat**

Le composant accepte une entree externe et l'ecrit telle quelle dans le stockage applicatif. Sur les versions Android anciennes supportees par l'app, ce type de broadcast a historiquement ete souvent spoofable.

**Impact**

- pollution des donnees d'attribution ;
- manipulation possible de logiques basees sur l'install referrer ;
- augmentation de la confiance accordee a une donnee non authentifiee.

**Recommendation**

Supprimer ce receiver si non indispensable, ou restreindre le traitement a une source verifiee et a des versions Android/supports ou le mecanisme est fiable.

---

### 5. Bypass TLS dormant accessible via l'option `trusty` de RNFetchBlob (MOYEN, conditionnel)

**Fichiers**

- `RNFetchBlobConfig.smali`
- `RNFetchBlobReq.smali`
- `RNFetchBlobUtils.smali`
- `RNFetchBlobUtils$1.smali`
- `RNFetchBlobUtils$2.smali`

**Preuves**

La configuration lit un boolen `trusty` :

```smali
const-string v3, "trusty"
invoke-interface {p1, v3}, Lcom/facebook/react/bridge/ReadableMap;->getBoolean(Ljava/lang/String;)Z
```

Si `trusty == true`, le client HTTP devient volontairement "unsafe" :

```smali
invoke-static {v2}, Lcom/RNFetchBlob/RNFetchBlobUtils;->getUnsafeOkHttpClient(Lokhttp3/OkHttpClient;)Lokhttp3/OkHttpClient$Builder;
```

Le trust manager n'effectue aucune verification :

```smali
.method public checkServerTrusted([Ljava/security/cert/X509Certificate;Ljava/lang/String;)V
    return-void
.end method
```

Et le `HostnameVerifier` accepte tout :

```smali
.method public verify(Ljava/lang/String;Ljavax/net/ssl/SSLSession;)Z
    const/4 p1, 0x1
    return p1
.end method
```

**Constat**

Le binaire embarque un chemin de code permettant de desactiver totalement les verifications TLS. Je n'ai pas retrouve la chaine `trusty` dans `assets/index.android.bundle`, donc l'usage actif n'est pas demontre dans ce livrable, mais la capacite est bien presente dans l'application livree.

**Impact**

- si l'option est activee par le code JS, exposition immediate a des attaques MITM ;
- contournement complet de la verification de certificat et du nom d'hote.

**Recommendation**

Supprimer ce chemin "unsafe" en production, ou le neutraliser derriere un garde-fou impossible a activer hors debug interne.

---

### 6. `DevSettingsActivity` presente mais support developpeur desactive (FAIBLE)

**Fichiers**

- `AndroidManifest.xml` ligne 46
- `BuildConfig.smali`
- `MainApplication$1.smali`

**Preuves**

```xml
<activity android:name="com.facebook.react.devsupport.DevSettingsActivity"/>
```

```smali
.field public static final DEBUG:Z = false
```

```smali
.method public getUseDeveloperSupport()Z
    const/4 v0, 0x0
    return v0
.end method
```

**Constat**

L'activite de support React Native est encore declaree, mais le build est bien en `release` et le support developpeur est desactive.

**Impact**

Risque limite dans l'etat actuel. C'est surtout un residu de configuration qui augmente legerement la surface exposee et brouille la lecture du manifest.

**Recommendation**

Retirer `DevSettingsActivity` du manifest de production.

---

### 7. Endpoints et metadonnees de production hardcodes (INFO)

**Fichier** : `BuildConfig.smali`

**Preuves**

```smali
.field public static final BUILD_TYPE:Ljava/lang/String; = "release"
.field public static final ENVIRONMENT:Ljava/lang/String; = "production"
.field public static final ACCOUNT_ENDPOINT:Ljava/lang/String; = "https://api.nickel.eu/customer-banking-api"
.field public static final CUSTOMER_AUTHENTICATION_ENDPOINT:Ljava/lang/String; = "https://api.nickel.eu/customer-authentication-api"
.field public static final PERSONAL_SPACE_API_ENDPOINT:Ljava/lang/String; = "https://api.nickel.eu/personal-space-api"
```

**Constat**

Ces informations ne constituent pas une compromission a elles seules, mais elles documentent clairement l'architecture cible et simplifient la reconnaissance.

**Recommendation**

Considerer ces donnees comme publiques du point de vue d'un attaquant et eviter toute confiance implicite dans la discretion du client mobile.

---

## Points positifs

### 8. L'implementation RSA utilise le keystore Android (INFO)

**Fichier** : `RSA.smali`

**Elements positifs verifies**

- stockage des cles dans `AndroidKeyStore` ;
- taille de cle `2048` bits ;
- signature `SHA512withRSA` ;
- pas de cle privee hardcodee dans le code analyse.

**Preuves**

```smali
const-string v0, "AndroidKeyStore"
invoke-static {v0}, Ljava/security/KeyStore;->getInstance(Ljava/lang/String;)Ljava/security/KeyStore;
```

```smali
invoke-virtual {p1, v3}, Landroid/security/keystore/KeyGenParameterSpec$Builder;->setKeySize(I)Landroid/security/keystore/KeyGenParameterSpec$Builder;
```

```smali
const-string v0, "SHA512withRSA"
invoke-static {v0}, Ljava/security/Signature;->getInstance(Ljava/lang/String;)Ljava/security/Signature;
```

---

## Definition of Done (DoD)

- [x] Manifest analyse
- [x] Code Smali critique relu manuellement
- [x] Risques confirmes par preuves de code
- [x] Faux positifs reclasses quand necessaire
- [x] Recommandations priorisees redigees
