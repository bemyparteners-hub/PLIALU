# PLIALU — Module Configurateur

Module Configurateur du CRM PLIALU. Outil web statique pour paramétrer une
pièce (gamme, cotes, matière) et obtenir le DVP, la surface et le prix de
vente avec une vue isométrique en temps réel.

## Règles absolues

- **Aucun framework, aucun build** : HTML/CSS/JS vanilla uniquement
- Pas de backend, pas de CDN, pas d'asset partagé
- GitHub Pages déploie depuis `main`
- Développer sur une branche `claude/...` puis merger via PR

## Place dans le dépôt

Ce module vit sous `modules/configurateur/`. Il est constitué d'un seul
fichier `index.html` totalement auto-suffisant (CSS + JS + données métier
inline, ~50 Ko).

```
modules/configurateur/
├── index.html
└── CLAUDE.md          # Ce fichier
```

## Couplage avec la Calculette

Le configurateur et la calculette sont des modules **techniquement
indépendants** (déploiement, versioning, navigation propre) mais
**fonctionnellement liés** par le workflow `configurer → devis`. Le
couplage est assuré par :

- les **liens croisés dans les navbars** (`../calculette/...` côté
  configurateur, `../configurateur/index.html` côté calculette) ;
- la **convention `localStorage['plialu-devis']`** partagée par origine,
  qui transporte les lignes du configurateur vers `devis.html` sans
  appel inter-module.

Concrètement : un clic « Ajouter au devis » dans le configurateur fait
un `localStorage.setItem('plialu-devis', …)`. À l'ouverture suivante de
`modules/calculette/devis.html`, la file est lue puis vidée.

## localStorage utilisé

| Clé | Contenu |
|---|---|
| `plialu-configurateur-session` | État courant du configurateur (gamme, cotes, matière) — restauré au reload |
| `plialu-devis` | File partagée → poussée vers `devis.html` (lecture seule depuis le configurateur, write-then-read côté devis) |

Le configurateur **ne lit pas** les autres clés (`plialu_project_data`,
`plialu-devis-dessins`) — il sait juste les lister dans son bouton
« Réinitialiser tout ».
