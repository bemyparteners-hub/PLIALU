# PLIALU — Calculette

Outil web statique interne pour le façonnage aluminium sur mesure : calcul de prix, génération de devis PDF, dessin technique.

## Règles absolues

- **Aucun framework, aucun build** : HTML/CSS/JS vanilla uniquement
- **CDN uniquement** pour les libs externes (jsPDF, pdf-lib)
- **Pas de backend** : tout persiste en `localStorage`
- GitHub Pages déploie depuis `main`
- Développer sur une branche `claude/...` puis merger via PR

---

## Structure du repo

```
/
├── index.html          # Page d'accueil / tableau de bord
├── calcul.html         # Calculette de prix
├── devis.html          # Générateur de devis PDF
├── dessinateur.html    # Outil de dessin canvas
├── README.md
└── CLAUDE.md
```

---

## Modules

### 1. `calcul.html` — Calculette de prix

**Objectif** : Calculer un prix de vente HT à partir de la matière, des dimensions et de la main-d'œuvre.

**Inputs** :
- Catégorie (Bavette, Couvertine, Accessoire, Rails, Autres)
- Matière (Aluminium, Acier, Inox, Autre) → table de prix unitaire €/m²
- Épaisseur (boutons dynamiques selon matière : 10/10, 15/10, 20/10, 25/10, 30/10)
- DVP mm + Longueur mm
- Main-d'œuvre : passes × temps/passe (secondes) pour Cisaillage / Pliage / Poinçonnage
- Taux MO (€/seconde)
- Sous-traitance : Laquage (€/m²), Soudure (€ fixe), Transport (€ fixe)
- Coefficients : chute (défaut 0,9), frais port (défaut 0,9), marge (défaut 0,65)

**Calcul** :
1. Surface = (DVP/1000) × (Longueur/1000) m²
2. Coût matière = Surface × Prix unitaire
3. Matière + chute = Coût matière / Coeff chute
4. Temps total MO = Σ(passes × temps/passe)
5. Coût MO = Temps total × Taux/seconde
6. Coût total = Matière + MO + Sous-traitance
7. **PV HT = Coût total / (Coeff port × Coeff marge)**
8. Marge brute % = (PV - Coût) / PV
9. Coefficient sur matière = PV / Coût matière

**Affichage résultat** :
- PV HT (fond jaune, mis en avant)
- Marge brute % : vert ≥ 45 %, jaune 35–45 %, rouge < 35 %
- Prix au m², coeff multiplicateur sur matière

**Flux sortant** : bouton "Ajouter au devis" → pousse une ligne dans `localStorage['plialu-devis']`

---

### 2. `devis.html` — Générateur de devis PDF

**Objectif** : Constituer et exporter un devis PDF professionnel.

**Sections** :
1. **Infos devis** : Numéro (auto DEV-ANNÉE-###), date, validité (j), chantier, référence client, commercial (radio : QM / JPB / TR / GB avec nom/titre/tél/email codés en dur)
2. **Client** : Raison sociale, contact, email, tél, adresse
3. **Lignes** : tableau éditable — Désignation, RAL, DVP mm, Longueur mm, Qté, PU HT, Total HT
   - Import depuis calculette (vide `plialu-devis` après import)
   - Ajout manuel de ligne
   - Totaux HT / TVA 20 % / TTC calculés en temps réel
4. **Commentaires & annexes** : texte libre, import dessins depuis dessinateur (`plialu-devis-dessins`), upload multi-PDF
5. **Export PDF** : un clic génère le PDF complet

**PDF généré (jsPDF + autoTable)** :
- En-tête PLIALU bleu marine + badge DEVIS
- Bloc commercial + bloc client (fond gris clair)
- Tableau lignes avec lignes alternées
- Totaux : HT (jaune), TVA (gris clair), TTC (fond foncé, texte jaune)
- Commentaires si présents
- Annexes : jusqu'à 2 dessins par page (base64 PNG) avec nom et notes
- Pied de page sur chaque page : branding + info commercial + numéro de page
- Fusion des PDFs attachés (pdf-lib) en fin de document

**Flux entrant** : `plialu-devis` (lignes calculette) + `plialu-devis-dessins` (dessins)

---

### 3. `dessinateur.html` — Outil de dessin

**Objectif** : Créer des croquis techniques annotés avec dimensions et angles.

**Outils canvas** :
- **Stylo** : traits droits A→B avec guides croisés en pointillés + HUD en temps réel (distance mm, angle °)
- **Gomme** : effacement libre
- **Texte** : labels draggables, redimensionnables, double-clic pour éditer, poignées de redimensionnement (NE / SO / SE)
- **Angle** : 3 clics → calcule l'angle au sommet (popup avec copie)

**Paramètres** : couleur (Noir / Bleu / Rouge), épaisseur (2 / 4 / 8 px), échelle (dénominateur, défaut 100 → 1:100)

**Conversion** : 1 px CSS ≈ 0,2646 mm → mm réel = px × (25,4/96) × échelle

**Snap** : si le nouveau point de départ est à < 15 px du dernier point, accrochage automatique

**Export** :
- PNG haute résolution (download direct)
- "Sauvegarder & Ajouter au devis" → pousse dans `plialu-devis-dessins`

**Annulation** : pile d'historique (max 50 états ImageData)

---

## localStorage — Architecture des données

| Clé | Type | Contenu |
|---|---|---|
| `plialu_project_data` | Objet JSON | `{ calcul: {...}, devis: {...}, dessinateur: {...} }` — sauvegarde auto de tous les champs |
| `plialu-devis` | Tableau JSON | Lignes en transit calculette → devis (vidé après import) |
| `plialu-devis-dessins` | Tableau JSON | Dessins en transit dessinateur → devis (chaque élément : `{id, name, notes, date, image (base64)}`) |

La sauvegarde est déclenchée à chaque événement `input`/`change`. Un indicateur visuel confirme la sauvegarde. Le bouton "Réinitialiser tout" sur index.html vide les 3 clés.

---

## Design system

**Couleurs** :
- Fond header : `#0d2933` (bleu marine)
- Accent : `#e8fc69` (jaune citron)
- Fond page : `#f0f4f8`
- Texte principal : `#1a2e38`
- Succès : `#dcfce7` / bordure `#86efac`
- Alerte : `#fef9c3` / bordure `#fcd34d`
- Danger : `#fee2e2` / bordure `#fca5a5`

**Typographie** : Segoe UI, sans-serif — titres 800–900, corps 400–600

**Responsive** : grilles 2–3 colonnes → 1 colonne sous 650 px ; navbar sticky z-index 100

**Canvas** : 500 px de haut, largeur fluide, support HiDPI (devicePixelRatio)

---

## Librairies CDN (devis.html uniquement)

- **jsPDF** v2.5.1 — création de PDF
- **jsPDF-AutoTable** v3.5.31 — tableaux dans PDF
- **PDF-Lib** (unpkg latest) — fusion de PDFs attachés

---

## Patterns importants

- Auto-save sur chaque `input`/`change` (sans debounce, indicateur visuel)
- Transfert inter-modules exclusivement via localStorage (pas de state global partagé)
- Canvas HiDPI : `canvas.width = offsetWidth × devicePixelRatio`
- Pile undo dessinateur : snapshots `ImageData` (max 50)
- Textes canvas : overlays `<div>` absolus, pas dessinés sur le canvas
- Validation minimale : DVP + Longueur requis pour calcul ; nom requis pour sauvegarde dessin

---

## Skills disponibles

- `/performance` — Analyse des performances web
- `/code-review` — Revue de code
