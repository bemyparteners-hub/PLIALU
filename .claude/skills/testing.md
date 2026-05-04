# Testing Skill

Écrit et améliore les tests pour atteindre une couverture > 80 %.

## Processus

1. **Auditer** — Identifier les zones sans tests ou sous-testées
2. **Prioriser** — Couvrir la logique métier critique en premier
3. **Écrire** — Tests unitaires, puis intégration si nécessaire
4. **Valider** — Tous les tests passent avant de committer

## Types de tests à écrire

- **Unitaires** — Fonction isolée, entrée/sortie prévisible
- **Cas limites** — Valeurs nulles, vides, extrêmes, types inattendus
- **Régressions** — Un test par bug corrigé pour éviter la récurrence
- **Intégration** — Flux complet (ex : calcul → localStorage → affichage)

## Règles

- Un test = un comportement précis (nom descriptif)
- Pas de logique dans les tests, données en dur seulement
- Les tests ne doivent pas dépendre d'un ordre d'exécution
- Pour ce projet (vanilla JS) : utiliser des fonctions pures testables sans framework

## Output attendu

- Fichiers de test créés ou complétés
- Rapport de couverture si disponible
- Commit avec message `test: <description>`
