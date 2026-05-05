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

**Top 3 à faire en priorité** :

1. 🔴 Supprimer `assets/pieces/` (197 PNG, **17 Mo**) — totalement
   orphelins depuis la suppression de `nouvelle-page.html` en phase 2.
   La documentation les présente comme « partagés » alors qu'aucun
   module ne les charge.
2. 🟡 Factoriser le pattern `showSaveIndicator` + `getProjectData`
   + `SAVE_KEY` dupliqué à l'identique dans **4 fichiers HTML**
   (calcul, devis, dessinateur, configurateur) → `shared/js/storage.js`.
3. 🟡 Mettre à jour `modules/calculette/CLAUDE.md` qui référence
   encore `../../assets/pieces/` comme dépendance — c'est faux
   depuis la phase 2.

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

#### F-1.2 🟡 `tools/fold_configurator_export.py` — script Python jetable

- **Localisation** : `tools/fold_configurator_export.py` (534 lignes)
- **Constat** : ce script écrit un HTML prototype de
  « Configurateur de pliage » dans `/mnt/data/fold_configurator.html`
  (path qui n'existe pas hors du notebook d'origine). Aucun
  consommateur. Le projet a maintenant un vrai
  `modules/configurateur/index.html` qui rend ce prototype
  obsolète.
- **Action recommandée** : `git rm tools/fold_configurator_export.py`
  (l'historique git conserve le contenu si besoin de redécouvrir
  le prototype). Si le dossier `tools/` devient vide, le supprimer
  également.

#### F-1.3 🟡 `packSheets()` — fonction JS orpheline dans MAX

- **Localisation** : `modules/maxcut/index.html:868`
- **Constat** : déclarée mais **jamais appelée** (vérifié par grep).
  Probablement un résidu d'une implémentation antérieure
  remplacée par le pipeline actuel `runOptimize() → packBin*()`.
- **Action recommandée** : supprimer la fonction si confirmation
  qu'elle n'est pas utilisée par un export externe. Sinon, marquer
  d'un commentaire `// kept for external export — DO NOT REMOVE`.

#### F-1.4 🟡 5 tokens définis mais jamais consommés

- **Localisation** : `shared/tokens.css`
- **Constat** :
  - `--bg-secondary` (#fafbfc) — utilisé seulement par `theme-dark.css` qui n'est plus chargé
  - `--brand-700` (#1a2e38) — duplique exactement `--text-primary`, jamais utilisé directement
  - `--success-border` (#86efac) — défini, jamais consommé
  - `--warning-bg` (#fef3c7) — idem
  - `--warning-border` (#fcd34d) — idem
- **Action recommandée** :
  - `--bg-secondary`, `--brand-700` : SUPPRIMER (vraiment morts).
  - `--success-border`, `--warning-bg/border` : **garder** pour
    cohérence avec la triade success/warning/danger (les tokens
    `--danger-bg/border` existent et sont utilisés). Ce serait
    arbitraire de ne garder que la moitié de la palette de statuts.

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

#### F-2.1 🟡 Logique d'auto-save dupliquée dans 4 fichiers HTML

- **Localisation** :
  - `modules/calculette/calcul.html:325-326,327-...,426-...`
  - `modules/calculette/devis.html:286,288,291`
  - `modules/calculette/dessinateur.html:912,914,917`
  - `modules/configurateur/index.html:751`
- **Constat** : le triplet `const SAVE_KEY = 'plialu_project_data'`
  + `function getProjectData()` + `function showSaveIndicator()`
  est répété **identique** (ou quasi-identique au `0.88` près)
  dans les 4 fichiers. C'est ~25 lignes × 4 = ~100 lignes de
  duplication.
  Le CSS associé `#save-indicator { … }` apparaît aussi en double
  (calcul.html:73 + configurateur:91), avec en plus un troisième
  duplicata via `el.style.cssText = '…'` dans le JS lui-même
  (parce que le helper crée l'élément à la volée s'il n'existe
  pas dans le DOM).
- **Action recommandée** : créer
  `shared/js/storage.js` exposant `window.PlialuStorage = {
  saveKey, getProjectData(), saveProjectData(data),
  showSaveIndicator() }`. Charger via `<script src="…/storage.js">`
  dans les 4 pages. Supprimer les définitions locales.
  Bénéfice : ~80 lignes en moins, point unique de mise à jour si
  le format de stockage évolue. Risque : faible (refactor
  mécanique, JS).

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

#### F-5.1 🟡 (cf. F-2.1) JS auto-save non factorisé

Voir F-2.1 — le pattern le plus dupliqué du projet, prêt pour une
factorisation propre.

#### F-5.2 🟢 `<script src="…">` partagés inexistants

- **Constat** : il n'y a **aucun** fichier JS partagé dans `shared/`
  (seulement des CSS). Si la factorisation F-2.1 se fait, ce sera
  l'introduction du concept. À documenter dans `shared/README.md`
  et créer un sous-dossier `shared/js/`.
- **Action recommandée** : **prévoir** la convention en même temps
  que F-2.1 (premier `shared/js/` du projet).

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

#### F-6.3 🟢 `AUDIT.md` et `STYLE-AUDIT.md` sont historiques

- **Localisation** : `AUDIT.md`, `STYLE-AUDIT.md`
- **Constat** : ces snapshots décrivent l'état **avant** les
  refactors. Ils sont obsolètes au sens où ils ne reflètent pas
  l'état actuel, mais **précieux** comme archives expliquant
  pourquoi le code a été refactoré. La date 2026-05-04 est
  explicitement mentionnée dans leur en-tête.
- **Action recommandée** : ajouter en haut de chacun un encart
  bien visible :
  > **⚠ HISTORICAL SNAPSHOT — état du dépôt avant refactor.
  > Conserve la trace de l'audit initial. Pour l'état courant,
  > voir `LINK-AUDIT.md` et `COHERENCE-AUDIT.md`.**

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
