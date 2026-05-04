# SEO Skill

Optimise le référencement naturel des pages web statiques.

## Processus

1. **Auditer** — Analyser les balises meta, la structure HTML et les performances
2. **Identifier** — Repérer les manques (title, description, balises sémantiques)
3. **Corriger** — Appliquer les bonnes pratiques SEO on-page
4. **Vérifier** — S'assurer que les modifications n'altèrent pas le rendu

## Points de contrôle prioritaires

### Balises essentielles
- `<title>` unique et descriptif par page (50-60 caractères)
- `<meta name="description">` résumé pertinent (150-160 caractères)
- `<meta name="viewport">` pour le responsive

```html
<title>Calculette DVP aluminium — PLIALU</title>
<meta name="description" content="Calculez le DVP, le prix matière et générez vos devis aluminium sur mesure.">
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Structure sémantique
- Un seul `<h1>` par page, cohérent avec le `<title>`
- Hiérarchie de titres logique (`h1` > `h2` > `h3`)
- Balises sémantiques (`<main>`, `<nav>`, `<header>`, `<footer>`)

### Liens et navigation
- Textes de liens descriptifs (éviter "cliquez ici")
- URLs lisibles et stables
- Pas de liens brisés

### Performances (impact SEO)
- Images avec `alt` et dimensions spécifiées
- Pas de ressources bloquantes inutiles
- Minification des fichiers CSS/JS si possible

### Open Graph (partage réseaux sociaux)
```html
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:type" content="website">
```

## Règles

- Le SEO technique sert aussi l'accessibilité et la performance
- Ne pas sur-optimiser : écrire pour les utilisateurs, pas pour les moteurs
- Pour un site statique sur GitHub Pages, se concentrer sur le SEO on-page

## Output attendu

- Balises meta et structure HTML corrigées
- Commit avec message `seo: <description>`
