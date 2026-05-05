# shared/ — Design system PLIALU

Système de design partagé entre le hub CRM et les modules
(`calculette`, `configurateur`, `maxcut`). Tout est servi en
**HTML/CSS/JS vanilla**, sans build, donc compatible `file://`
et GitHub Pages.

---

## Arborescence

```
shared/
├── tokens.css                  # Tokens globaux (thème clair par défaut)
├── theme-dark.css              # Surcharges du thème sombre
├── preview.html                # Aperçu visuel des composants
├── README.md                   # Ce fichier
└── components/
    ├── navbar.css              # Navbar horizontale + logo (modules)
    ├── sidebar.css              # Sidebar verticale + logo (hub uniquement)
    ├── buttons.css              # .btn + variantes
    ├── card.css                 # .card / .card-title / .card-active /
    │                            #   .card--rich + .card-icon / -arrow / -tags
    └── form.css                 # input/select/textarea + label
```

---

## Système de tokens

`tokens.css` définit l'ensemble des valeurs canoniques sur `:root`
(thème clair par défaut). `theme-dark.css` surcharge un sous-ensemble
de surfaces et de textes pour les pages en thème sombre.

### Catégories

| Catégorie | Préfixe | Exemples |
|---|---|---|
| Brand | `--brand-*`, `--accent*` | `--brand-900`, `--accent`, `--accent-hover`, `--accent-glow` |
| Surfaces | `--bg-*` | `--bg-app`, `--bg-elevated`, `--bg-muted`, `--bg-secondary` |
| Texte | `--text-*` | `--text-primary`, `--text-on-brand`, `--text-muted`, `--text-disabled` |
| Bordures | `--border-*` | `--border-soft`, `--border-strong` |
| Statuts | `--success-*`, `--warning-*`, `--danger-*` | fonds, bordures, textes |
| Espacements | `--space-N` | 1=4 / 2=8 / 3=12 / 4=16 / 5=20 / 6=24 / 8=32 |
| Rayons | `--radius*` | `--radius-sm` (6), `--radius` (8), `--radius-lg` (12) |
| Layout | `--nav-height` | hauteur des navbars (52) |
| Typographie | `--font-sans`, `--text-*` | `--text-xs` (11) à `--text-xl` (18) |
| Ombres | `--shadow-*` | `--shadow-card`, `--shadow-card-hover` |

Voir `tokens.css` pour la liste complète et les valeurs.

### Thèmes

- **Clair** (défaut) : appliqué via `<link rel="stylesheet" href="…/shared/tokens.css">`.
- **Sombre** : `theme-dark.css` existe mais n'est chargé par **aucune page en production**. Pour activer un thème sombre sur un module :
  ```html
  <link rel="stylesheet" href="…/shared/tokens.css">
  <link rel="stylesheet" href="…/shared/theme-dark.css"> <!-- APRÈS tokens.css -->
  ```
  Surcharge `--bg-*`, `--text-*`, `--border-*`, et les couleurs de statut.

> **Note** : aucun module ne charge `theme-dark.css` actuellement. Dernier
> usage : MAXCUT, retiré le 2026-05-04 lors du passage en thème clair
> unifié. Le fichier est volontairement conservé (cf. commentaire en tête)
> car il encode des choix design non triviaux (inversion des surfaces,
> mappings statuts, bordures alpha-blendées) prêts à être ré-utilisés.

---

## Composants

### `navbar.css` — Navbar + logo

Markup canonique d'un module :

```html
<nav class="nav">
  <a class="nav-brand" href="../../index.html" title="Retour au hub CRM">
    <span class="nav-mark">P</span>
    <span class="nav-title">PLIALU</span>
  </a>
  <ul class="nav-links">
    <li><a class="nav-btn" href="page-a.html">Page A</a></li>
    <li><a class="nav-btn nav-btn--active" href="page-b.html">Page B</a></li>
  </ul>
</nav>
```

Variante hub historique (logo non-cliquable, `CRM PLIALU`) — laissée pour
référence, **plus utilisée** depuis que le hub adopte la sidebar :

```html
<nav class="nav">
  <div class="nav-brand nav-brand--static" title="Hub CRM PLIALU">
    <span class="nav-mark">P</span>
    <span class="nav-title nav-title--hub">
      <span class="nav-title-prefix">CRM</span>PLIALU
    </span>
  </div>
</nav>
```

### `sidebar.css` — Sidebar (hub uniquement)

Sidebar permanente de 250 px utilisée par `index.html` à la racine. Les
modules conservent leur navbar horizontale (`navbar.css`).

```html
<aside class="sidebar">
  <div class="sidebar-header">
    <span class="sidebar-mark">P</span>
    <span class="sidebar-title">
      <span class="sidebar-title-prefix">CRM</span>PLIALU
    </span>
  </div>

  <nav class="sidebar-section">
    <div class="sidebar-section-label">Outils</div>
    <ul class="sidebar-links">
      <li><a class="sidebar-link" href="…">
        <span class="sidebar-link-icon">🧮</span>Calculette
      </a></li>
      <!-- … -->
    </ul>
  </nav>

  <div class="sidebar-section">
    <div class="sidebar-section-label">À venir</div>
    <ul class="sidebar-links">
      <li><span class="sidebar-link sidebar-link--placeholder">
        <span class="sidebar-link-icon">+</span>Module à venir
      </span></li>
    </ul>
  </div>

  <div class="sidebar-footer">© PLIALU — Outils internes</div>
</aside>
```

Layout côté page :

```css
body { display: flex; min-height: 100vh; }
main { flex: 1; min-width: 0; }
```

Variantes utiles :

