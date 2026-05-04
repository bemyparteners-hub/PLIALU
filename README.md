# PLIALU

Outils web internes de PLIALU pour le façonnage aluminium sur mesure.
HTML / CSS / JS vanilla, sans build, déployés sur GitHub Pages depuis `main`.

## Applications

| URL (GH Pages) | Source | Rôle |
|---|---|---|
| `/` | `index.html` | Tableau de bord — points d'entrée vers les outils |
| `/calcul.html` | `calcul.html` | Calculette de prix (matière + MO + sous-traitance → PV HT) |
| `/devis.html` | `devis.html` | Génération de devis PDF (jsPDF + autoTable + pdf-lib) |
| `/dessinateur.html` | `dessinateur.html` | Croquis techniques canvas (cotes, angles, export PNG) |
| `/configurateur.html` | `configurateur.html` | Configurateur de pièces (gammes / matières / SVG paramétrique) |
| `/maxcut/` | `maxcut/index.html` | Optimiseur de découpe aluminium (autonome) |

## Structure du dépôt

```
/
├── index.html, calcul.html, devis.html, dessinateur.html, configurateur.html
├── CLAUDE.md                 Documentation projet pour les agents IA
├── README.md                 Ce fichier
├── LICENSE                   Tous droits réservés — PLIALU
├── AUDIT.md                  Audit de structure (référence historique)
├── contacts.local.example.json   Schéma des contacts commerciaux (cf. infra)
├── .gitignore
├── .claude/
│   └── skills/               Slash-commands Claude Code (10 skills)
├── assets/
│   └── pieces/               Catalogue d'images de pièces (197 PNG)
├── maxcut/
│   └── index.html            Optimiseur de découpe (autonome)
└── tools/
    └── fold_configurator_export.py   Prototype Python (export HTML statique)
```

## Données locales (PII)

Les contacts commerciaux affichés dans les devis ne sont **pas** versionnés.
Pour activer les vrais noms / téléphones / emails :

1. Copier `contacts.local.example.json` en `contacts.local.json` (ignoré par Git).
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

Le bouton « Réinitialiser tout » de `index.html` purge ces 3 clés.

## Développement

```bash
# Servir en local (n'importe quel serveur HTTP statique)
python3 -m http.server 8000
# puis http://localhost:8000/
```

Convention de branche pour les contributions assistées :
`claude/<courte-description>` puis PR vers `main`.

## Licence

Propriétaire. Voir [`LICENSE`](./LICENSE).
