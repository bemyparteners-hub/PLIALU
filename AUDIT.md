# AUDIT — Dépôt PLIALU

> ⚠ **HISTORICAL SNAPSHOT — état du dépôt avant refactor.**
> Ce document décrit l'état *initial* du dépôt (3 zips, doublons,
> drift, code mort). Conserve la trace de l'audit qui a déclenché
> les phases de restructuration et de design system. Pour l'état
> courant, voir `LINK-AUDIT.md` et `COHERENCE-AUDIT.md`.
>
> Phase 1 : audit lecture seule. Aucun fichier du dépôt n'a été modifié hormis ce rapport.
> Date d'audit : 2026-05-04 — Branche : `claude/audit-repository-ALinL`.

---

## 0. TL;DR

Le dépôt **n'est pas un dépôt de code** : il contient 3 archives ZIP non-extraites
(`MAXCUT-main.zip`, `calculette-main (1).zip`, `config-main.zip`) et un `README.md`
de 8 octets (`# PLIALU`). Tout le code utile est encapsulé dans les zips. Le contenu
réel doit être extrait, classé et structuré.

Trois sous-projets distincts cohabitent :

| Sous-projet | Rôle | État | Référencé ailleurs ? |
|---|---|---|---|
| `calculette-main/` | Suite calculette + devis + dessinateur + configurateur PLIALU | Actif (CLAUDE.md détaillé) | — |
| `MAXCUT-main/` | Optimiseur de découpe aluminium (one-shot HTML) | Standalone, fonctionnel | Non lié à calculette |
| `config-main/` | Prototype de configurateur de pliage (script Python générant un HTML) | Prototype unique | Non lié |

Problèmes structurels majeurs :
- 200+ images mal nommées (mojibake `#U00e0`, espaces, casse mixte `.PNG`/`.png`)
- Doublons de configurateur (`configurateur.html` vs `nouvelle-page.html` vs `config-v2.html`)
- 67 PNG à la racine **non référencés** par aucun code actif
- Bibliothèque tierce **vendorée minifiée** (`easytest.js` 1,1 Mo) provenant manifestement d'un build externe
- PII commerciaux (noms, téléphones, emails) en clair dans `devis.html`
- `config-main/index.html` est en réalité un script Python avec extension `.html`

---

## 1. Inventaire

### 1.1 Racine du dépôt

```
/home/user/PLIALU
├── .git/
├── README.md                  8 B     2026-05-04   (juste « # PLIALU »)
├── MAXCUT-main.zip           20 K     2026-05-04   contenu zippé du 2026-03-18
├── calculette-main (1).zip   19 M     2026-05-04   contenu zippé du 2026-04-23
└── config-main.zip            6 K     2026-05-04   contenu zippé du 2026-03-23
```

Historique git : 2 commits (`Initial commit` + `Add files via upload`). Pas de
`.gitignore`, pas de `.github/`, pas de `LICENSE`.

### 1.2 `MAXCUT-main.zip` (1 fichier utile)

```
MAXCUT-main/
└── index.html        78 K   2026-03-18   « PLIALU – Optimiseur de découpe aluminium »
```

Application HTML/CSS/JS vanilla autonome (1705 lignes), CDN : jsPDF 2.5.1 + html2canvas 1.4.1.

### 1.3 `config-main.zip` (3 fichiers)

```
config-main/
├── README.md         8 B     « # config »
└── index.html       20 K     SCRIPT PYTHON déguisé en .html
```

`config-main/index.html` commence par `from pathlib import Path` puis stocke un
gros document HTML dans une variable `html = r"""..."""` et écrit le fichier dans
`/mnt/data/fold_configurator.html`. C'est manifestement un export brut depuis un
notebook (extension trompeuse).

### 1.4 `calculette-main (1).zip` (290 fichiers)

#### 1.4.1 Code applicatif (HTML/JS/CSS)

