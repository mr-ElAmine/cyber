# US 11 : Politique de securite mobile

## User Story

**EN TANT QUE** responsable securite  
**JE VEUX** proposer une politique mobile  
**AFIN DE** encadrer le developpement et l'usage des applications mobiles

---

## 1. Objet

La presente politique de securite mobile definit les exigences minimales de securite
applicables aux terminaux mobiles, aux applications mobiles et aux services associes.

Elle a pour objectif de :

- proteger les donnees de l'organisation ;
- limiter les risques lies a la perte, au vol ou a la compromission d'un terminal ;
- encadrer le developpement, le deploiement et la maintenance des applications mobiles ;
- fixer les responsabilites des equipes metier, IT, RSSI, developpement et utilisateurs ;
- imposer un niveau de securite coherent sur l'ensemble du cycle de vie mobile.

---

## 2. Perimetre

Cette politique s'applique :

- aux smartphones et tablettes appartenant a l'organisation ;
- aux terminaux personnels autorises a acceder au SI de l'organisation dans un cadre BYOD ;
- aux applications mobiles developpees en interne ;
- aux applications mobiles editees par des tiers mais utilisees pour des besoins professionnels ;
- aux environnements de test, preproduction et production relies aux applications mobiles ;
- aux donnees professionnelles stockees, traitees ou transmises depuis un terminal mobile.

Cette politique couvre Android et iOS, sauf mention contraire.

---

## 3. Principes generaux

Les principes suivants sont obligatoires :

- le mobile est considere comme un point d'entree du systeme d'information ;
- toute donnee stockee sur un terminal mobile doit etre consideree comme exposee en cas de compromission du terminal ;
- aucun secret critique ne doit etre suppose protege du seul fait qu'il est embarque dans une application mobile ;
- tout flux reseau doit etre protege par chiffrement fort et verification d'integrite ;
- l'acces mobile aux ressources de l'organisation doit etre limite au strict besoin ;
- la securite mobile doit etre traitee sur tout le cycle de vie : conception, developpement, test, deploiement, exploitation, retrait.

---

## 4. Roles et responsabilites

### 4.1 Direction

La direction :

- approuve la presente politique ;
- alloue les moyens necessaires a sa mise en oeuvre ;
- arbitre les exceptions majeures si le risque est documente.

### 4.2 RSSI / Equipe securite

Le RSSI ou l'equipe securite :

- maintient la politique et les standards associes ;
- definit les exigences minimales techniques ;
- valide les exceptions de securite documentees ;
- suit les incidents et les plans de remediation.

### 4.3 Equipe IT / MDM

L'equipe IT :

- administre les terminaux geres ;
- maintient la plateforme MDM/UEM ;
- applique les profils de configuration, les contraintes de chiffrement et les regles de conformite ;
- gere l'enrolement, le retrait et l'effacement a distance.

### 4.4 Equipes de developpement

Les equipes de developpement :

- appliquent les regles de developpement securise ;
- corrigent les vulnerabilites identifiees ;
- documentent les bibliotheques tierces, API, secrets techniques et autorisations demandees ;
- assurent la mise a jour reguliere des dependances.

### 4.5 Utilisateurs

Les utilisateurs :

- protegent physiquement leur terminal ;
- respectent les consignes de verrouillage, mise a jour et usage des applications ;
- signalent sans delai toute perte, vol, compromission ou comportement suspect.

---

## 5. Exigences de securite des terminaux

Tout terminal autorise a acceder a des donnees ou services professionnels doit respecter
les exigences suivantes :

- verrouillage par code, mot de passe fort, biometrie ou combinaison equivalente ;
- chiffrement natif du terminal active ;
- mise a jour reguliere de l'OS et des correctifs de securite ;
- verrouillage automatique apres une duree d'inactivite definie par l'organisation ;
- effacement automatique ou blocage apres plusieurs tentatives d'authentification echouees ;
- interdiction des terminaux rootes, jailbreakes ou modifies hors controles de l'organisation ;
- interdiction d'installer des applications depuis des sources non approuvees sur les terminaux professionnels ;
- capacite d'effacement a distance pour les terminaux geres ;
- separation des donnees personnelles et professionnelles lorsqu'un mode BYOD est autorise.

Un terminal non conforme doit etre bloque ou place en acces restreint.

---

