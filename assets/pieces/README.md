# Images des pièces

Déposez ici les photos ou schémas des articles au format PNG.

## Nommage

Convention : `{articleName}` normalisé en minuscules, espaces → `_`, tirets conservés.

| Article | Fichier attendu |
|---|---|
| Bv2Plis | `bv2plis.png` |
| Bv2Plis-90deg | `bv2plis-90deg.png` |
| Bv3Plis | `bv3plis.png` |
| Bv3Plis-90deg | `bv3plis-90deg.png` |
| Bv4Plis | `bv4plis.png` |
| Bv4Plis-90deg | `bv4plis-90deg.png` |
| Couvertine Pente Clipse | `couvertine_pente_clipse.png` |
| Couvertine Plate Collee | `couvertine_plate_collee.png` |
| Couvertine Plate 2 Rabats | `couvertine_plate_2_rabats.png` |
| Couvre joint Plat | `couvre_joint_plat.png` |
| Couvre Joint General | `couvre_joint_general.png` |
| Ge Type 1 | `ge_type_1.png` |

## Règle générale

```
slug = articleName
  .toLowerCase()
  .replace(/\s+/g, '_')
  .replace(/[^a-z0-9_\-]/g, '')
```

Si aucun fichier n'est trouvé, le configurateur affiche le rendu 3D SVG généré automatiquement.
