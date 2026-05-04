# Refactor Skill

Nettoie et simplifie le code sans changer son comportement.

## Processus

1. **Lire** — Comprendre entièrement le code avant de toucher quoi que ce soit
2. **Identifier** — Repérer la duplication, la complexité inutile, les noms obscurs
3. **Prioriser** — Traiter en premier ce qui apporte le plus de clarté
4. **Refactorer** — Un changement à la fois, vérifier entre chaque étape
5. **Valider** — Le comportement observable doit rester identique

## Patterns courants

- Extraire une fonction si un bloc est utilisé 2+ fois
- Renommer variables/fonctions pour qu'elles décrivent l'intention
- Supprimer le code mort et les commentaires obsolètes
- Aplatir les conditions imbriquées (early return)
- Remplacer les magic numbers par des constantes nommées

## Règles

- Pas de nouvelles fonctionnalités pendant un refactor
- Conserver la compatibilité avec le reste du code
- Commit séparé du travail fonctionnel

## Output attendu

- Code plus lisible, même comportement
- Commit avec message `refactor: <description>`
