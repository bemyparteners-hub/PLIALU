# Code Review

Effectue une revue de code sur les fichiers du projet PLIALU.

## Points à vérifier

- Cohérence du style (nommage, indentation)
- Sécurité : pas d'injection XSS (escHtml utilisé partout)
- Gestion des erreurs (try/catch sur localStorage, PDF generation)
- Accessibilité : labels, contrastes, navigation clavier
- Logique métier : calculs TVA, références matière, export PDF

## Actions

1. Lire le(s) fichier(s) concerné(s)
2. Signaler les problèmes par ordre de priorité (critique / mineur)
3. Proposer les corrections
