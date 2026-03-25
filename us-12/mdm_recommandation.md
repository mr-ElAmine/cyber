# US 12 : Recommandation MDM

## User Story

**EN TANT QUE** architecte securite  
**JE VEUX** comparer 2 solutions MDM  
**AFIN DE** recommander la plus adaptee

---

## 1. Objet

Ce document compare deux solutions de gestion de terminaux mobiles (MDM/UEM) afin de
proposer une recommandation adaptee a une organisation souhaitant encadrer :

- ses smartphones et tablettes Android/iOS ;
- les usages BYOD et terminaux professionnels ;
- les applications mobiles et l'acces aux ressources de l'entreprise ;
- la conformite, l'effacement a distance et l'application d'une politique mobile.

Les deux solutions comparees sont :

1. **Microsoft Intune**
2. **Omnissa Workspace ONE UEM**

---

## 2. Hypothese retenue pour la recommandation

Comme le contexte exact du client n'est pas detaille, la recommandation ci-dessous repose
sur l'hypothese suivante :

- organisation de taille petite a moyenne ou moyenne ;
- flotte mixte Android et iOS ;
- besoin classique de MDM/UEM : enrolement, conformite, BYOD, separation des donnees,
  distribution d'applications, effacement a distance ;
- environnement bureautique potentiellement deja proche de Microsoft 365 / Entra ID ;
- besoin de solution robuste mais simple a administrer.

Si l'organisation cible est au contraire tres heterogene, multisite, MSP, ou fortement
orientee terminaux durcis / partages / frontline, la conclusion peut evoluer.

---

## 3. Solutions comparees

### 3.1 Microsoft Intune

Microsoft Intune est la solution UEM cloud de Microsoft. Elle permet la gestion des
terminaux Windows, macOS, iOS et Android, tout en s'integrant fortement avec
Microsoft 365, Microsoft Entra ID et Conditional Access.

Points forts attendus :

- forte integration avec l'ecosysteme Microsoft ;
- MAM/MAM-WE (protection applicative sans enrolement complet dans certains cas) ;
- bonne adaptation aux scenarios BYOD ;
- administration centralisee pour les organisations deja clientes Microsoft.

### 3.2 Omnissa Workspace ONE UEM

Workspace ONE UEM est la solution UEM d'Omnissa, orientee gestion unifiee d'un parc
heterogene : mobile, desktop, rugged, shared devices et terminaux specialises.

Points forts attendus :

- couverture tres large des cas d'usage et types de terminaux ;
- orientation multi-tenant et operations a grande echelle ;
- bonne maturite pour les environnements heterogenes ou complexes ;
- gestion poussee des terminaux partages, rugged et frontline.

---

## 4. Tableau comparatif

> Note prix : les prix ci-dessous ont ete observes le **25 mars 2026** sur les pages
> officielles des editeurs, en **USD**, hors taxes et hors remises contractuelles
> eventuelles. Ils peuvent varier selon la region, le canal d'achat et l'engagement.