| Fichier | Taille | Rôle | Référencé par navbar ? |
|---|---|---|---|
| `index.html` | 11 K | Page d'accueil / hub | ✅ (auto + nav) |
| `calcul.html` | 27 K | Calculette de prix | ✅ |
| `devis.html` | 36 K | Générateur de devis PDF | ✅ |
| `dessinateur.html` | 41 K | Outil de dessin canvas | ✅ |
| `configurateur.html` | 51 K | Configurateur (auto-suffisant, 11 SVG, GAMMES inline) | ✅ |
| `config-v2.html` | 31 K | « Configurateur V2 » Bootstrap 4 + jQuery + easytest.js | ❌ orphelin |
| `nouvelle-page.html` | 40 K | Configurateur prototype basé sur plialu-data/materials/geometry | ❌ orphelin |
| `easytest.js` | **1,1 Mo** | Bundle minifié `configurator.a149130c.js` (Hammer.js, ZRender, BootstrapVue…) | uniquement `config-v2.html` |
| `easytest2.css` | 85 K | Bundle CSS associé à `easytest.js` | uniquement `config-v2.html` |
| `geometry.js` | 1,3 K | `AluGeom` — utilitaires polyligne/bbox | uniquement `nouvelle-page.html` |
| `plialu-data.js` | 35 K | 275 articles × 15 familles, mapping `img:` | uniquement `nouvelle-page.html` |
| `plialu-materials.js` | 117 K | Tables matières/RAL/épaisseurs | uniquement `nouvelle-page.html` |

#### 1.4.2 Documentation & métadonnées

| Fichier | Taille | Statut |
|---|---|---|
| `README.md` | 12 B | Quasi vide (`# calculette`) |
| `CLAUDE.md` | 6,5 K | Documentation projet complète et à jour |
| `.claude/skills/*.md` (10 fichiers) | 12,7 K | Slash-commands custom (accessibility, bug-fix, code-review, documentation, mobile, performance, refactor, security, seo, testing) |

#### 1.4.3 Images

| Emplacement | Nb | Total | Référencées ? |
|---|---|---|---|
| Racine `calculette-main/*.PNG \|*.png` | 67 | ≈ 4,5 Mo | **0** par le code actif (uniquement vers `nouvelle-page.html` indirect via `plialu-data.js`) |
| `img/pieces/*.PNG` | 198 | ≈ 17 Mo | 153 sur 196 références de `plialu-data.js` matchent un fichier |
| `img/pieces/README.md` | 977 B | — | Définit la convention de nommage **slug snake_case** non appliquée |
| `img/pieces/.gitkeep` | 0 B | — | OK |

Cas particuliers :
- 2 fichiers présents à la racine **et** dans `img/pieces/` : `Capture Omega Laque Ext.PNG`,
  `Capture Omega Laque Int.PNG` (doublons binaires probables).
- 43 références dans `plialu-data.js` ne pointent vers aucun fichier (différences
  d'encodage entre les vrais caractères accentués — `é`, `à` — utilisés dans le JS
  et la version mojibake `#U00e9`, `#U00e0` présente sur le disque).
- Tous les noms de fichiers utilisent des espaces, ce qui complique URL-encoding,
  scripts shell et déploiement web.

---

## 2. Classification fichier par fichier

Légende : ✅ garder · 🟡 déplacer · 🟠 renommer · 🔵 fusionner · 🔴 supprimer

### 2.1 Racine du dépôt

| Fichier | Action |
|---|---|
| `README.md` (8 B) | 🟠 réécrire (vide actuellement) |
| `MAXCUT-main.zip` | 🔴 supprimer **après** extraction et migration de son contenu |
| `calculette-main (1).zip` | 🔴 supprimer **après** extraction et migration |
| `config-main.zip` | 🔴 supprimer **après** extraction et migration |

### 2.2 Contenu de `calculette-main/`

#### Code applicatif

| Fichier | Action | Justification |
|---|---|---|
| `index.html` | ✅ garder, 🟡 → racine | Hub principal, lié partout |
| `calcul.html` | ✅ garder, 🟡 → racine | Lié, fonctionnel |
| `devis.html` | ✅ garder, 🟡 → racine | Lié, fonctionnel ; ⚠️ contient PII en clair |
| `dessinateur.html` | ✅ garder, 🟡 → racine | Lié, fonctionnel |
| `configurateur.html` | ✅ garder, 🟡 → racine | Lié depuis navbar, version active |
| `config-v2.html` | 🔴 supprimer | Orphelin, charge un bundle 1,1 Mo non maintenable |
| `nouvelle-page.html` | 🟠 renommer en `configurateur-v2.html` ou 🔴 supprimer | Orphelin ; doublon fonctionnel de `configurateur.html` mais utilise plialu-data/materials. **Décision attendue**. |
| `geometry.js` | 🔵 dépend de `nouvelle-page.html` | À garder uniquement si `nouvelle-page.html` est conservé |
| `plialu-data.js` | 🔵 idem | 275 articles — donnée de valeur, mais inutile si on ne garde pas la page consommatrice |
| `plialu-materials.js` | 🔵 idem | 117 K de tables matière |
| `easytest.js` (1,1 Mo) | 🔴 supprimer | Bundle minifié vendoré, sans source map ni `package.json` |
| `easytest2.css` (85 K) | 🔴 supprimer | Idem |

