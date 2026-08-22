# ADR 0003 — PostgreSQL comme source de vérité

## Statut

Accepté

## Contexte

BuildingOS doit conserver les informations nécessaires à la supervision
d'un bâtiment.

Ces informations comprennent notamment :

- utilisateurs ;
- bâtiments ;
- zones ;
- équipements ;
- capacités des équipements ;
- configurations ;
- alarmes ;
- historiques ;
- mesures énergétiques ;
- événements.

Ces données doivent rester disponibles après le redémarrage des services.

## Décision

PostgreSQL sera utilisé comme base de données principale de BuildingOS
et comme source de vérité pour les données persistantes.

Les communications temps réel avec les équipements ne seront pas réalisées
directement via PostgreSQL.

Les commandes destinées aux équipements passeront par les services de
communication appropriés.

## Principe

```text
Application
     │
     ▼
  FastAPI
     │
     ├──────────────► PostgreSQL
     │                 données persistantes
     │
     └──────────────► Protocol adapters
                       │
                       ├── MQTT
                       ├── Modbus
                       ├── BACnet
                       └── KNX