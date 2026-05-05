# LINK-AUDIT — Audit préventif des liens CSS partagés

> Lecture seule. Aucun correctif appliqué. Date : 2026-05-04.
> Vérifie que chaque page HTML charge les fichiers de `shared/` dont
> elle utilise les classes, et qu'elle ne charge rien d'inutile.

---

## Légende

- **✓✓** : fichier `<link>`-é **et** au moins une classe / un selecteur
  qu'il fournit est utilisé dans le HTML / `<style>` inline.
- **✓** : fichier `<link>`-é mais **aucune** classe utilisée → *lien mort*.
- **⚠ INLINE** : classe / sélecteur utilisé dans le HTML mais le shared
  correspondant **n'est pas chargé**. La page définit la classe inline
  pour son propre compte (look intentionnellement différent du canonique).
- **✗ BUG** : classe utilisée mais ni shared ni inline ne la définit
  (rendu cassé). *Aucun cas dans le dépôt.*
- **—** : non chargé, non utilisé (correctement absent).

Classes/sélecteurs fournis par chaque shared :

| Fichier | Fournit |
|---|---|
| `tokens.css` | `:root` custom properties (consommées via `var(--*)`) |
| `theme-dark.css` | surcharges `:root` du thème sombre |
| `components/navbar.css` | `.nav`, `.nav-brand[--static]`, `.nav-mark`, `.nav-title[--hub]`, `.nav-title-prefix`, `.nav-links`, `.nav-btn[--active]` |
| `components/sidebar.css` | `.sidebar`, `.sidebar-header`, `.sidebar-mark`, `.sidebar-title[-prefix]`, `.sidebar-section[-label]`, `.sidebar-links`, `.sidebar-link[-icon, --active, --placeholder]`, `.sidebar-footer` |
| `components/buttons.css` | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger`, `.btn-reset`, `.btn-sm`, `.btn-lg`, `.btn-icon` |
| `components/card.css` | `.card`, `.card-title`, `.card-active`, `.card--rich`, `.card-icon`, `.card-arrow`, `.card-tags`, `.card-tag` (+ `.card--rich h3/p`) |
| `components/form.css` | `input`, `select`, `textarea`, `label` (sélecteurs d'éléments) |

---

## Tableau synthétique

| Page | tokens | theme-dark | navbar | sidebar | buttons | card | form |
|---|---|---|---|---|---|---|---|
| `index.html` (hub) | ✓✓ (33) | — | — | ✓✓ (12) | ✓✓ | ✓✓ | — |
| `modules/calculette/index.html` | ✓✓ (6) | — | ✓✓ (7) | — | ✓✓ | ✓✓ | — |
| `modules/calculette/calcul.html` | ✓✓ (3) | — | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ (43) |
| `modules/calculette/devis.html` | ✓✓ (3) | — | ✓✓ | — | ✓✓ | ✓✓ | ✓✓ (32) |
| `modules/calculette/dessinateur.html` | ✓✓ (11) | — | ✓✓ | — | ✓✓ | ✓✓ | ✓✓ (6) |
| `modules/configurateur/index.html` | ✓✓ (4) | — | ✓✓ | — | ✓✓ | ✓✓ | ✓✓ (41) |
| `modules/maxcut/index.html` | ✓✓ (134) | ✓✓ | ✓✓ | — | ✓✓ | — *(see A1)* | **⚠ INLINE** (19) |

Les nombres entre parenthèses indiquent :
- pour `tokens.css` : occurrences de `var(--*)` dans le `<style>` inline.
- pour `navbar.css` / `sidebar.css` : nombre de classes shared distinctes utilisées.
- pour `form.css` : nombre d'éléments `<input>/<select>/<textarea>/<label>` dans le markup.

---

## Détail page par page

### `index.html` (hub)

- **CSS chargés** : `tokens.css` · `sidebar.css` · `buttons.css` · `card.css`
- **Classes shared utilisées** :
  - `sidebar*` (12) — `sidebar`, `sidebar-header`, `sidebar-mark`, `sidebar-title`, `sidebar-title-prefix`, `sidebar-section`, `sidebar-section-label`, `sidebar-links`, `sidebar-link`, `sidebar-link-icon`, `sidebar-link--placeholder`, `sidebar-footer`
  - `card*` (6) — `card`, `card--rich`, `card-icon`, `card-arrow`, `card-tags`, `card-tag`
  - `btn*` (4) — `btn`, `btn-primary`, `btn-secondary`, `btn-lg`
- **Tokens consommés** : 33 `var()` dans le `<style>` inline (hub-hero, hub-modules, etc.)
- **Statut** : ✅ tout cohérent.

### `modules/calculette/index.html` (dashboard)

- **CSS chargés** : `tokens.css` · `navbar.css` · `buttons.css` · `card.css`
- **Classes shared utilisées** :
  - `nav*` (7) · `card*` (5) · `btn*` (3 : `btn`, `btn-primary`, `btn-reset`)
- **Classes inline page-spécifiques** :
  - `btn-outline` (l. 72) — variant CTA hero, transparent + bordure blanche, défini inline car non couvert par buttons.css canonique.
- **Tokens consommés** : 6 occurrences.
- **Statut** : ✅ depuis le fix `72a86a7` (commit précédent).

### `modules/calculette/calcul.html`

- **CSS chargés** : tokens · navbar · buttons · card · form
- **Classes shared utilisées** :
  - `nav*` (7) · `btn*` (3) · `card*` (2 : `card`, `card-title`)
- **Classes inline page-spécifiques** :
  - `btn-group` (l. 23) — wrapper flex de boutons
  - `btn-calc-row` (l. 68) — décalage `margin-top` du bouton Calculer
- **Form** : 43 éléments `<input>/<select>/<label>` → form.css consommé.
- **Statut** : ✅

### `modules/calculette/devis.html`

- **CSS chargés** : tokens · navbar · buttons · card · form
- **Classes shared utilisées** :
  - `nav*` (7) · `btn*` (7 : `btn`, `btn-primary`, `btn-secondary`, `btn-danger`, `btn-reset`, `btn-sm`, `btn-lg`) · `card*` (2)
- **Form** : 32 éléments.
- **Statut** : ✅

### `modules/calculette/dessinateur.html`

- **CSS chargés** : tokens · navbar · buttons · card · form
- **Classes shared utilisées** :
  - `nav*` (7) · `btn*` (4 : `btn`, `btn-primary`, `btn-secondary`, `btn-reset`) · `card*` (2)
- **Form** : 6 éléments.
- **Statut** : ✅

### `modules/configurateur/index.html`

- **CSS chargés** : tokens · navbar · buttons · card · form
- **Classes shared utilisées** :
  - `nav*` (7) · `btn*` (4) · `card*` (2)
- **Form** : 41 éléments.
- **Statut** : ✅

### `modules/maxcut/index.html`

- **CSS chargés** : tokens · **theme-dark** · navbar · buttons (pas de card, pas de form, pas de sidebar)
- **Classes shared utilisées** :
  - `nav*` (9, dont `nav-tab`/`nav-tabs` qui sont des classes **page-spécifiques** — voir note infra) · `btn*` (8 : tous sauf `btn-reset`)
- **Classes utilisées sans `<link>` correspondant** :
  - `card`, `card-title`, `card-header` → définies **inline** dans le `<style>` de MAX, **différentes** du canonique (thème sombre, font-size, no border-bottom accent).
- **Form** : 19 éléments `<input>/<select>/<textarea>/<label>` → stylés inline via `.form-control` / `.pieces-table input` / `.format-inputs input` (pas de form.css canonique chargé).
- **Tokens consommés** : 134 occurrences (MAX consomme intensivement les tokens partagés depuis la migration phase 2 commit 8).
- **Statut** : ✅ visuellement correct, mais **shadow-naming** intentionnel (voir Anomalies).

---

## Anomalies à corriger

> Strictement parlant, **aucune classe n'est utilisée sans avoir été
> définie quelque part** (shared ou inline). Donc **aucun rendu cassé**.
> **Aucun lien `<link>` mort** détecté non plus.

### A1 — Shadow-naming des classes `card` / `card-title` dans MAXCUT — ✅ RÉSOLU

**Statut** : résolu le 2026-05-04 par `caf08b5` (option (a) — préfixe explicite — retenue).

Les trois classes ambiguës de `modules/maxcut/index.html` ont été
renommées avec le préfixe `max-` pour casser l'homonymie avec le
canonique de `shared/components/card.css` :

| Avant | Après |
|---|---|
| `.card` | `.max-card` |
| `.card-header` | `.max-card-header` |
| `.card-title` | `.max-card-title` |

Le rendu visuel est inchangé (refactor purement nominatif, le sélecteur
CSS et la classe HTML ont été modifiés en tandem). Les autres familles
préfixées (`.stat-card`, `.plan-card-*`, `.mat-card-*`) n'étaient pas
ambiguës et restent intactes.

**Contexte original** (laissé pour référence) :

> `modules/maxcut/index.html` utilisait les classes `.card`,
> `.card-title`, `.card-header` mais **ne chargeait pas**
> `shared/components/card.css`. Ses définitions inline divergeaient
> volontairement du canonique (thème sombre). Risque : un futur
> contributeur qui ajouterait `<div class="card">` à `maxcut/index.html`
> en s'attendant au rendu canonique aurait eu le rendu sombre, et
> inversement.

### A2 — `form.css` non chargé dans MAXCUT alors que la page contient 19 éléments de formulaire

**Sévérité** : informationnelle. Pas un bug, par conception.

MAX style ses inputs et selects via des sélecteurs class-scopés inline
(`.form-control`, `.pieces-table input`, `.format-inputs input`) qui ont
une spécificité supérieure au sélecteur d'élément `input` du shared
form.css. Si form.css était chargé, il s'appliquerait aux inputs **sans
classe** (s'il y en a) — autrement il serait inerte.

**Risque** : faible. Si quelqu'un ajoute un `<input>` nu dans MAX, il
récupérera les styles natifs du navigateur (texte sombre sur fond clair)
au lieu d'un input cohérent avec le thème sombre. Cas peu probable étant
donné la maturité de la page.

### A3 — Classes `nav-tab` / `nav-tabs` dans MAXCUT homonymes du namespace navbar

**Sévérité** : très faible. Faux positif de mon scan.

MAX a des `.nav-tab` / `.nav-tabs` (sous-tabs internes Pièces / Paramètres
/ Résultats) qui sont **page-spécifiques** et n'ont rien à voir avec
les `.nav-btn` de la navbar shared. Ils ne polluent pas mais le préfixe
`nav-` est trompeur.

**Option** : renommer en `.section-tabs` / `.section-tab` pour clarifier.

---

## Récap quantitatif

| Indicateur | Valeur |
|---|---|
| Pages auditées | 7 |
| Liens shared morts (CSS chargé sans usage) | **0** |
| Classes orphelines (utilisées sans CSS qui les définit) | **0** |
| Pages avec rendu visuellement cassé | **0** |
| Notes informationnelles (shadow-naming, etc.) | 3 |

Le dépôt est dans un état cohérent : chaque `<link>` shared correspond
à un usage réel dans la page, et chaque classe utilisée est définie
quelque part dans la cascade. Les 3 notes informationnelles concernent
toutes MAXCUT et sont **par design** dues à son thème sombre divergent.

---

## Méthode

```bash
# Pour chaque fichier HTML :
grep -oE '<link[^>]*shared[^>]*>' "$f"          # CSS chargés
grep -oE 'class="[^"]+"' "$f" | tr ' ' '\n' \
  | grep -E '^(card|btn|nav|sidebar)'           # classes shared utilisées
awk '/<style/,/<\/style>/' "$f" \
  | grep -ocE 'var\(--'                         # tokens consommés inline
grep -ocE '<(input|select|textarea|label)[ />]' # éléments de form
```

Cross-référence manuelle avec le contenu de `shared/components/*.css`.