#### Documentation

| Fichier | Action |
|---|---|
| `CLAUDE.md` | ✅ garder, 🟡 → racine |
| `README.md` (12 B) | 🔴 supprimer (sera remplacé par le nouveau README racine) |
| `.claude/skills/*.md` (10 fichiers) | ✅ garder, 🟡 → racine `.claude/skills/` |

#### Images racine `calculette-main/*.PNG`

| Fichier | Action |
|---|---|
| 65 PNG racine non référencés (`Angle Corn Ext.PNG`, `CJEXTangle95.PNG`, `Capture A D#U00e9bit.PNG`, `Capture Angle*`, `Capture Corn*`, `Capture Tableau*`, `Capture U *`, `Capture Z *`, `Capture Plat.PNG`, `Capture Linteau*`, `Capture LintSpec-1.PNG`, `Capture Habillage Perfos*`, `Capture Divers.PNG`, `Capture Double Epingle.PNG`, `Capture Epingle.PNG`, `Capture Omega Brut.PNG`, `Tube.PNG`, `EclGe.png`, `G#U00e9n#U00e9ralGeExtrude.png`, `GeExtrude.png`, `AngleRentrantGeExtrude.png`, `AngleSortantGeExtrude.png`, `Bouchon Ge Droite.png`, `Bouchon Ge Gauche.png`) | 🟡 → `assets/legacy/` puis 🔴 candidate à suppression après revue métier (potentiellement à intégrer dans `img/pieces/` selon la convention) |
| `Capture Omega Laque Ext.PNG`, `Capture Omega Laque Int.PNG` | 🔵 doublons de `img/pieces/` — supprimer copie racine |

#### Images `img/pieces/`

| Fichier | Action |
|---|---|
| 198 PNG | 🟡 → `assets/pieces/` + 🟠 normaliser le nommage selon le slug défini par le README (`lowercase`, `_`, sans accents) **et** mettre à jour `plialu-data.js` en parallèle |
| `img/pieces/README.md` | ✅ garder + 🟡 → `assets/pieces/README.md` |
| `img/pieces/.gitkeep` | ✅ garder |

### 2.3 Contenu de `MAXCUT-main/`

| Fichier | Action |
|---|---|
| `index.html` | ✅ garder, 🟠 renommer en `maxcut.html`, 🟡 → racine **OU** garder dans sous-dossier `maxcut/` |

### 2.4 Contenu de `config-main/`

| Fichier | Action |
|---|---|
| `index.html` (script Python) | 🟠 renommer en `tools/fold_configurator_export.py` 🟡 + extraire le HTML généré dans un fichier statique distinct si encore utilisé, sinon 🔴 supprimer |
| `README.md` (8 B) | 🔴 supprimer |

---

## 3. Problèmes détectés

### 3.1 Structure du dépôt

- **R-01 (critique)** : le code est encapsulé dans des zips versionnés. Aucune
  diff utile possible, aucune CI possible, aucune navigation IDE possible.
  GitHub Pages ne peut pas servir le contenu en l'état.
- **R-02** : aucun `.gitignore` → risque d'inclure ultérieurement `.DS_Store`,
  `node_modules`, builds, secrets locaux.
- **R-03** : 3 sous-projets non liés (calculette / MAXCUT / config) sans
  délimitation explicite ni documentation racine.

### 3.2 Code mort / orphelin

- **D-01** : `config-v2.html` n'est lié par aucune navbar et tire un bundle
  vendoré de 1,2 Mo (`easytest.js` + `easytest2.css`). À supprimer ou réintégrer
  proprement.
- **D-02** : `nouvelle-page.html` n'est lié par aucune navbar mais constitue le
  seul consommateur de `plialu-data.js` (275 articles), `plialu-materials.js`
  (tables RAL) et `geometry.js`. Décision métier requise : finir l'intégration ou
  archiver.
