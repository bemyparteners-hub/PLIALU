# CRM PLIALU

Hub d'outils web internes de PLIALU pour le façonnage aluminium sur mesure.
HTML / CSS / JS vanilla, sans build, déployés sur GitHub Pages depuis `main`.

## Modules

| URL (GH Pages) | Source | Rôle |
|---|---|---|
| `/` | `index.html` | Hub CRM — point d'entrée vers les modules |
| `/modules/calculette/` | `modules/calculette/index.html` | Tableau de bord Calculette |
| `/modules/calculette/calcul.html` | `modules/calculette/calcul.html` | Calculette de prix (matière + MO + sous-traitance → PV HT) |
| `/modules/calculette/devis.html` | `modules/calculette/devis.html` | Génération de devis PDF (jsPDF + autoTable + pdf-lib) |
| `/modules/calculette/dessinateur.html` | `modules/calculette/dessinateur.html` | Croquis techniques canvas |
| `/modules/configurateur/` | `modules/configurateur/index.html` | Configurateur de pièces (gammes / matières / SVG) |
| `/modules/maxcut/` | `modules/maxcut/index.html` | Optimiseur de plan de découpe aluminium |

Pour ajouter un module, créer `modules/<nom>/index.html` puis ajouter une carte
dans le hub `index.html` (un `<a class="card">`).

### Couplage Calculette ↔ Configurateur

La calculette et le configurateur sont **techniquement indépendants**
(déploiement, navigation, versioning) mais **fonctionnellement liés** par le
workflow `configurer → devis`. Le couplage est assuré par :

- des **liens croisés dans les navbars** des deux modules ;
- la **convention `localStorage['plialu-devis']`** partagée par origine, qui
  transporte les lignes du configurateur vers le devis sans appel direct.

Tout autre module ajouté reste libre d'utiliser ou non cette convention.

## Structure du dépôt

```
/
├── index.html                Hub CRM (cartes vers les modules)
├── README.md
├── LICENSE
├── AUDIT.md                  Audit de structure (référence historique)
├── STYLE-AUDIT.md            Audit CSS (référence historique)
├── .gitignore
├── .claude/
│   └── skills/               Slash-commands Claude Code (10 skills)
├── shared/                   Design system (tokens + composants)
│   ├── tokens.css            Tokens couleurs / espacements / typo
│   ├── theme-dark.css        Surcharges thème sombre
│   ├── components/           navbar, buttons, card, form
│   ├── preview.html          Aperçu visuel des composants
│   └── README.md             Documentation du design system
├── modules/
│   ├── calculette/
│   │   ├── index.html        Accueil Calculette
│   │   ├── calcul.html
│   │   ├── devis.html
│   │   ├── dessinateur.html
│   │   ├── CLAUDE.md         Documentation du module
│   │   └── contacts.local.example.json
│   ├── configurateur/
│   │   ├── index.html        Configurateur de pièces (autonome)
│   │   └── CLAUDE.md         Documentation du module
│   └── maxcut/
│       └── index.html        Optimiseur de découpe
├── assets/
│   └── pieces/               Catalogue d'images de pièces (197 PNG, partagé)
└── tools/
    └── fold_configurator_export.py   Script Python jetable (export HTML)
```

`assets/` est partagé entre modules et reste à la racine. Les modules y
accèdent via `../../assets/...`. `tools/` est un répertoire dev, pas un
module utilisateur.

### Design system

Toutes les pages partagent un système de tokens et de composants CSS sous
`shared/` (HTML/CSS vanilla, pas de build). Voir [`shared/README.md`](./shared/README.md)
pour les conventions, l'ordre de chargement, et la procédure pour ajouter
un composant ou un thème.

## Données locales (PII)

Les contacts commerciaux affichés dans les devis ne sont **pas** versionnés.
Pour activer les vrais noms / téléphones / emails :

1. Copier `modules/calculette/contacts.local.example.json` en
   `modules/calculette/contacts.local.json` (ignoré par Git).
2. Charger ce JSON au démarrage en exposant `window.PLIALU_CONTACTS`
   avant l'inclusion de `devis.html`. Exemple :

   ```html
   <script>
     fetch('contacts.local.json')
       .then(r => r.json())
       .then(c => { window.PLIALU_CONTACTS = c; });
   </script>
   ```

   ou plus simplement, créer un `contacts.local.js` (lui aussi gitignoré) :

   ```js
   window.PLIALU_CONTACTS = {
     QM:  { nom:'…', fonction:'Chef des Ventes', tel:'…', email:'…' },
     JPB: { … }, TR: { … }, GB: { … }
   };
   ```

   et l'inclure avant le `<script>` principal de `devis.html`.

Sans `contacts.local.json`, des placeholders neutres (« Commercial QM », etc.)
sont utilisés — le devis fonctionne mais sans coordonnées.

## Persistance navigateur (`localStorage`)

Aucun backend. Toutes les données vivent dans le `localStorage` du navigateur :

| Clé | Contenu |
|---|---|
| `plialu_project_data` | État global (calcul / devis / dessinateur) — auto-sauvegardé |
| `plialu-devis` | File de lignes calculette → devis (vidée à l'import) |
| `plialu-devis-dessins` | File de dessins dessinateur → devis |

Le bouton « Réinitialiser tout » de `modules/calculette/index.html` purge ces 3 clés.

## Développement

```bash
# Servir en local (n'importe quel serveur HTTP statique)
python3 -m http.server 8000
# puis http://localhost:8000/
```

Le hub fonctionne aussi en `file://` (ouvrir directement `index.html`).

Convention de branche pour les contributions assistées :
`claude/<courte-description>` puis PR vers `main`.

## Licence

Propriétaire. Voir [`LICENSE`](./LICENSE).
