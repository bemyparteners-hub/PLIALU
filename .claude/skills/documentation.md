# Documentation Skill

Documente le code de façon claire et maintenable.

## Processus

1. **Lire** — Comprendre le code avant de rédiger quoi que ce soit
2. **Identifier** — Repérer les fonctions publiques, les modules complexes, les décisions non évidentes
3. **Documenter** — JSDoc pour les fonctions, commentaires inline pour la logique obscure
4. **Vérifier** — La documentation doit rester synchronisée avec le code

## Ce qu'il faut documenter

- **Fonctions publiques** — Paramètres, valeur de retour, effets de bord
- **Décisions architecturales** — Pourquoi ce choix plutôt qu'un autre
- **Cas limites** — Comportement attendu avec des valeurs inattendues
- **Flux de données** — Comment les données circulent entre les composants

## Format JSDoc (vanilla JS)

```js
/**
 * Calcule le DVP d'une pièce aluminium.
 * @param {number[]} segments - Longueurs des segments en mm
 * @param {number} epaisseur - Épaisseur du matériau en mm
 * @returns {number} DVP total en mm
 */
function calculerDVP(segments, epaisseur) { ... }
```

## Règles

- Ne pas documenter ce qui est évident (`i++` ne nécessite pas de commentaire)
- Un commentaire qui répète le code est pire qu'aucun commentaire
- Mettre à jour la doc en même temps que le code, jamais après

## Output attendu

- Fonctions documentées avec JSDoc
- Commentaires utiles sur la logique complexe
- Commit avec message `docs: <description>`
