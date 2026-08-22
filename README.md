# BuildingOS

BuildingOS est une plateforme de Gestion Technique du Bâtiment (GTB)
destinée à superviser, contrôler et automatiser les équipements d'un
bâtiment intelligent.

## Objectifs

Le projet vise à centraliser la supervision et le pilotage de différents
systèmes techniques du bâtiment, notamment :

- éclairage ;
- gestion et suivi de l'énergie ;
- comptage ;
- volets et stores ;
- contrôle d'accès ;
- sécurité ;
- systèmes CVC ;
- alarmes et événements ;
- autres équipements communicants.

## Protocoles

BuildingOS est conçu pour pouvoir communiquer avec plusieurs protocoles
et technologies du bâtiment, notamment :

- BACnet ;
- Modbus ;
- KNX ;
- MQTT ;
- autres protocoles selon les besoins du projet.

## Architecture

Le projet repose sur une architecture modulaire permettant de séparer :

- la logique métier ;
- les protocoles de communication ;
- la supervision ;
- la simulation ;
- les interfaces utilisateur ;
- le stockage des données.

## Développement

La première version de BuildingOS est développée dans un environnement
de simulation afin de permettre le développement et les tests sans
nécessiter immédiatement l'installation d'équipements GTB physiques.

Les équipements physiques pourront être intégrés progressivement,
notamment à travers un ESP32.

## Technologies

Les principales technologies envisagées sont :

- Python / FastAPI ;
- PostgreSQL ;
- Docker ;
- MQTT / Mosquitto ;
- Flutter ;
- BACnet ;
- Modbus ;
- KNX ;
- ESP32.

## Statut

Projet en cours de développement.

La première phase est consacrée à la mise en place de l'architecture
logicielle, de l'infrastructure Docker et des mécanismes de simulation.