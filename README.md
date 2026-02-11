Avantages observés
L’automatisation des tests évite de tout retester à la main après chaque modification. Le CI/CD permet d’exécuter les tests automatiquement à chaque push et bloque les merges si quelque chose casse, donc ça évite d’intégrer du code non fonctionnel. Ça rend le projet plus fiable et plus rapide à valider.

Défis rencontrés
Selenium est assez fragile si on ne met pas de WebDriverWait ça crash direct, car les éléments ne sont pas toujours chargés au bon moment et ça provoque des erreurs. Le mode headless sur GitHub Actions a aussi été compliqué à configurer, surtout avec les problèmes de ChromeDriver et de compatibilité Linux/Windows. J'ai aussi rencontré des blocages de sécurité Windows (Smart App Control) qui empêchaient l’exécution du driver et meme en général me bloquait énormément.

Métriques importantes

Les métriques principales sont le taux de réussite des tests, le temps total du pipeline et la couverture de code. On vérifie si les builds passent à chaque push, combien de temps prend l’exécution complète, et si les tests couvrent correctement les fonctionnalités importantes
