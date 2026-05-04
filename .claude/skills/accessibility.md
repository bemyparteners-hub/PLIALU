# Accessibility Skill

Améliore l'accessibilité des interfaces pour tous les utilisateurs.

## Processus

1. **Auditer** — Analyser le HTML et les interactions existantes
2. **Identifier** — Repérer les problèmes de navigation clavier, contraste, sémantique
3. **Corriger** — Appliquer les améliorations WCAG 2.1 niveau AA
4. **Tester** — Vérifier avec la navigation clavier et les outils de contraste

## Points de contrôle prioritaires

### Sémantique HTML
- Utiliser les balises appropriées (`<button>` pour les actions, `<a>` pour la navigation)
- Structure de titres cohérente (`h1` > `h2` > `h3`)
- Labels associés aux inputs (`<label for="id">` ou `aria-label`)

### Navigation clavier
- Tous les éléments interactifs doivent être atteignables au clavier
- Ordre de tabulation logique
- Focus visible (ne jamais faire `outline: none` sans alternative)

### ARIA
- Utiliser ARIA uniquement quand le HTML natif ne suffit pas
- `aria-label` pour les éléments sans texte visible (icônes)
- `aria-live` pour les zones mises à jour dynamiquement (résultats de calcul)

### Contraste
- Texte normal : ratio minimum 4.5:1
- Texte large (18px+ ou 14px gras) : ratio minimum 3:1
- Vérifier avec les outils de contraste WCAG

### Images et médias
- `alt` descriptif pour les images informatives
- `alt=""` pour les images décoratives

## Règles

- L'accessibilité bénéficie à tous, pas seulement aux personnes en situation de handicap
- Préférer le HTML sémantique natif aux solutions ARIA complexes
- Tester avec un vrai clavier, pas seulement avec la souris

## Output attendu

- HTML et JS corrigés pour l'accessibilité
- Commit avec message `a11y: <description>`
