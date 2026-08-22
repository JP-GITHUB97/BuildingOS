# Contributing to BuildingOS

Merci de votre intérêt pour BuildingOS.

## Workflow

1. Créer une branche dédiée à la fonctionnalité.
2. Développer la fonctionnalité.
3. Ajouter ou modifier les tests nécessaires.
4. Vérifier que les tests passent.
5. Créer un commit clair.
6. Ouvrir une Pull Request.

## Convention de commit

Les commits suivent autant que possible le format Conventional Commits.

Exemples :

- `feat: add device management API`
- `fix: correct MQTT connection`
- `docs: update architecture documentation`
- `test: add health endpoint tests`
- `chore: update dependencies`

## Principes

- Ne jamais versionner de secrets.
- Ne jamais mettre de mots de passe dans le code.
- Ajouter des tests pour les fonctionnalités importantes.
- Documenter les décisions d'architecture.