## 6. Controle d'acces et authentification

Les regles suivantes s'appliquent a l'acces mobile :

- le principe du moindre privilege est obligatoire ;
- l'authentification forte doit etre imposee pour les acces sensibles ;
- les comptes de service et tokens techniques doivent etre limites et traces ;
- les sessions doivent expirer apres une duree raisonnable d'inactivite ;
- les mecanismes de renouvellement de session doivent etre proteges contre l'abus ;
- les secrets d'authentification ne doivent pas etre stockes en clair sur le terminal ;
- les clefs, certificats et secrets locaux doivent etre stockes dans les mecanismes securises du systeme (`Android Keystore`, `Keychain`, equivalent) ;
- les terminaux non conformes ne doivent pas obtenir un acces complet aux ressources de l'organisation.

---

## 7. Exigences de developpement securise des applications mobiles

### 7.1 Conception

Avant developpement, chaque application mobile doit :

- faire l'objet d'une classification des donnees traitees ;
- identifier ses dependances critiques ;
- documenter ses flux reseau, son stockage local et ses integrations tierces ;
- definir ses exigences d'authentification, de chiffrement et de journalisation ;
- prevoir des tests de securite adaptes au niveau de criticite.

### 7.2 Gestion des secrets

Les regles suivantes sont obligatoires :

- aucune cle privee, mot de passe, secret d'administration ou jeton privilegie ne doit etre hardcode dans l'application ;
- les API keys cote client doivent etre considerees comme potentiellement exposables ;
- toute cle API embarquee doit etre restreinte au strict usage necessaire ;
- les secrets doivent etre geres par un mecanisme dedie cote serveur ou par une solution de secret management ;
- les rotations de secrets doivent etre prevues et documentees.

### 7.3 Communications reseau

Les applications mobiles doivent :

- utiliser TLS par defaut pour tout flux externe ou interne ;
- interdire le cleartext traffic sauf exception formelle et documentee ;
- verifier les certificats et les noms d'hotes ;
- ne pas embarquer de mode "trust all", "unsafe SSL" ou equivalent en production ;
- proteger les flux sensibles contre les attaques de type MITM.

### 7.4 Stockage local

Le stockage local doit respecter les exigences suivantes :

- minimisation des donnees stockees sur le terminal ;
- pas de stockage en clair de secrets, tokens longue duree ou donnees sensibles ;
- chiffrement des donnees locales sensibles ;
- purge des donnees de session a la deconnexion ou a l'expiration ;
- limitation de l'usage des logs contenant des donnees utilisateur ou des secrets.

### 7.5 Permissions et surface d'attaque

Les applications doivent :

- demander uniquement les permissions strictement necessaires ;
- documenter toute permission sensible ;
- minimiser les composants exportes ;
- proteger les `Activity`, `Service`, `BroadcastReceiver` et `ContentProvider` exposes ;
- supprimer les composants de debug, de test ou de support developpeur des builds de production.

### 7.6 Bibliotheques tierces

Les equipes de developpement doivent :

- maintenir un inventaire des SDK et dependances tierces ;
- suivre les avis de securite des bibliotheques utilisees ;
- corriger ou remplacer rapidement les composants vulnerables ;
- eviter d'inclure des SDK non necessaires ou sans justification metier.

---

## 8. Tests de securite et validation avant mise en production

Avant mise en production, une application mobile doit au minimum faire l'objet :

- d'une revue de code ou d'une validation technique ;
- d'un scan automatise de securite adapte au contexte ;
- d'une verification des secrets exposes ;
- d'une revue des permissions et composants exportes ;
- d'une verification du chiffrement du transport ;
- d'une verification des mecanismes d'authentification et de session ;
- d'un test de regressions de securite apres correction d'une faille majeure.

Pour les applications critiques, des tests complementaires sont exiges :

- reverse engineering ;
- tests d'integrite et anti-tampering ;
- tests d'API ;
- verification de configuration cloud associee ;
- pentest mobile cible.

---

## 9. Distribution, signature et mises a jour

Les regles de deploiement suivantes sont obligatoires :

- les applications doivent etre signees avec des certificats maitrises par l'organisation ou l'editeur autorise ;
- les keystores et certificats de signature doivent etre stockes dans un environnement securise ;
- les keystores de test ne doivent jamais etre utilises en production ;
- toute mise a jour doit suivre un processus de validation et de tracabilite ;
- les correctifs de securite doivent etre deployes prioritairement ;
- les versions obsoletes ou vulnerables doivent etre retirees ou bloquees.

