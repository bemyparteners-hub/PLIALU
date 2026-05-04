# STYLE-AUDIT — Inventaire CSS du CRM PLIALU

> Audit visuel **en lecture seule** des CSS inline des 7 pages du dépôt.
> Date : 2026-05-04. Aucun fichier n'a été modifié hormis ce rapport.

Pages couvertes :

| Code | Fichier | Lignes CSS (≈) |
|---|---|---|
| **HUB** | `index.html` (racine) | ~95 |
| **CAL.idx** | `modules/calculette/index.html` | ~190 |
| **CAL.calc** | `modules/calculette/calcul.html` | ~70 |
| **CAL.dev** | `modules/calculette/devis.html` | ~95 |
| **CAL.des** | `modules/calculette/dessinateur.html` | ~85 |
| **CFG** | `modules/configurateur/index.html` | ~115 |
| **MAX** | `modules/maxcut/index.html` | ~210 |

---

## 1. Palette de couleurs

### 1.1 Vue agrégée — toutes pages confondues

**Bleu marine PLIALU (couleur d'identité)**

| Hex | Usages | Pages |
|---|---|---|
| `#0d2933` | fond navbar, fond hero, texte principal sur clair, fond bouton actif, bordures actives | HUB · CAL.idx · CAL.calc · CAL.dev · CAL.des · CFG · MAX (`--bg-main`) |
| `#1a2e38` | texte principal corps | CAL.calc · CAL.dev · CAL.des · CFG · HUB |
| `#1a2e35` | texte principal corps | **CAL.idx uniquement** |
| `#1a3d4a` | fond secondaire (table head, panneau) | MAX (`--bg-secondary`) |
| `#0a1f28` | fond tertiaire (header MAXCUT, tracks scrollbar) | MAX (`--bg-tertiary`) |

→ **Drift sur le texte corps** : `#1a2e38` partout sauf `#1a2e35` dans `CAL.idx`. Différence de 1 chiffre hex (3 → presque imperceptible) — manifestement involontaire.

**Jaune citron PLIALU (accent)**

| Hex | Usages | Pages |
|---|---|---|
| `#e8fc69` | accent primaire (bouton actif, texte sur fond foncé, pastille logo, bordure de carte active) | toutes |
| `#d4f040` | hover du bouton primaire jaune | CAL.calc · CAL.dev · CAL.des · CFG |
| `#d4e85a` | hover du bouton primaire jaune | **CAL.idx** |
| `#d4e85f` | hover du bouton primaire jaune | **MAX** |
| `#cbff00` | bordure d'un `.result-box.has-value` | **CFG uniquement** |

→ **3 hovers différents pour le même bouton jaune**. `#cbff00` est un quatrième jaune utilisé une seule fois.

**Fond page (clair)**

| Hex | Usages | Pages |
|---|---|---|
| `#f0f4f8` | body background | HUB · CAL.calc · CAL.dev · CAL.des · CFG (et `#f0f4f8` en hover de zone d'upload, fond toolbar dessinateur) |
| `#f4f6f8` | body background | **CAL.idx uniquement** |
| `#f8fafc` | fond de bouton non-actif, fond input table, bg tag, fond saved-item | toutes pages claires |
| `#f8fafb` | hover tool-btn | **CAL.des uniquement** (drift d'1 caractère vs `#f8fafc`) |
| `#fafbfc` | fond saved-item & iso-wrap | CAL.des · CFG |
| `#f0f4f5` | fond .tag (calculette dashboard) | **CAL.idx uniquement** (drift vs `#f8fafc`) |
| `#f0f8fa` | fond `.pdf-item` | **CAL.dev uniquement** |

**Gris texte secondaire**

| Hex | Usages | Pages |
|---|---|---|
| `#5b6c75` | texte description (lead, card.p) | HUB |
| `#5a7a85` | texte description (module-card p, section-title p) | **CAL.idx** |
| `#6b7a80` | label uppercase, texte secondaire formulaires | CAL.calc · CAL.dev · CAL.des · CFG · CAL.idx (footer ?) |
| `#7a8b94` | footer | HUB |
| `#9aa8af` | placeholder card | HUB |
| `#8fa8b0` | `--text-secondary` | MAX |
| `#a0bcc4` | nav-btn idle, totaux label | CAL.calc · CAL.dev · CAL.des · CFG |
| `#4a6572` | mo-title, gamme svg stroke | CAL.calc · CFG |

→ **5 nuances de gris pour un même rôle** (texte secondaire). À fusionner.

**Bordures grises**

| Hex | Usages |
|---|---|
| `#e2e8f0` | bordure card, bordure result-box (HUB, CAL.idx, CAL.calc, CAL.dev, CAL.des, CFG) |
| `#dde3e8` | bordure input, btn secondaire, swatch (CAL.calc · CAL.dev · CAL.des · CFG) |
| `#c8d6db` | bordure upload-zone (**CAL.dev**) |
| `#c0d0d5` | flèche de carte module (**CAL.idx**) |
| `#cbd6dc` | bordure carte placeholder (**HUB**) |

→ `#dde3e8` et `#e2e8f0` sont quasi-identiques visuellement.

**Statuts (succès / alerte / danger)**

| Couleur | Hex | Pages | Note |
|---|---|---|---|
| Succès fond | `#dcfce7` | CAL.calc · CAL.dev · CFG | OK |
| Succès bordure | `#86efac` | CAL.calc · CFG | |
| Succès texte | `#166534` | CAL.calc · CAL.dev · CFG | |
| Succès alt fond | `#e6f9ee` | **CAL.des uniquement** | drift |
| Succès alt texte | `#1a7a42` | **CAL.des uniquement** | drift |
| Succès vert | `#4caf82` | **MAX** (`--success`) | thème dark |
| Alerte fond | `#fef3c7` | CAL.calc | |
| Alerte bordure | `#fcd34d` | CAL.calc | |
| Alerte texte | `#92400e` | CAL.calc | |
| Alerte orange | `#f0a500` | **MAX** (`--warning`) | thème dark |
| Danger fond | `#fee2e2` | CAL.dev (btn-del, pdf-remove) | |
| Danger texte | `#991b1b` | CAL.dev (btn-del) | |
| Danger contour | `#fca5a5` | CAL.dev (btn-del:hover) | |
| Danger texte | `#d9534f` | CAL.calc · CAL.des · CFG | **2e rouge utilisé pour la même intention** |
| Danger fond | `#c62828` | CAL.des (`#angleResult .ar-val`) | **3e rouge** |
| Danger | `#e05555` | **MAX** (`--danger`) | |

→ **5 rouges différents** pour exprimer "danger" (`#991b1b`, `#fca5a5`, `#d9534f`, `#c62828`, `#e05555`). À unifier.

**Bleu MO (thème "matière" / "transport" / "marge" dans calcul.html)**

| Hex | Usage |
|---|---|
| `#dbeafe` / `#93c5fd` / `#1e3a8a` | coef-mat (bleu) — **CAL.calc uniquement** |
| `#fef3c7` / `#fcd34d` / `#92400e` | coef-transport (jaune ambré) — **CAL.calc uniquement** |
| `#dcfce7` / `#86efac` / `#14532d` | coef-marge (vert) — **CAL.calc uniquement** |
| `#1e40af` / `#fff` | mat-btn actif — **CAL.calc uniquement** |

→ Palette catégorielle locale, propre à `calcul.html`, isolée du reste — OK telle quelle.

**Couleurs RGBA récurrentes**

| Valeur | Usage | Pages |
|---|---|---|
| `rgba(13,41,51,0.07)` à `rgba(13,41,51,0.13)` | shadow card | toutes pages claires |
| `rgba(13,41,51,0.82)` à `rgba(13,41,51,0.88)` | overlay save indicator, HUD | CAL.calc · CAL.dev · CAL.des · CFG |
| `rgba(232,252,105,0.1)` à `rgba(232,252,105,0.4)` | glow accent | CAL.idx · MAX |
| `rgba(255,255,255,0.3)` à `rgba(255,255,255,0.75)` | texte/bordure sur fond foncé | CAL.idx · MAX |
| `rgba(143,168,176,…)` | bordures dark theme | MAX uniquement |

### 1.2 Synthèse couleurs page par page

| Page | Brand | Accent | Fond page | Texte corps | Notes |
|---|---|---|---|---|---|
| HUB | #0d2933 | #e8fc69 | #f0f4f8 | #1a2e38 | Référence neutre |
| CAL.idx | #0d2933 | #e8fc69 (hover #d4e85a) | **#f4f6f8** ⚠ | **#1a2e35** ⚠ | 2 drifts vs HUB |
| CAL.calc | #0d2933 | #e8fc69 (hover #d4f040) | #f0f4f8 | #1a2e38 | OK |
| CAL.dev | #0d2933 | #e8fc69 (hover #d4f040) | #f0f4f8 | #1a2e38 | OK |
| CAL.des | #0d2933 | #e8fc69 (filter brightness) | #f0f4f8 | #1a2e38 | rouges multiples |
| CFG | #0d2933 | #e8fc69 (hover #d4f040) | #f0f4f8 | #1a2e38 | un `#cbff00` parasite |
| MAX | #0d2933 (`--bg-main`) | #e8fc69 (hover #d4e85f) | **#0d2933** ⚠ thème inversé | `#f0f0f0` | seule page en dark mode |

---

## 2. Typographie

### 2.1 Font-family

- **Toutes les pages** : `'Segoe UI', sans-serif` ou `'Segoe UI', system-ui, -apple-system, sans-serif` (HUB, MAX).
- Cohérence quasi-totale, à l'exception de la stack `system-ui, -apple-system` non répétée partout. Sans impact visuel sur Windows mais drift sur macOS/Linux.
- `'Courier New', monospace` ponctuel dans MAX (`.format-item span`, `.plan-format-badge`) — usage isolé, justifié.

### 2.2 Font-size — par rôle

| Rôle | HUB | CAL.idx | CAL.calc | CAL.dev | CAL.des | CFG | MAX |
|---|---|---|---|---|---|---|---|
| Titre header / hero h1 | 18px | 42px | — | — | — | 20px | `1.35rem` (≈21,6) |
| Titre carte / h2 | 16px | 26px (section), 20px (carte) | — | — | — | — | `1rem` (modal) |
| Card-title (uppercase tag) | — | — | 13px | 13px | 13px | **12px** ⚠ | `0.875rem` (14) |
| Sous-titre / lead | 14px | 17px (hero p), 15px (section) | — | — | — | 13px | `0.85rem` |
| Texte courant | 13px (card p) | 14px (module-card p) | 14px (input) | 14px (input) | 14px (input) | 14px (input) | `0.875rem`–`0.9rem` |
| Label (uppercase tag) | 12px (arrow) | 12px (badge) | 10px | 10px | 10px | 10px | `0.8rem` (12,8) |
| Tag pill | — | 11px | — | — | — | — | `0.72rem` |
| Footer/petit | 12px | 13px | — | — | 11px (date) | — | `0.72rem` |

→ **Card-title à 12px en CFG uniquement**, contre 13px partout ailleurs : drift visible.
→ MAX mélange `rem` / `px` selon les blocs ; les autres pages utilisent uniquement `px`. Choix d'unité non aligné.

### 2.3 Font-weight

| Rôle | Valeur(s) trouvée(s) |
|---|---|
| Logo / brand | `800` (HUB, CAL.idx, CAL.calc, CAL.dev, CAL.des, CFG), `800` (MAX `.logo-text`) |
| Titre uppercase tag (card-title) | `800` partout |
| Bouton primaire | `800` (CAL.calc, CAL.dev, CAL.des, CFG), `600` (MAX `.btn`) |
| Bouton secondaire | `700` (CAL.des, CFG), `600` (MAX) |
| Label uppercase | `700` partout |
| Texte courant | `400`–`600` (mix variable) |
| Pastille logo `<span>` | **`900`** (CAL.calc, CAL.dev, CAL.des, CFG, HUB header mark) |

→ Pas de drift majeur sur les graisses. La paire `800/700/600` est utilisée de façon quasi-cohérente.

---

## 3. Espacements

### 3.1 Padding récurrents

| Valeur | Contexte typique | Pages |
|---|---|---|
| `0 24px` / `0 16px` / `0 32px` | navbar horizontal | calcul/dev/des/cfg : 24px ; cal.idx : 32px ; HUB : 32px ; MAX : `1.5rem` (24) |
| `8px 18px` | nav-btn | CAL.calc · CAL.dev · CAL.des · CFG |
| `8px 16px` | navbar-links a | **CAL.idx** ⚠ (drift de 2px) |
| `22px 24px` | card | CAL.calc · CAL.dev · CAL.des |
| `18px 20px` | card | **CFG uniquement** (drift) |
| `22px 22px 20px` | card | **HUB uniquement** |
| `32px 28px` | module-card | **CAL.idx** |
| `1.25rem` (20px) | card | MAX |
| `10px 12px` / `9px 11px` | input padding | calc/dev/des : 10×12 ; CFG : 9×11 ⚠ |
| `12px 28px` / `12px 22px` / `12px 24px` | bouton primaire | CAL.calc : 12×28 ; CAL.des : 12×22 ; CFG : 12×24 ⚠ |
| `13px 28px` / `11px 22px` / `9px 20px` | autres boutons | CAL.dev btn-gen 13×28 ; CFG btn-secondary 11×20 / btn-reset 9×20 |

→ **6 paddings de bouton différents** pour des intentions identiques.

### 3.2 Margin récurrents

| Valeur | Contexte | Pages |
|---|---|---|
| `28px auto` / `24px auto` / `0 auto` | container .page | calc/dev/des : 28px ; CFG : 24px ; cal.idx : 0 |
| `48px 24px` / `48px 24px 64px` | main padding | HUB / CAL.idx |
| `16px` margin-bottom card | toutes pages claires |
| `14px` gap grid | calc/dev/des/cfg |
| `18px` gap | HUB grid cards |
| `20px` gap | CAL.idx modules-grid |

### 3.3 Border-radius

| Valeur | Usage |
|---|---|
| `6px` | nav-btn, swatch-petit, tool-btn, input table |
| `8px` | input, bouton, .btn, badge, tag (HUB) |
| `10px` | mo-bloc, info-band, upload-zone, iso-wrap |
| `12px` | card (toutes pages claires sauf HUB) |
| `14px` | card HUB |
| `20px` | tag pill, save-indicator, badge |
| `50%` | pastille logo, swatch couleur |
| `--radius` (8px) / `--radius-lg` (12px) | MAX uniquement |

→ HUB est la seule à avoir `14px` pour ses cartes. Les autres ont `12px`.

### 3.4 Hauteur de navbar

| Page | Hauteur |
|---|---|
| HUB | pas de navbar (header) |
| CAL.idx | **60px** ⚠ |
| CAL.calc | 52px |
| CAL.dev | 52px |
| CAL.des | 52px |
| CFG | 52px |
| MAX | **60px** ⚠ |

→ Deux hauteurs : 52 (suite calculette/configurateur) et 60 (CAL.idx + MAX). Visible quand on enchaîne les pages.

---

## 4. Composants partagés

### 4.1 Navbar — **4 variantes incompatibles**

| Variante | Pages | Classe principale | Hauteur | Logo | Items |
|---|---|---|---|---|---|
| A — `.nav` (52px) | CAL.calc, CAL.dev, CAL.des, CFG | `.nav` + `.nav-logo span` (pastille ronde 22px) + `.nav-btn` | 52 | « ⊙ PLIALU » | `.nav-btn`, idle gris `#a0bcc4` |
| B — `.navbar` (60px) | CAL.idx | `.navbar` + `.navbar-brand` (texte seul ●) + `.navbar-links a` | 60 | « ● PLIALU » | `.navbar-links a` idle blanc 75% |
| C — `<header>` (HUB) | HUB | `<header>` + `.mark` (carré arrondi 34px) | ~70 | « P » + h1 « CRM PLIALU » | aucun |
| D — `.app-header` (60px) | MAX | `.app-header` + `.logo-mark` (carré 36px svg) + `.logo-text` + `.logo-sub` | 60 | « PLIALU » + sous-titre | `.nav-tabs > .nav-tab` (tabs sous-jacents) |

→ **4 implémentations totalement différentes du même concept** "navbar du module + retour au hub". Le travail récent (lien `🏠 Hub`) a été dupliqué 5 fois sans factorisation.

### 4.2 Logo PLIALU — **5 implémentations différentes**

| Page | Markup | Pastille/Mark | Texte | Couleur fond pastille | Couleur texte |
|---|---|---|---|---|---|
| HUB | `<div class="mark">P</div>` + `<h1>CRM <span>PLIALU</span></h1>` | carré 34×34 r=8, **#e8fc69** | « CRM PLIALU » 18px, 800, uppercase | accent | white + accent |
| CAL.idx | `<div class="navbar-brand">● PLIALU</div>` | bullet ● *Unicode* | « ● PLIALU » 20px, 800 | (pas de fond) | accent |
| CAL.calc/dev/des/CFG | `<div class="nav-logo"><span>o</span> PLIALU</div>` | rond 22×22 50%, **#e8fc69** | « PLIALU » 17px, 800 | accent | accent |
| MAX | `<div class="logo-mark"><svg.../></div>` + `.logo-text` + `.logo-sub` | carré 36×36 r=6, **#e8fc69** + svg paths | « PLI**ALU** » 1.35rem (≈21,6) + sous-titre « Optimiseur de découpe » | accent | white + accent |

→ **Aucune harmonisation**. Mark : carré arrondi 34px / bullet Unicode / rond 22px / carré 36px svg. Texte : 17, 18, 20 px et 1.35rem. Le seul invariant est la couleur `#e8fc69`. C'est le composant le plus visiblement incohérent du dépôt.

### 4.3 Boutons

`.btn-primary` est défini dans **5 fichiers** avec des règles distinctes :

| Page | bg | color | padding | font-size | font-weight | border-radius | hover |
|---|---|---|---|---|---|---|---|
| CAL.idx | #e8fc69 | #0d2933 | 14px 28px | 15 | 800 | 8px | bg #d4e85a + translateY |
| CAL.calc | #e8fc69 | #0d2933 | 12px 28px | 15 | 800 | 8px | bg #d4f040 + translateY |
| CAL.des | #e8fc69 | #0d2933 | 12px 22px | 14 | 800 | 8px | filter brightness |
| CFG | #e8fc69 | #0d2933 | 12px 24px | 14 | 800 | 8px | bg #d4f040 + translateY |
| MAX | var(--accent) | var(--bg-tertiary) | 0.6rem 1.2rem (≈9,6×19) | 0.875rem (14) | 600 | var(--radius) (8) | bg #d4e85f |

→ Même intention, **5 implémentations différentes**. Tailles, hover, font-weight (600 vs 800).

`.btn-secondary` : présent dans CAL.des, CFG, MAX — 3 implémentations distinctes.

`.btn-reset` : CAL.calc + CFG → définitions identiques (factorisation déjà naturelle).

`.btn-add` / `.btn-gen` / `.btn-ligne` / `.btn-import` / `.btn-calc` / `.btn-del` / `.btn-danger` : multiplication de variantes locales (CAL.calc, CAL.dev). À catégoriser.

### 4.4 Card

| Page | bg | radius | padding | shadow | border |
|---|---|---|---|---|---|
| HUB | #fff | 14px | 22px 22px 20px | 0 8px 22px rgba(...) on hover | 1.5px solid #e2e8f0 |
| CAL.idx (`.module-card`) | #fff | 12px | 32px 28px | hover 0 12px 32px | 2px solid #e2e8f0 |
| CAL.calc/dev/des | #fff | 12px | 22px 24px | 0 1px 4px rgba(0,0,0,.07) | (aucune) |
| CFG | #fff | 12px | 18px 20px | 0 1px 4px | (aucune) |
| MAX | var(--bg-tertiary) | var(--radius-lg)=12 | 1.25rem (20) | (aucune) | 1px solid var(--border) |

→ 5 cards avec radius {14, 12, 12, 12, 12}, padding très variable, shadow ou border indifféremment.

### 4.5 Inputs / formulaires

| Page | padding | border | border-radius | focus border | font-size |
|---|---|---|---|---|---|
| CAL.calc | 10px 12px | 1.5px solid #dde3e8 | 8px | #0d2933 | 14px |
| CAL.dev | 10px 12px | 1.5px solid #dde3e8 | 8px | #0d2933 | 14px |
| CAL.des | 10px 12px | 1.5px solid #dde3e8 | 8px | #0d2933 | 14px |
| CFG | **9px 11px** ⚠ | 1.5px solid #dde3e8 | 8px | #0d2933 | 14px |
| MAX | 0.65rem 0.875rem | 1px solid var(--border) | var(--radius)=8 | var(--accent) | 0.9rem (14,4) |
| HUB | (pas de form) | | | | |
| CAL.idx | (pas de form) | | | | |

→ Calculette = 4 fichiers parfaitement alignés sauf CFG qui est légèrement plus petit (9 vs 10).

### 4.6 Tableaux

| Page | Header bg | Header text color | Row hover bg |
|---|---|---|---|
| CAL.dev `.devis-table` | `#0d2933` | `#e8fc69` | `#f8fafc` |
| MAX `.pieces-table` | `var(--bg-secondary)` | `var(--text-secondary)` | `rgba(...)` |

→ Règles complètement disjointes mais composent le même rôle.

### 4.7 Tags / badges

| Page | Markup | bg | color | padding | radius | font-size |
|---|---|---|---|---|---|---|
| CAL.idx | `.tag` | #f0f4f5 | #0d2933 | 4px 10px | 20px | 11px |
| MAX | `.tag` (générique + variantes `.tag-material`) | rgba(...) | var(--success) | 2px 8px | 20px | 0.72rem |

→ Même nom de classe (`.tag`), 2 visuels très différents.

---

## 5. Logo PLIALU — vérification rigoureuse

Détaillé en §4.2. À retenir :

- Pastille jaune **toujours `#e8fc69`** (un seul invariant).
- Forme : carré 34px (HUB), rond 22px (suite calculette), carré 36px svg (MAX), bullet ● Unicode (CAL.idx).
- Lettre dans la pastille : « P » (HUB), « o » (CAL.calc/dev/des/CFG, lettre minuscule arbitraire), aucune (CAL.idx, MAX).
- Texte « PLIALU » : 17px (suite calculette), 18px (HUB), 20px (CAL.idx), ~21,6px (MAX).
- Sous-titre : seul MAX en a un (« Optimiseur de découpe »).
- Couleur du texte : tout `#e8fc69` (suite calculette/CAL.idx) sauf HUB et MAX qui le coupent (« CRM » et « PLI » en blanc, « PLIALU »/« ALU » en accent).

→ **Aucune des 4 implémentations ne peut servir de référence sans normalisation préalable.** Le drift est total.

---

## 6. Recommandations

### 6.1 Variables CSS prioritaires (à définir dans un futur `shared/tokens.css` ou `:root` partagé)

Top 10 par fréquence d'apparition et par gain de cohérence :

| # | Token | Valeur cible suggérée | Remplace |
|---|---|---|---|
| 1 | `--brand-900` | `#0d2933` | textuellement OK partout (1 seul hex) |
| 2 | `--brand-700` | `#1a2e38` | unifie `#1a2e35`/`#1a2e38` (drift CAL.idx) |
| 3 | `--accent` | `#e8fc69` | déjà unique |
| 4 | `--accent-hover` | (à choisir : `#d4f040` est majoritaire 4/5) | unifie `#d4e85a`/`#d4f040`/`#d4e85f` |
| 5 | `--bg-app` | `#f0f4f8` | unifie avec `#f4f6f8` (drift CAL.idx) |
| 6 | `--bg-elevated` | `#ffffff` | déjà unique |
| 7 | `--bg-muted` | `#f8fafc` | unifie `#f8fafc`/`#f8fafb`/`#fafbfc`/`#f0f4f5` |
| 8 | `--text-muted` | (à choisir : `#6b7a80` est majoritaire) | unifie `#5a7a85`/`#5b6c75`/`#6b7a80`/`#7a8b94` |
| 9 | `--border-soft` | `#e2e8f0` | unifie `#dde3e8`/`#e2e8f0` |
| 10 | `--danger` | (à choisir) | unifie `#991b1b`/`#d9534f`/`#c62828`/`#e05555`/`#fca5a5` |

Tokens d'espacement (deuxième niveau de priorité) :

- `--space-1` = 4 / `--space-2` = 8 / `--space-3` = 12 / `--space-4` = 16 / `--space-5` = 20 / `--space-6` = 24 / `--space-8` = 32
- `--radius-sm` = 6 / `--radius` = 8 / `--radius-lg` = 12
- `--nav-height` = (à arbitrer : 52 ou 60)

Tokens typographie :

- `--font-sans` = `'Segoe UI', system-ui, -apple-system, sans-serif`
- `--text-xs/sm/base/lg/xl` = 11/13/14/16/18 (à confirmer ; ces 5 valeurs couvrent ~95 % des cas)

### 6.2 Composants à extraire dans `shared/` par ordre de gain (ROI)

| Rang | Composant | Gain | Urgence |
|---|---|---|---|
| 1 | **Navbar + logo** | 4 implémentations distinctes du même rôle, ~110 lignes CSS dupliquées sur 5 fichiers + 1 logo MAX désaligné | **haute** — c'est le composant le plus visible |
| 2 | **Bouton `.btn-primary` / `.btn-secondary` / `.btn-reset`** | 5 versions de btn-primary, 3 de btn-secondary | haute |
| 3 | **Card** | 5 variantes (HUB, CAL.idx, calculette, CFG, MAX) — au moins 3 à fusionner sur le thème clair | moyenne |
| 4 | **Input + label uppercase** | 4 fichiers calculette quasi-identiques (CFG drift de 1px) | moyenne — drift faible |
| 5 | **Table** | CAL.dev + MAX seulement, thèmes différents → 2 templates (clair/sombre) | basse |
| 6 | **Tag pill** | 2 implémentations (CAL.idx clair, MAX sombre) | basse — peu utilisé |

### 6.3 « Fausses incohérences » (vraisemblablement des bugs visuels)

Ces écarts ne semblent pas intentionnels — ils trahissent un copier-coller sans uniformisation :

1. **CAL.idx fond `#f4f6f8`** vs `#f0f4f8` partout ailleurs — drift d'un caractère hex.
2. **CAL.idx texte corps `#1a2e35`** vs `#1a2e38` partout ailleurs — drift d'un chiffre hex.
3. **CAL.idx hauteur navbar 60px**, le reste de la suite calculette à 52px → bord supérieur qui « saute » entre `index.html` et `calcul.html`.
4. **CAL.idx hover bouton `#d4e85a`** vs `#d4f040` majoritaire (et MAX `#d4e85f`).
5. **CFG card-title à 12px** vs 13px partout ailleurs dans la suite calculette.
6. **CFG input padding `9px 11px`** vs `10px 12px` partout ailleurs dans la suite.
7. **CFG card padding `18px 20px`** vs `22px 24px` partout ailleurs dans la suite.
8. **CAL.des `#f8fafb`** (au lieu de `#f8fafc`) — drift d'un caractère.
9. **CAL.des** introduit `#e6f9ee` / `#1a7a42` pour le succès — alors que le reste utilise `#dcfce7` / `#166534`.
10. **HUB radius card 14px** vs 12px sur toutes les autres pages claires.
11. **CFG `.result-box.has-value` borde en `#cbff00`** — quatrième jaune utilisé une seule fois, manifestement une faute de frappe (`#e8fc69` ou `#cbef00` ?).
12. **5 nuances de rouge danger** (`#991b1b`, `#fca5a5`, `#d9534f`, `#c62828`, `#e05555`) là où une seule suffit.

Items 1-2-3 sont les plus criants : ils touchent `modules/calculette/index.html`, qui sert d'« entrée » du module mais n'a pas exactement le même look que ses pages-soeurs.

### 6.4 Ce qui est déjà cohérent (à préserver)

- `'Segoe UI'` partout (un drift mineur sur la stack système).
- `#e8fc69` strictement identique partout pour l'accent.
- `#0d2933` strictement identique partout pour le brand sombre.
- Border-radius `8px` pour les boutons : invariant.
- Reset `box-sizing: border-box` + `margin/padding: 0` : présent sur toutes les pages.
- MAX étant le seul thème sombre, il **doit** rester séparé — c'est un module à part. Mais il devrait utiliser les **mêmes tokens nommés** que le reste, juste avec des valeurs `:root` différentes (pattern « thème »).

---

**En attente de validation avant toute action.**
