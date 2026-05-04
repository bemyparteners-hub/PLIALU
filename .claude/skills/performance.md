# Performance

Analyse les performances du projet web PLIALU (calcul.html, devis.html, dessinateur.html).

## Points à vérifier

- Taille des fichiers HTML/JS/CSS
- Chargement des scripts externes (jsPDF, pdf-lib)
- Manipulation du DOM (boucles, re-rendus inutiles)
- Canvas : fréquence de redraw, getImageData/putImageData
- localStorage : sérialisation/désérialisation fréquente

## Actions

1. Identifier les goulots d'étranglement
2. Proposer des optimisations concrètes
3. Vérifier que les modifications ne cassent pas les fonctionnalités existantes
