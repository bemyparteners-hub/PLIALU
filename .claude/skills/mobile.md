# Mobile Skill

Optimise l'expérience sur appareils mobiles et tactiles.

## Processus

1. **Auditer** — Inspecter le CSS responsive, les tailles de cibles tactiles, la lisibilité
2. **Identifier** — Repérer les éléments trop petits, les débordements, les interactions non adaptées
3. **Corriger** — Appliquer les ajustements responsive et tactiles
4. **Tester** — Vérifier aux breakpoints courants (360px, 768px)

## Points de contrôle prioritaires

### Viewport et base responsive
- `<meta name="viewport" content="width=device-width, initial-scale=1">` obligatoire
- Pas de largeurs fixes en px sur les conteneurs principaux
- Utiliser `max-width` plutôt que `width` fixe

### Cibles tactiles
- Taille minimale de 44×44px pour les boutons et liens (recommandation Apple/Google)
- Espacement suffisant entre les éléments cliquables

```css
button, a, input, select {
  min-height: 44px;
  min-width: 44px;
}
```

### Typographie
- Taille de police minimale 16px pour les inputs (évite le zoom automatique iOS)
- Corps de texte lisible sans zoom (minimum 14-16px)
- Interligne suffisant (`line-height: 1.5` minimum)

### Formulaires et inputs
- `type` approprié sur les inputs (`number`, `email`, `tel`) pour le bon clavier virtuel
- Labels toujours visibles (pas uniquement en placeholder)
- Éviter les selects ou checkboxes trop petits

### Mise en page
- Flex/Grid avec wrapping pour les éléments en ligne
- Pas de `overflow: hidden` qui masque du contenu sur petits écrans
- Tableaux : prévoir un scroll horizontal ou une mise en page alternative

### Performance mobile
- Éviter les images lourdes sans compression
- Limiter les reflows/repaints coûteux sur scroll

## Règles

- Mobile-first : concevoir d'abord pour petit écran, agrandir ensuite
- Tester sur vrai appareil ou émulateur, pas seulement en redimensionnant la fenêtre
- Ne pas désactiver le zoom utilisateur (`user-scalable=no` est à proscrire)

## Output attendu

- CSS et HTML adaptés au mobile
- Commit avec message `mobile: <description>`
