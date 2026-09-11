# US5 — Évaluation des risques

*Évaluation fondée sur les observations du 10 septembre 2026.*

J’ai évalué les impacts à partir des analyses statique et dynamique. Le risque principal concerne **la confidentialité des saisies**, si des informations sensibles sont entrées pendant l’exécution du programme.

| Risque | Niveau | Constat |
| --- | --- | --- |
| Collecte des saisies | Élevé si données sensibles | Écritures observées ; collecte complète non démontrée. |
| Installation et persistance | Modéré | Fichiers copiés et valeurs Run écrites ; relancement non testé. |
| Envoi du journal | Élevé conditionnel | Aucun transfert observé ; `Env.exe` bloqué. |
| Perturbation du système | Faible dans les essais | Erreur applicative ; aucune destruction démontrée. |

**Aucun vol de mot de passe n’est démontré.** L’erreur Qt et l’absence de réseau limitent l’évaluation de l’envoi SMTP.

## Mesures prioritaires

1. Isoler le poste et arrêter les saisies sensibles.
2. Préserver la mémoire et les traces avant l’arrêt, puis restaurer un état sain.
3. Si des secrets ont pu être exposés, les changer depuis un appareil sain et révoquer les sessions concernées.
4. Surveiller les fichiers et valeurs Run identifiés, limiter le SMTP sortant et l’exécution de logiciels non approuvés.

**US5 validée : impacts décrits, niveaux justifiés et mesures proposées.** Les niveaux sont qualitatifs ; les mesures ne sont pas présentées comme toutes déployées ou testées.

[Analyse statique](../us3/rendu.md) · [Analyse dynamique](../us4/rendu.md) · [Justifications détaillées](../V1/us5/rendu.md).