- **D-03** : 65 PNG à la racine de `calculette-main/` ne sont référencés ni par
  les pages actives ni par `plialu-data.js`. Dette visuelle de 4,5 Mo.

### 3.3 Nommage / encoding

- **N-01** : noms de fichiers contenant des espaces et des séquences mojibake
  `#U00e9` (é), `#U00e0` (à) issues de la dé-zippification d'un archive Windows
  vers Linux. Cassent les URLs proprement encodées et empêchent un mapping
  fiable depuis `plialu-data.js`.
- **N-02** : extensions hétérogènes `.PNG` (majuscule) vs `.png` (minuscule)
  pour des fichiers du même type. Casse sur systèmes case-sensitive.
- **N-03** : `img/pieces/README.md` documente un slug `lowercase_underscore`
  qui n'est **pas appliqué** sur le disque. Convention écrite ≠ pratique.
- **N-04** : 43 entrées de `plialu-data.js` ne trouvent pas leur image (à cause
  de N-01).
- **N-05** : `config-main/index.html` n'est pas un fichier HTML mais un script
  Python.

### 3.4 Sécurité / confidentialité

- **S-01** (PII) : `devis.html` lignes 281-284 expose 4 collaborateurs
  (`Quentin MONTEIRO q.monteiro@plialu.fr`, `Jean-Pierre BAX jpbax@plialu.fr`,
  `Thibaut RONDET t.rondet@plialu.fr`, `Ghayth BENYOUCEF g.benyoucef@plialu.fr`)
  avec leurs téléphones mobiles. Acceptable pour un usage interne mais à
  documenter ; **incompatible** avec un dépôt public (le repo est sur GitHub).