- `.sidebar-link--active` : item courant (fond accent, texte brand) — non
  utilisé sur le hub car il n'y a pas d'item correspondant à la page
  d'accueil dans la liste des outils.
- `.sidebar-link--placeholder` : emplacement réservé en pointillés,
  non-cliquable (`pointer-events: none`, opacity 0.5).

Responsive : sous **900px** la sidebar bascule en barre horizontale
au-dessus du `main` (footer + section labels masqués, liens en pillules).
Aucun JS requis.

### `buttons.css` — Boutons

Pattern double-classe : `.btn` (base) + variante.

```html
<button class="btn btn-primary">Action principale</button>
<button class="btn btn-secondary">Action secondaire</button>
<button class="btn btn-danger btn-sm">Supprimer</button>
<button class="btn btn-reset">Réinitialiser</button>
<a class="btn btn-primary btn-lg" href="…">Lien CTA</a>
```

Variantes : `.btn-primary` (jaune accent), `.btn-secondary` (fond clair, bordure), `.btn-danger` (fond rouge clair), `.btn-reset` (neutre, hover rouge).
Tailles : `.btn-sm`, `.btn-lg`, `.btn-icon`.

### `card.css` — Card

Card simple :

```html
<div class="card">
  <h3 class="card-title">Titre uppercase</h3>
  <p>Contenu…</p>
</div>

<div class="card card-active">
  <!-- bordure accent pour mise en avant -->
</div>
```

Card riche (tile cliquable, grille de modules) — utilisée par le hub et le
dashboard de la calculette :

```html
<a class="card card--rich" href="…">
  <span class="card-arrow" aria-hidden="true">→</span>
  <div class="card-icon">🧮</div>
  <h3>Titre du module</h3>
  <p>Description courte.</p>
  <ul class="card-tags">
    <li class="card-tag">Tag</li>
    <li class="card-tag">Tag</li>
  </ul>
</a>
```

`.card--rich` ajoute un effet de hover (lift + barre accent qui apparaît en
bas) ; `.card-arrow` glisse vers la droite au survol ; `.card-tag` est une
pillule au fond `--bg-muted`.

### `form.css` — Formulaires

Style global appliqué à `<input>`, `<select>`, `<textarea>` et `<label>`. Pas de classe à ajouter, le markup standard suffit :

```html
<label for="ex">Mon champ</label>
<input id="ex" type="text" placeholder="…">
```

---

## Conventions

### Chemins relatifs

| Page | Chemin vers `shared/` |
|---|---|
| `index.html` (hub, racine) | `shared/…` |
| `modules/<nom>/<page>.html` (profondeur 2) | `../../shared/…` |

### Ordre de chargement des `<link>`

```html
<link rel="stylesheet" href="…/shared/tokens.css">          <!-- 1. tokens -->
<link rel="stylesheet" href="…/shared/theme-dark.css">      <!-- 2. (optionnel) thème -->
<link rel="stylesheet" href="…/shared/components/navbar.css"> <!-- 3. composants -->
<link rel="stylesheet" href="…/shared/components/buttons.css">
<link rel="stylesheet" href="…/shared/components/card.css">
<link rel="stylesheet" href="…/shared/components/form.css">
<style>
  /* règles propres à la page, en dernier */
</style>
```

Le `<style>` inline arrive après les `<link>` : ses règles peuvent surcharger les composants partagés pour des cas vraiment spécifiques à la page (ex. styles d'un canvas, d'un tableau métier).

### Règle absolue dans `shared/components/`

> **Aucune valeur en dur (hex, px) dans les fichiers `shared/components/*.css`. Toujours via `var(--token)`.**

Si un composant a besoin d'une dimension non couverte par un token global (ex. taille du logo 34×34), elle est déclarée comme **propriété CSS scopée locale** sur le composant, avec préfixe `--_` :

```css
.nav {
  --_logo-mark-size: 34px;
}
.nav-mark {
  width: var(--_logo-mark-size);
  height: var(--_logo-mark-size);
}
```

Cela permet de garder ces valeurs « privées » au composant, hors du jeu de tokens globaux.

### Naming

- Tokens globaux : `--<catégorie>-<rôle>` (ex. `--brand-900`, `--text-primary`).
- Variables locales scopées : `--_<rôle>` (préfixe underscore).
- Classes : kebab-case ; modificateurs en BEM léger (`--`) pour les variantes (`.nav-brand--static`, `.nav-btn--active`).
- Types de composants : un fichier par concept (`navbar.css`, pas `nav.css` ni `header.css`).

---

## Ajouter un nouveau composant

1. Créer `shared/components/<nom>.css`.
2. N'utiliser que des `var(--token)` ; pour toute valeur non couverte, déclarer une propriété locale scopée `--_*`.
3. Documenter le markup attendu en haut du fichier (commentaire CSS).
4. Ajouter une section dans `shared/preview.html` montrant les variantes principales.
5. Inclure le fichier dans les pages cibles via `<link>` (cf. ordre ci-dessus).
6. Mettre à jour ce README et la table des composants.

## Ajouter un nouveau thème

1. Créer `shared/theme-<nom>.css`.
2. Surcharger uniquement les tokens qui changent dans ce thème (typiquement les surfaces et le texte). Conserver les noms de tokens — la même variable, valeur différente.
3. Charger après `tokens.css` dans les pages concernées.

## Aperçu visuel

`shared/preview.html` montre les composants dans plusieurs contextes (clair, sombre, hub). Ouvrir le fichier dans un navigateur (`file://` accepté) pour vérifier qu'un changement de token ou de composant ne casse rien visuellement avant de toucher aux pages.