| Critere | Microsoft Intune | Omnissa Workspace ONE UEM | Analyse |
|---------|------------------|---------------------------|---------|
| Positionnement | UEM cloud fortement integre a Microsoft 365 / Entra | UEM cloud plus large, axe heterogeneite et operations a grande echelle | Intune est plus naturel dans un SI Microsoft ; Workspace ONE est souvent plus fort sur les contextes tres heterogenes |
| OS supportes | Windows, macOS, iOS/iPadOS, Android | Windows, macOS, iOS, Android, Linux, ChromeOS, rugged/specialty devices | Workspace ONE couvre plus explicitement les terminaux specialises |
| BYOD | Oui, avec MAM et Android work profile | Oui, avec prise en charge BYOD et differents modes d'enrolement | Les deux sont adaptes au BYOD |
| Protection des donnees sans enrolement complet | Oui, Intune propose des app protection policies pour iOS/Android, y compris sur appareils non entierement geres selon le scenario | Possible via Workspace ONE, mais l'argument commercial le plus fort est surtout sur la gestion globale du terminal et des apps | Avantage Intune pour les scenarios MAM Microsoft |
| Terminaux corporate-owned | Oui, y compris Android Enterprise fully managed et modes iOS supervises | Oui, avec onboarding, patching, configuration et policies centralisees | Equivalent sur le besoin standard |
| Terminaux partages / rugged / frontline | Pris en charge, mais ce n'est pas son angle principal | Point fort explicite de la solution | Avantage Workspace ONE |
| Multi-tenant / delegation a grande echelle | Possible, mais moins mis en avant comme force produit | Multi-tenant architecture mise en avant officiellement | Avantage Workspace ONE |
| Wipe / selective wipe | Remote wipe et separation des donnees pro/personnelles mis en avant | Enterprise Wipe et Full Device Wipe documentes explicitement | Equivalent fonctionnel, avec bonne lisibilite chez Workspace ONE |
| Securite / Zero Trust | Forte integration avec Entra Conditional Access et posture device | Conditional access, posture, automation et zero trust egalement mis en avant | Intune est souvent plus simple a aligner si Entra est deja en place |
| Automatisation / orchestration | Bonne automatisation dans l'ecosysteme Microsoft | Low-/no-code orchestration et automation mises en avant | Avantage Workspace ONE sur les contextes d'orchestration UEM avances |
| Gestion applicative | Gestion d'apps et app protection tres mature, surtout sur apps Microsoft | Full application lifecycle management avec Intelligent Hub | Equivalent, avec avantage Intune si apps Microsoft 365 dominantes |
| Simplicite de choix / exploitation | Tres lisible pour une organisation deja cliente Microsoft | Plus riche, mais potentiellement plus lourd a cadrer selon le contexte | Avantage Intune dans un contexte standard |
| Prix d'entree observe | Intune Plan 1 : **8 USD / utilisateur / mois** ; Intune Suite : **10 USD / utilisateur / mois** en add-on | Mobile Essentials : **3 USD / device / mois** ou **5,40 USD / user / mois** ; UEM Essentials : **5,25 USD / device / mois** ou **9,45 USD / user / mois** ; Enterprise : **10 USD / device / mois** ou **15 USD / user / mois** | Workspace ONE peut etre competitif selon le mode device-based et le type de flotte ; Intune est souvent rentable si deja inclus dans Microsoft 365 |

---

## 5. Analyse detaillee

### 5.1 Pourquoi Microsoft Intune est tres pertinent

Microsoft Intune est particulierement adapte si l'organisation :

- utilise deja Microsoft 365 ;
- s'appuie sur Microsoft Entra ID pour l'identite ;
- veut une gestion BYOD simple avec protection des donnees d'entreprise ;
- cherche un outil centralise avec une courbe de gouvernance relativement lisible ;
- veut limiter le nombre de solutions a integrer.

L'atout majeur d'Intune est son integration native avec :

- Entra ID ;
- Conditional Access ;
- les applications Microsoft 365 ;
- les politiques de conformite et de protection applicative.

Pour une organisation "standard" qui veut surtout securiser iPhone, iPad et Android
professionnels ou personnels avec un socle Zero Trust raisonnable, Intune est souvent
le meilleur compromis entre securite, exploitation et cout global.

### 5.2 Pourquoi Workspace ONE peut etre meilleur dans certains cas

Workspace ONE devient tres interessant si l'organisation :

- gere une flotte tres heterogene ;
- a beaucoup de terminaux rugged, partages, kiosques ou frontline ;
- a besoin d'une architecture multi-tenant plus marquee ;
- veut une plateforme UEM plus orientee operations de grande echelle ;
- ne souhaite pas centrer son architecture sur Microsoft.

Workspace ONE met clairement en avant :

- la gestion de tous types de terminaux ;
- les usages BYOD, corporate-owned, shared devices et mission-critical specialty devices ;
- l'orchestration et l'automatisation ;
- le multi-tenant ;
- les workflows d'effacement et de remediation.

Dans un contexte retail, logistique, industrie, terrain ou parc tres diversifie,
Workspace ONE peut etre plus adapte qu'Intune.

---

## 6. Recommandation retenue

### Solution recommandee : Microsoft Intune

### Motif principal

Dans l'hypothese retenue d'une organisation classique avec flotte Android/iOS mixte et
besoin de gouvernance mobile moderne, **Microsoft Intune** est la recommandation la
plus adaptee.

### Raisons de la recommandation

