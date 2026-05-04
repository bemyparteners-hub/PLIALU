# Bug Fix Skill

Analyse et corrige le bug décrit par l'utilisateur de façon systématique.

## Processus

1. **Reproduire** — Identifier les étapes exactes qui déclenchent le bug
2. **Isoler** — Localiser le fichier et la ligne responsable
3. **Comprendre** — Lire le code environnant avant toute modification
4. **Corriger** — Appliquer le correctif minimal sans effets de bord
5. **Vérifier** — S'assurer que le bug est résolu et rien n'est cassé

## Règles

- Ne jamais modifier du code non lié au bug
- Préférer une correction chirurgicale à un refactor
- Si la cause racine est ailleurs, signaler sans corriger en cascade
- Documenter le correctif dans le commit message

## Output attendu

- Fichier(s) modifié(s) avec le correctif
- Explication courte de la cause et de la solution
- Commit avec message `fix: <description précise>`
