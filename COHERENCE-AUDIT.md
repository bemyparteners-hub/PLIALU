# COHERENCE-AUDIT — Audit critique du projet PLIALU

> Phase exploratoire, lecture seule. Date : 2026-05-05.
> Aucun fichier modifié hormis ce rapport.
>
> Audit indépendant et critique de l'état du dépôt après les phases
> initiale (audit), structurelle (modules), design system (tokens +
> composants), et harmonisation thème clair (MAXCUT).

---

## A · Résumé exécutif

**État global** : sain. Les phases successives ont laissé un dépôt
fonctionnellement cohérent, avec un design system propre et un
hub CRM unifié. Les rendus sont en accord avec les objectifs.
Les écarts détectés sont quasi tous des **dettes mineures**
(documentation drift, code mort résiduel, duplications JS qui
étaient OK dans une logique « page autonome » mais le sont moins
dans la logique « modules d'un même CRM »).

**Top 3 à faire en priorité** *(tous résolus à la date du
2026-05-04 — voir détail par finding ci-dessous)* :

1. ✅ ~~Supprimer~~ documenter `assets/pieces/` (197 PNG, 17 Mo) :
   décision **conservation**, statut « réservé pour aperçus
   visuels futurs », doc mise à jour. Voir F-1.1.
2. ✅ Factoriser le pattern `showSaveIndicator` + `getProjectData`
   + `SAVE_KEY` dupliqué dans 4 fichiers → `shared/js/storage.js`.
   Voir F-2.1 (branche `refactor/shared-js-storage`, 7 commits).
3. ✅ Mettre à jour `modules/calculette/CLAUDE.md` (référence
   obsolète à `../../assets/pieces/`). Voir F-6.1.

**Top 3 à NE PAS faire** :

1. ✋ Ne **pas** tokeniser les 48 occurrences de `#0d2933` et
   30 de `#e8fc69` hardcodées dans les `<style>` inline. Le risque
   est purement cosmétique, l'effort est élevé, et le drift
   éventuel d'`--brand-900` est très peu probable (couleur de marque).
2. ✋ Ne **pas** supprimer `shared/components/sidebar.css` même
   s'il n'a qu'**un seul** consommateur (le hub). La cohérence
   avec `navbar.css` (même pattern d'extraction) prime.
3. ✋ Ne **pas** archiver / déplacer `AUDIT.md`, `STYLE-AUDIT.md`,
   `LINK-AUDIT.md` ailleurs. Les laisser à la racine avec un
   header explicite « HISTORICAL — snapshot du <date> » suffit.
   Ils servent de mémoire de projet pour le prochain contributeur.

---

## B · Findings détaillés

### 1. Code mort

#### F-1.1 ✅ RÉSOLU — `assets/pieces/` documenté comme réservé pour usage futur

- **Statut** : résolu le 2026-05-05 par `c29cbf5`. Décision
  utilisateur : **conserver les images** pour usage futur (aperçus
  visuels dans configurateur / devis / fiche pièce). Le dossier
  passe de « orphelin trompeur » à « réserve documentée » :
  - `assets/pieces/README.md` réécrit avec un statut explicite
    (« currently UNUSED in production / Reserved for future
    visual previews ») + historique d'extraction + convention
    d'usage future + conventions de nommage.
  - `README.md` racine annoté en conséquence.
  - `modules/calculette/CLAUDE.md` corrigé (ne prétend plus que
    le module dépend des images).
- **Constat original** : `grep -rn "pieces/"` retourne **0 référence**
  dans le HTML/CSS/JS de production. Les images étaient consommées
  par `nouvelle-page.html` + `plialu-data.js`, tous deux supprimés
  en phase 2 commit 7cc1622 (Q1).

#### F-1.2 ✅ RÉSOLU — `tools/fold_configurator_export.py` supprimé

- **Statut** : résolu en commit 3 de Vague 1. Le script Python jetable
  (534 lignes, écriture vers `/mnt/data/` inexistant hors notebook,
  zéro consommateur) supprimé via `git rm`. Le dossier `tools/`
  devenu vide a été supprimé du working tree (les répertoires vides
  ne sont pas suivis par git). L'historique git conserve le
  contenu si besoin de redécouvrir le prototype (`git log -- tools/`).
  `README.md` racine mis à jour : entrée `tools/` retirée du tree.

#### F-1.3 🟡 `packSheets()` — fonction JS orpheline dans MAX

- **Localisation** : `modules/maxcut/index.html:868`
- **Constat** : déclarée mais **jamais appelée** (vérifié par grep).
  Probablement un résidu d'une implémentation antérieure
  remplacée par le pipeline actuel `runOptimize() → packBin*()`.
- **Action recommandée** : supprimer la fonction si confirmation
  qu'elle n'est pas utilisée par un export externe. Sinon, marquer
  d'un commentaire `// kept for external export — DO NOT REMOVE`.

#### F-1.4 ✅ RÉSOLU partiellement — 2 tokens morts supprimés, 3 conservés par cohérence

- **Statut** : résolu en commit 3 de Vague 1 sur la partie
  « vraiment morte ». Suppression dans `shared/tokens.css` de :
  - `--brand-700` (#1a2e38) — duplique `--text-primary`, zéro usage.
  - `--bg-secondary` (#fafbfc) — zéro consommateur en thème clair.
  
  `theme-dark.css` n'a **pas** été modifié : il redéfinissait
  `--bg-secondary: #0a1f28` pour le dark mode. Garder cette
  ligne dans le « ready-to-use override » (le fichier reste
  cohérent comme pré-bagage pour un futur module dark).
  L'asymétrie créée (token défini en dark mais pas en light) est
  sans conséquence : aucune page ne charge theme-dark + ne
  consomme `--bg-secondary`.
- **Conservés** : `--success-border` (#86efac), `--warning-bg`
  (#fef3c7), `--warning-border` (#fcd34d). La triade
  success/warning/danger reste symétrique (`--danger-bg/border`
  existent et sont utilisés).

#### F-1.5 🟢 4 classes shared sans usage en production

- **Localisation** :
  - `.card-active` dans `shared/components/card.css`
  - `.nav-brand--static`, `.nav-title--hub`, `.nav-title-prefix`
    dans `shared/components/navbar.css` (utilisées seulement par
    `shared/preview.html` Section 3, comme référence historique du
    hub avant migration sidebar)
  - `.sidebar-link--active` dans `shared/components/sidebar.css`
    (le hub n'a pas d'item actif puisqu'on EST déjà à la maison)
- **Action recommandée** : **garder**. Coût zéro, ce sont des
  variantes prêtes à l'emploi qui peuvent matérialiser un état
  futur (carte sélectionnée, lien sidebar actif sur sous-page,
  etc.). Documentées par la convention de nommage explicite.

### 2. Doublons

#### F-2.1 ✅ RÉSOLU — `shared/js/storage.js` factorise l'auto-save

- **Statut** : résolu le 2026-05-04 par la branche
  `refactor/shared-js-storage` (7 commits) :

  | # | SHA | Commit |
  |---|---|---|
  | 1 | `1fac6d7` | `feat(shared): add storage helpers` |
  | 2 | `8fa6f05` | `refactor(calculette/calcul): use PlialuStorage` |
  | 3 | `ed821f8` | `refactor(calculette/devis): use PlialuStorage` |
  | 4 | `bb85955` | `refactor(calculette/dessinateur): use PlialuStorage` |
  | 5 | `4f9dd44` | `refactor(configurateur): use PlialuStorage` |
  | 6 | `974cc8e` | `chore: drop static save-indicator markup and CSS` |
  | 7 | (ce commit) | `docs: resolve F-2.1 and document shared/js/` |

  78 lignes JS dupliquées remplacées par 110 lignes shared (gain
  net −26 lignes + 1 source de vérité unique pour le format de
  stockage et l'indicateur visuel).

- **API factorisée** dans `shared/js/storage.js` (cf. `shared/README.md`
  section *JS partagé*) :

  ```js
  // Une clé propre (configurateur)
  const storage = PlialuStorage.forKey('plialu-configurateur-session');
  // Une sous-clé d'un objet racine partagé (calculette pages)
  const storage = PlialuStorage.forSubkey('plialu_project_data', 'calcul');
  storage.load();   // null si rien stocké, l'objet sinon
  storage.save(d);  // persiste + déclenche le toast
  storage.clear();  // efface (NE déclenche PAS le toast)
  ```

  Plus `PlialuStorage.showIndicator(message?)` pour appel manuel.
  Toast : élément `.plialu-save-indicator` créé à la volée + stylé
  par `shared/components/save-indicator.css` (token-driven).

- **Constat original** (laissé pour référence) :
  > Le triplet `const SAVE_KEY = 'plialu_project_data'` +
  > `function getProjectData()` + `function showSaveIndicator()`
  > était répété identique dans les 4 fichiers (~25 lignes × 4 = ~100
  > lignes). Le CSS `#save-indicator { … }` apparaissait aussi en
  > double (calcul.html + configurateur) avec un troisième duplicata
  > inline via `el.style.cssText = '…'` dans devis.html et
  > dessinateur.html.

#### F-2.2 🟡 Hex literals brand non tokenisés (post phase 2 commit 8)

- **Localisation** : 48 × `#0d2933`, 30 × `#e8fc69`, 16 × `#1a2e38`
  dans les inline `<style>` des 5 pages calculette + configurateur.
- **Constat** : la phase 2 commit 8 a tokenisé `body{}` mais a
  laissé les règles page-spécifiques (tables, hero, modals, etc.)
  avec leurs hex littéraux. Conséquence : si `--brand-900` change
  un jour, ces 48 occurrences ne suivent pas. Le système de tokens
  n'est pas complètement adopté.
- **Action recommandée** : **laisser**. Les couleurs de marque
  ne changeront pas (c'est l'identité PLIALU). Le risque de drift
  effectif est très faible. Le coût de migration (touch tous les
  inline styles) est élevé. Mauvais ROI.

#### F-2.3 🟢 Reset CSS répété dans chaque page

- **Localisation** : `*,*::before,*::after { box-sizing:border-box;
  margin:0; padding:0 }` dans **toutes** les 7 pages, en début de
  `<style>` inline.
- **Constat** : reset CSS canonique, identique partout. Pourrait
  être extrait dans `shared/components/_base.css` ou ajouté à
  `tokens.css`.
- **Action recommandée** : **borderline**. C'est 1 ligne, mais
  copiée 7 fois. Si on veut la propreté du design system, ajouter
  un fichier `shared/reset.css` (ou la mettre tokens.css). Sinon
  laisser — la duplication est triviale et zéro risque de drift.

### 3. Incohérences structurelles

#### F-3.1 🟢 Aucun lien CSS mort détecté

- **Localisation** : N/A
- **Constat** : audit `LINK-AUDIT.md` reste valable. Chaque `<link
  rel="stylesheet">` a au moins un consommateur dans la page.
  Aucune classe utilisée sans CSS qui la définit (le bug latent
  fixé dans `72a86a7` était l'unique cas).

#### F-3.2 🟢 Conventions de nommage cohérentes

- **Localisation** : N/A
- **Constat** : kebab-case partout, modificateurs BEM `--variant`
  partout. Préfixes namespaced (`.max-card`, `.stat-card`,
  `.plan-card`, `.mat-card`) cohérents. Pas de drift détecté.

### 4. Sur-ingénierie

#### F-4.1 🟢 `shared/components/sidebar.css` chargé par 1 page

- **Localisation** : `shared/components/sidebar.css` (~200 lignes,
  à supposer du contenu)
- **Constat** : production : `index.html` (hub) seulement.
  Dev tool : `shared/preview.html`. Total = 2 consommateurs.
- **Action recommandée** : **garder**. Cohérence avec `navbar.css`
  (même logique d'extraction), file size raisonnable, et permet
  l'évolutivité (un futur module monitoring pourrait l'utiliser).
  Le ROI de ré-inliner serait négatif.

#### F-4.2 🟢 `shared/components/form.css` — usage solide

- **Localisation** : `shared/components/form.css`
- **Constat** : utilisé par 4 pages (calcul, devis, dessinateur,
  configurateur) avec 64 éléments de formulaire au total. Pas
  d'overrides inline en concurrence (1 seul dans devis.html).
  **Bonne extraction**, ne pas toucher.

### 5. Sous-ingénierie

#### F-5.1 ✅ RÉSOLU (cf. F-2.1) — JS auto-save factorisé

Voir F-2.1 — résolu en branche `refactor/shared-js-storage`.

#### F-5.2 ✅ RÉSOLU — `shared/js/` créé avec convention documentée

- **Statut** : résolu le 2026-05-04 par le commit 1 de la branche
  `refactor/shared-js-storage` (`1fac6d7`). Le dossier `shared/js/`
  contient maintenant `storage.js` (premier fichier JS partagé) et
  la convention est documentée dans `shared/README.md` section
  *JS partagé* (namespacing global `window.PlialuStorage`, pas de
  modules ES, pas de build, ordre de chargement `<script>` avant
  l'inline qui le consomme).

### 6. Documentation

#### F-6.1 ✅ RÉSOLU — `modules/calculette/CLAUDE.md` ne référence plus `assets/pieces/`

- **Statut** : résolu le 2026-05-05 par `72c5b3f`. La section
  « Place dans le dépôt » a été reformulée pour pointer vers les
  vraies dépendances (composants `shared/`) et plus vers les
  images. Un bonus a été corrigé en passant : la section
  « Design system » avait `--warning-bg = #fef9c3` (typo, vraie
  valeur `#fef3c7`) ; remplacée par un pointeur vers
  `tokens.css`.
- **Constat original** : citation littérale —
  > « Les assets partagés (`assets/pieces/`) sont à la racine ;
  > depuis ce module, on y accède via `../../assets/pieces/`. »
  Faux : le module calculette n'accède à aucune image de
  `assets/pieces/`.

#### F-6.2 ✅ RÉSOLU — `README.md` racine annoté

- **Statut** : résolu le 2026-05-05 par `c29cbf5`.
  L'entrée `pieces/` du tree est maintenant : « 197 PNG réservés
  pour aperçus visuels futurs (non utilisés en production, voir
  assets/pieces/README.md) ». Plus de mention trompeuse
  « partagé ».

#### F-6.3 ✅ RÉSOLU — `AUDIT.md` et `STYLE-AUDIT.md` annotés comme historiques

- **Statut** : résolu en commit 3 de Vague 1. Encart « HISTORICAL
  SNAPSHOT » ajouté en haut de chacun des 2 fichiers, pointant vers
  `LINK-AUDIT.md` et `COHERENCE-AUDIT.md` pour l'état courant. Les
  fichiers restent à la racine pour servir de mémoire de projet.

#### F-6.4 🟢 `LINK-AUDIT.md` à jour

- **Localisation** : `LINK-AUDIT.md`
- **Constat** : counts vérifiés (134 var() pour MAX, 33 pour hub,
  6 pour calculette/index — tous identiques aux valeurs de
  référence). A1 marqué résolu, A2/A3 toujours pertinents.
- **Action recommandée** : **rien**.

#### F-6.5 🟢 `shared/README.md` cohérent avec les fichiers présents

- **Localisation** : `shared/README.md`
- **Constat** : décrit `tokens.css`, `theme-dark.css`,
  `components/navbar.css`, `components/sidebar.css`,
  `components/buttons.css`, `components/card.css`,
  `components/form.css`, `preview.html` — tous présents.
  Note explicite sur theme-dark.css non utilisé. À jour.
- **Action recommandée** : **rien**.

### 7. Arborescence

#### F-7.1 🔴 `assets/pieces/` (cf. F-1.1)

#### F-7.2 🟡 `tools/` avec 1 seul fichier rarement utile (cf. F-1.2)

#### F-7.3 🟢 Aucun dossier vide

- **Constat** : tous les dossiers ont du contenu utile.

#### F-7.4 🟢 Profondeurs cohérentes

- **Constat** : `..` resolution audit = OK. Hub @ root, modules
  @ depth 2, shared @ root. Conventions documentées dans
  `shared/README.md`.

---

## C · Plan d'exécution proposé (si tu valides)

Si tu veux exécuter les findings importants, voici l'ordre
suggéré, **du moins risqué au plus impactant** :

| # | Commit | Niveau | Risque |
|---|---|---|---|
| 1 | `docs: mark AUDIT.md and STYLE-AUDIT.md as historical snapshots` | 🟢 | aucun |
| 2 | `chore: remove obsolete assets/pieces ref from calculette CLAUDE.md and root README` (sans toucher aux images) | 🟢 | aucun |
| 3 | `chore: drop 5 unused design tokens (--bg-secondary, --brand-700, --success-border, --warning-bg, --warning-border)` *ou subset selon décision F-1.4* | 🟢 | très faible (vérification preview.html) |
| 4 | `chore: drop orphan packSheets() from MAXCUT` (à confirmer) | 🟡 | faible |
| 5 | `chore: drop tools/fold_configurator_export.py` | 🟡 | faible |
| 6 | `chore: drop unused assets/pieces/ (197 PNG, ~17 MB)` | 🔴 | **moyen** — irréversible côté working tree, mais conservé en history. **Demande confirmation explicite.** |
| 7 | `feat(shared): extract storage helpers to shared/js/storage.js` (factorisation F-2.1) + migrer les 4 fichiers consommateurs | 🟡 | moyen — ouvre la convention `shared/js/` |
| 8 | `docs: update LINK-AUDIT and shared/README to reflect changes` | 🟢 | aucun |

**Total estimé** : 8 commits si tu valides tout. Possibilité de
fusionner 1+2+3+4+5 en un seul commit « cleanup global » si tu
préfères, mais des commits séparés permettent de revert
individuellement.

**Risques de régression** :

- F-6 (suppression `assets/pieces/`) : aucun consommateur connu,
  mais s'il y a un module futur qui les attendait, il faudra les
  ré-extraire de l'historique git.
- F-7 (factorisation JS auto-save) : risque de bug si le
  factorisation ne préserve pas l'isolation des données par page
  (calcul, devis, dessinateur, configurateur lisent/écrivent
  des sous-clés différentes du même `plialu_project_data`).
  **Tester chaque page après migration**.

**Findings non actionnés (par recommandation)** :
- F-2.2 (hex hardcodés `#0d2933`) : laisser
- F-2.3 (reset CSS dupliqué) : borderline, laisser sauf si tu
  veux pousser le design system
- F-1.5 (4 classes shared mortes) : laisser
- F-4.1 (`sidebar.css` 1 user) : laisser
- F-1.4 partiel (success/warning border tokens) : laisser
- F-6.4, F-6.5 (LINK-AUDIT, shared/README) : à jour, ne rien faire

---

**En attente de ta validation.**