---

## 10. Journalisation, supervision et protection des donnees

Les applications et services mobiles associes doivent :

- journaliser les evenements de securite pertinents ;
- eviter toute journalisation de secret, mot de passe, token ou donnees personnelles non necessaires ;
- transmettre les journaux utiles vers un systeme de supervision si le contexte le justifie ;
- permettre la detection d'echecs d'authentification, d'anomalies d'integrite et d'usage suspect ;
- respecter les exigences legales et contractuelles relatives a la protection des donnees.

Les donnees personnelles et sensibles doivent etre traitees selon les principes suivants :

- minimisation ;
- limitation de finalite ;
- duree de conservation definie ;
- protection en transit et au repos ;
- suppression ou anonymisation lorsque cela est requis.

---

## 11. BYOD, MDM et conformite des terminaux

Si le BYOD est autorise, il doit etre encadre par une solution MDM/UEM ou un mecanisme
equivalent permettant au minimum :

- l'enrolement du terminal ;
- la verification de conformite ;
- l'application de politiques de code, chiffrement et verrouillage ;
- la separation des donnees professionnelles ;
- le retrait des donnees professionnelles sans effacement complet des donnees personnelles, lorsque c'est techniquement possible ;
- le blocage de l'acces en cas de non-conformite.

Pour les terminaux professionnels, l'usage d'une solution MDM/UEM est obligatoire.

---

## 12. Gestion des incidents mobiles

Tout incident mobile doit etre traite selon un processus documente.

Les evenements suivants doivent etre signales sans delai :

- perte ou vol d'un terminal ;
- suspicion de malware ou de compromission ;
- fuite de donnees ;
- decouverte de secrets exposes dans une application ;
- detection d'un comportement reseau anormal ;
- detection d'une faille critique dans une application ou un SDK mobile.

Les actions minimales attendues sont :

- qualification de l'incident ;
- confinement ;
- blocage ou effacement du terminal si necessaire ;
- rotation des secrets ou tokens compromis ;
- analyse des causes ;
- correction et suivi post-incident.

---

## 13. Exceptions

Toute exception a la presente politique doit :

- etre documentee ;
- etre justifiee par un besoin metier ou technique explicite ;
- faire l'objet d'une evaluation de risque ;
- comporter une date de fin ou de revue ;
- etre approuvee par les responsables competents.

Aucune exception ne doit autoriser sans validation formelle :

- l'embarquement de secrets administratifs ;
- la desactivation durable des verifications TLS ;
- l'usage de terminaux rootes/jailbreakes ;
- le maintien en production d'un composant critique connu comme vulnerable sans plan d'action.

---

## 14. Controle, revue et mise a jour

La presente politique doit etre revue :

- au moins une fois par an ;
- en cas d'evolution majeure du parc mobile ;
- en cas de changement reglementaire ou contractuel ;
- apres un incident de securite mobile significatif ;
- apres l'introduction d'une nouvelle solution MDM/UEM ou d'un nouveau standard de developpement mobile.

Des controles periodiques peuvent etre realises pour verifier l'application effective
de cette politique sur les terminaux, les applications et les environnements associes.

---

## 15. Entree en vigueur

Cette politique entre en vigueur a compter de sa validation par l'organisation.

Elle s'impose a toute equipe ou utilisateur entrant dans son perimetre d'application.

---

## 16. Resume des exigences minimales

En synthese, l'organisation impose au minimum :

- terminaux a jour, chiffres et verrouilles ;
- authentification forte pour les usages sensibles ;
- zero secret critique hardcode dans les applications ;
- TLS obligatoire et aucun mode "trust all" en production ;
- permissions et composants exportes reduits au strict necessaire ;
- revue de securite avant mise en production ;
- gestion des terminaux via MDM/UEM des qu'un acces professionnel est autorise ;
- declaration rapide des incidents et remediation documentee.

---

## Definition of Done (DoD)

- [x] Politique mobile redigee
- [x] Regles pour terminaux, applications et usages documentees
- [x] Exigences de developpement securise integrees
- [x] Gestion MDM/BYOD incluse
- [x] Livrable Markdown fourni