- **S-02** : 15 usages de `innerHTML` dans les pages actives. À auditer pour XSS
  (les inputs proviennent du `localStorage` et de saisies utilisateur, ce qui
  reste local mais conserve un risque de stored-XSS d'un poste partagé).
- **S-03** : `easytest.js` est un bundle tiers minifié sans `LICENSE` ni
  `package.json` ni hash d'intégrité — provenance non auditable.

### 3.5 Conventions

- **C-01** : `README.md` racine vide (8 B) → ne décrit ni le projet, ni la
  structure, ni le déploiement.
- **C-02** : pas de licence, pas de fichier `LICENSE`.
- **C-03** : `CLAUDE.md` (à l'intérieur du zip) référence une structure cible
  (`/index.html /calcul.html /devis.html /dessinateur.html`) qui n'existe pas
  dans le dépôt — la documentation est en avance sur le code livré.

### 3.6 Doublons

- **DUP-01** : `Capture Omega Laque Ext.PNG` et `Capture Omega Laque Int.PNG`
  présents simultanément à `calculette-main/` racine et dans
  `calculette-main/img/pieces/`.
- **DUP-02** : 3 fichiers HTML « configurateur » coexistent
  (`configurateur.html`, `config-v2.html`, `nouvelle-page.html`) avec recouvrement
  fonctionnel.

---

## 4. Plan de rangement proposé

### 4.1 Arborescence cible

```
/                                  GitHub Pages root
├── README.md                      (réécrit ; structure + déploiement)
├── CLAUDE.md                      (déplacé depuis calculette-main/)
├── LICENSE                        (à créer ; MIT/proprio selon décision)
├── .gitignore                     (à créer)
├── index.html                     (hub PLIALU)
├── calcul.html
├── devis.html
├── dessinateur.html
├── configurateur.html
├── maxcut.html                    (depuis MAXCUT-main/index.html)
├── .claude/
│   └── skills/
│       ├── accessibility.md
│       ├── bug-fix.md
│       ├── code-review.md
│       ├── documentation.md
│       ├── mobile.md
│       ├── performance.md
│       ├── refactor.md
│       ├── security.md
│       ├── seo.md
│       └── testing.md
├── assets/
│   ├── pieces/                    (depuis img/pieces/, renommé en slug)
│   │   ├── README.md
│   │   ├── bv2plis.png …
│   │   └── (198 fichiers normalisés)
│   └── legacy/                    (PNG racine en attente de tri métier)
└── tools/
    └── fold_configurator_export.py   (script Python ex-config-main)
```

### 4.2 Décisions à valider (DÉPENDANT DU CHOIX)

> **Q1** — `nouvelle-page.html` + `plialu-data.js` + `plialu-materials.js` + `geometry.js` :
> - **Option A** : on les supprime tous (configurateur unique = `configurateur.html`).
> - **Option B** : on les conserve sous `experimental/` ou on intègre les data files
>   dans `configurateur.html`.
>
> Le plan ci-dessous est par défaut **A** (suppression) ; passer à B ajoute des
> moves au lieu des deletes.

> **Q2** — Les 65 PNG racines non référencés : suppression directe ou conservation
> sous `assets/legacy/` pendant 1 commit pour revue métier ?
> Le plan ci-dessous conserve via `assets/legacy/` puis suppression dans un commit
> séparé (réversible).

> **Q3** — `MAXCUT` : `maxcut.html` à la racine **ou** sous-dossier `maxcut/index.html` ?
> Le plan ci-dessous met à la racine pour rester aligné avec le pattern « une page = un fichier ».

> **Q4** — `config-main/` : le script Python est un export jetable. Conserver
> sous `tools/` ou supprimer tout simplement (aucune dépendance détectée) ?

### 4.3 Mapping `chemin actuel → chemin cible`

#### Extraction & landing initiaux

| Source | Cible |
|---|---|
| `MAXCUT-main.zip` (extrait) | `maxcut.html` (renommé) |
| `calculette-main (1).zip` (extrait) | (mappings ci-dessous) |
| `config-main.zip` (extrait) | `tools/fold_configurator_export.py` |

#### Pages HTML (calculette)

| De | Vers |
|---|---|
| `calculette-main/index.html` | `index.html` |
| `calculette-main/calcul.html` | `calcul.html` |
| `calculette-main/devis.html` | `devis.html` |
| `calculette-main/dessinateur.html` | `dessinateur.html` |
| `calculette-main/configurateur.html` | `configurateur.html` |
| `MAXCUT-main/index.html` | `maxcut.html` |

#### Documentation

| De | Vers |
|---|---|
| `calculette-main/CLAUDE.md` | `CLAUDE.md` |
| `calculette-main/.claude/skills/*.md` (×10) | `.claude/skills/*.md` |
| `calculette-main/README.md` | (supprimé) |
| `calculette-main/img/pieces/README.md` | `assets/pieces/README.md` |
| `MAXCUT-main/` (zip global) | (supprimé une fois `maxcut.html` extrait) |
| `config-main/README.md` | (supprimé) |

#### Images

| De | Vers |
|---|---|
| `calculette-main/img/pieces/<NomPiece>.PNG` | `assets/pieces/<slug>.png` (198 fichiers, slug calculé) |
| `calculette-main/img/pieces/.gitkeep` | `assets/pieces/.gitkeep` |
| `calculette-main/<NomPiece>.PNG` (65 fichiers non référencés) | `assets/legacy/<NomPiece>.PNG` *(en attente Q2)* |
| `calculette-main/Capture Omega Laque Ext.PNG` | (supprimé, doublon de `img/pieces/`) |
| `calculette-main/Capture Omega Laque Int.PNG` | (supprimé, doublon de `img/pieces/`) |

#### Suppressions (Option A pour Q1 + nettoyage zips)

| Fichier | Raison |
|---|---|
| `MAXCUT-main.zip` | extrait, transmigré |
| `calculette-main (1).zip` | extrait, transmigré |
| `config-main.zip` | extrait, transmigré |
| `calculette-main/config-v2.html` | orphelin, dépend d'un bundle non maintenable |
| `calculette-main/easytest.js` (1,1 Mo) | bundle vendoré orphelin |
| `calculette-main/easytest2.css` (85 K) | bundle vendoré orphelin |
| `calculette-main/nouvelle-page.html` | orphelin (Option A) |
| `calculette-main/plialu-data.js` | consommé uniquement par `nouvelle-page.html` (Option A) |
| `calculette-main/plialu-materials.js` | idem |
| `calculette-main/geometry.js` | idem |

#### Modifications de code requises post-déplacements

| Fichier | Modification |
|---|---|
| `index.html`, `calcul.html`, `devis.html`, `dessinateur.html`, `configurateur.html`, `maxcut.html` | Mettre à jour les liens d'`assets/` (aujourd'hui sans préfixe). Vérifier la nav inter-pages (déjà compatible une fois tous les fichiers à la racine). |
| `CLAUDE.md` | Mettre à jour la section « Structure du repo » pour inclure `configurateur.html`, `maxcut.html`, `assets/`, `.claude/skills/`. |
| `README.md` | Réécriture complète (vue d'ensemble + déploiement GH Pages + arborescence). |
| `.gitignore` | Créer : `*.zip`, `.DS_Store`, `Thumbs.db`, `node_modules/`, `dist/`, `.idea/`, `.vscode/`, `*.log`, `*.tmp`. |

### 4.4 Suite de commits proposée (phase 2)

1. `chore: extract calculette zip into repo root` (move bulk)
2. `chore: extract MAXCUT and config zips` (move bulk)
3. `chore: remove zip archives from repo`
4. `chore: drop orphan configurator V2 and easytest bundle` (3 deletes)
5. `chore: drop orphan nouvelle-page and plialu-data/materials/geometry` (Option A) **OU** `chore: archive nouvelle-page prototype under experimental/` (Option B)
6. `chore: deduplicate Capture Omega Laque {Ext,Int}.PNG`
7. `chore: move pieces images to assets/pieces and slugify` (mass rename + update `plialu-data.js` si conservé)
8. `chore: archive unreferenced root images under assets/legacy`
9. `chore: relocate Claude skills to .claude/skills`
10. `docs: rewrite root README and refresh CLAUDE.md`
11. `chore: add .gitignore + LICENSE`

Chaque commit reste atomique et réversible.

---

## 5. Risques

| # | Risque | Probabilité | Impact | Atténuation |
|---|---|---|---|---|
| RX-1 | URLs cassées si on slugifie les images sans synchroniser `plialu-data.js` | Élevée | Haut (configurateur muet) | Faire le rename + edit JS dans le **même commit** ; tester via GH Pages preview |
| RX-2 | Suppression de PNG racine (65) qui auraient été référencés en interne par un mode développeur non couvert | Moyenne | Moyen | Étape via `assets/legacy/` (commit 8), suppression définitive seulement après validation visuelle |
| RX-3 | `nouvelle-page.html` est en réalité l'avenir du configurateur (Option A serait alors une régression) | Inconnu | Élevé | **Demander Q1 avant exécution** |
| RX-4 | `easytest.js` contient peut-être une logique métier extraite d'un build interne, pas seulement Hammer/ZRender | Faible | Moyen | Inspection rapide avant suppression : recherche de chaînes `PLIALU`, `bavette`, etc. dans le bundle |
| RX-5 | GitHub Pages servait peut-être déjà le contenu d'un zip via un workflow non visible | Faible | Faible | Vérifier `Settings → Pages` côté GitHub avant push |
| RX-6 | Fuite des PII commerciales si le repo bascule public | Moyenne | Élevé | Avant phase 2 : confirmer la nature privée du dépôt OU externaliser ces blocs vers un fichier non versionné |
| RX-7 | Le hook git de ce repo signe via un workflow Anthropic (`bemyparteners-hub`) : un push massif (>200 renames) peut générer un PR difficile à reviewer | Élevée | Faible | Découper en commits thématiques (cf. §4.4) |
| RX-8 | `git mv` sur des fichiers contenant `#U00` peut échouer suivant le shell — utiliser quoting strict | Moyenne | Faible | Scripter via `python` ou `git mv -- "$src" "$dst"` |
| RX-9 | Suppression du script `config-main/index.html` (Python) si quelqu'un dépendait de la regénération | Faible | Faible | Conserver sous `tools/` au lieu de supprimer |

---

## 6. Validation requise

Avant de basculer en **Phase 2 (rangement effectif)**, j'ai besoin d'arbitrer :

- **Q1** : sort de `nouvelle-page.html` + ses dépendances (`plialu-data.js`, `plialu-materials.js`, `geometry.js`) — **supprimer** (Option A) ou **archiver** (Option B) ?
- **Q2** : 65 PNG racines non référencés — passage par `assets/legacy/` puis suppression dans un commit séparé (recommandé) ou suppression directe ?
- **Q3** : `maxcut.html` à la racine, ou sous `maxcut/index.html` ?
- **Q4** : script Python `config-main/index.html` — `tools/fold_configurator_export.py` ou suppression ?
- **Q5** : visibilité du dépôt — confirmer privé (sinon, traiter S-01 PII avant tout déplacement) ?
- **Q6** : LICENSE — MIT, propriétaire, autre ?

---

**Valides-tu le plan ? (oui / ajustements / non)**
