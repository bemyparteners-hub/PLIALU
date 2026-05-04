# Security Skill

Identifie et corrige les vulnérabilités de sécurité dans le code.

## Processus

1. **Auditer** — Passer en revue les points d'entrée de données (inputs, URL, localStorage)
2. **Identifier** — Repérer les risques XSS, injection, exposition de données
3. **Corriger** — Appliquer les protections minimales nécessaires
4. **Valider** — Vérifier que les corrections ne cassent pas le comportement

## Risques prioritaires pour ce projet (vanilla JS)

### XSS (Cross-Site Scripting)
- Ne jamais utiliser `innerHTML` avec des données utilisateur
- Toujours échapper les données avant insertion dans le DOM
- Utiliser `textContent` ou `createElement` à la place

```js
// Dangereux
el.innerHTML = userInput;

// Sûr
el.textContent = userInput;
```

### localStorage
- Ne jamais stocker de données sensibles (mots de passe, tokens)
- Toujours valider et sanitiser les données lues depuis localStorage
- Gérer les erreurs JSON.parse avec try/catch

### Données utilisateur
- Valider les types et formats côté client (et rappeler que ça ne remplace pas le serveur)
- Limiter la taille des inputs

## Règles

- La sécurité par obscurité n'est pas de la sécurité
- Moindre privilège : ne demander que ce dont on a besoin
- Signaler les risques résiduels qui nécessitent une correction côté serveur

## Output attendu

- Vulnérabilités corrigées avec explication
- Commit avec message `security: <description>`