1. **Meilleure adequation au besoin standard**
   Intune couvre tres bien les besoins MDM/UEM classiques : BYOD, terminaux corporate,
   conformite, remote wipe, app protection et administration centralisee.

2. **Excellente integration identite et acces**
   L'integration avec Microsoft Entra ID et Conditional Access simplifie fortement la
   mise en oeuvre d'une posture Zero Trust mobile.

3. **Tres bon compromis simplicite / securite**
   Intune est plus simple a justifier, a administrer et a faire adopter dans une
   organisation deja outillee Microsoft.

4. **Valeur economique potentiellement meilleure**
   Si l'organisation dispose deja de licences Microsoft 365 compatibles, Intune peut
   etre deja inclus ou plus economique en cout global qu'une nouvelle brique UEM.

5. **Pertinence forte pour le BYOD**
   Les capacites de protection applicative sans gestion complete du terminal sont un
   vrai atout dans les environnements ou les utilisateurs utilisent leur appareil personnel.

---

## 7. Cas ou il faudrait preferer Workspace ONE

Workspace ONE devrait etre prefere si l'organisation :

- gere un parc tres heterogene ou multisite complexe ;
- doit administrer beaucoup de terminaux partages, rugged, kiosques ou frontline ;
- a besoin d'un modele multi-tenant plus fort ;
- n'a pas de dependance particuliere a Microsoft 365 ;
- privilegie une approche UEM plus large que strictement mobile/BYOD.

---

## 8. Proposition de trajectoire de mise en oeuvre

Si la recommandation Intune est retenue, la trajectoire conseillee est :

1. definir le perimetre : Android/iOS, terminaux pro, BYOD, profils utilisateurs ;
2. connecter Intune a Microsoft Entra ID et aux groupes cibles ;
3. definir les politiques minimales :
   code, chiffrement, version OS minimale, blocage root/jailbreak, wipe, separation pro/perso ;
4. mettre en place les app protection policies pour les applications critiques ;
5. activer les controles de conformite et Conditional Access ;
6. lancer un pilote sur un perimetre restreint ;
7. industrialiser l'enrolement et la supervision ;
8. formaliser les processus d'incident, remplacement, perte/vol et offboarding.

---

## 9. Conclusion

Les deux solutions etudiees sont serieuses et adaptees a un usage entreprise.

**Workspace ONE UEM** est plus fort pour les environnements heterogenes, les terminaux
specialises, le multi-tenant et les contextes operationnels complexes.

**Microsoft Intune** est toutefois la recommandation la plus pertinente dans le cadre
d'une organisation standard cherchant une solution efficace, moderne, bien integree et
simple a gouverner, en particulier si l'ecosysteme Microsoft est deja present.

La recommandation finale retenue est donc :

> **Choisir Microsoft Intune comme solution MDM/UEM de reference**, sauf contexte
> fortement heterogene ou frontline/rugged justifiant plutot Workspace ONE.

---

## 10. Sources officielles utilisees

- [Microsoft Intune Plans and Pricing](https://www.microsoft.com/en-us/security/business/microsoft-intune-pricing)
- [Microsoft Learn - App protection policies in Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policies)
- [Microsoft Learn - Android Enterprise fully managed enrollment](https://learn.microsoft.com/en-us/intune/intune-service/enrollment/android-fully-managed-enroll)
- [Microsoft Learn - Intune BYOD / Android work profile and MAM scenarios](https://learn.microsoft.com/en-us/intune/intune-service/apps/android-deployment-scenarios-app-protection-work-profiles)
- [Omnissa Workspace ONE UEM](https://www.omnissa.com/products/workspace-one-unified-endpoint-management/)
- [Omnissa Tech Zone - What is Workspace ONE UEM?](https://techzone.omnissa.com/resource/what-workspace-one-unified-endpoint-management-uem)
- [Omnissa Tech Zone - What is Workspace ONE?](https://techzone.omnissa.com/resource/what-workspace-one)
- [Omnissa privacy disclosure for Workspace ONE](https://www.omnissa.com/omnissa-workspace-one-privacy-disclosure/)

---

## Definition of Done (DoD)

- [x] Deux solutions MDM comparees
- [x] Tableau comparatif fourni
- [x] Recommandation explicite formulee
- [x] Hypothese de contexte documentee
- [x] Livrable Markdown fourni
