# ADR 0001 — Séparation entre logique métier et protocoles

## Statut

Accepté

## Contexte

BuildingOS doit permettre de superviser et contrôler différents équipements
d'un bâtiment.

Les équipements peuvent utiliser différents protocoles :

- MQTT
- Modbus
- BACnet
- KNX
- protocoles ou simulateurs futurs

L'application utilisateur ne doit pas dépendre directement de ces protocoles.

## Décision

La logique métier de BuildingOS sera séparée de la couche de communication
avec les équipements.

Le backend exposera une représentation commune des équipements et des actions.

Les adaptateurs de protocoles seront responsables de traduire les actions
BuildingOS vers le protocole correspondant.

Exemple :

Utilisateur
→ "Allumer la lumière"

BuildingOS
→ commande `turn_on`

Adaptateur protocole
→ traduction vers MQTT, Modbus, BACnet ou KNX.

## Conséquences positives

- Ajout de nouveaux protocoles sans modifier toute l'application.
- Possibilité de simuler les équipements.
- Tests plus simples.
- Architecture plus évolutive.
- Possibilité de mélanger équipements réels et simulés.

## Conséquences négatives

- Architecture plus complexe qu'une communication directe.
- Nécessité de maintenir des adaptateurs pour chaque protocole.
- Nécessité de définir un modèle commun des équipements.

## Exemple

Une lumière peut être représentée dans BuildingOS comme :

```text
Light
├── id
├── name
├── location
├── state
└── capabilities