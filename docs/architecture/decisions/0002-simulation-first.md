# ADR 0002 — Développement simulation-first

## Statut

Accepté

## Contexte

BuildingOS doit permettre de contrôler et superviser différents équipements
d'un bâtiment :

- éclairage ;
- volets roulants ;
- compteurs d'énergie ;
- contrôle d'accès ;
- sécurité incendie ;
- capteurs ;
- équipements CVC ;
- autres équipements connectés.

Le projet est initialement développé dans un environnement domestique avec
un budget limité.

L'achat immédiat de nombreux équipements physiques KNX, BACnet, Modbus ou
autres protocoles serait coûteux et limiterait la vitesse de développement.

## Décision

BuildingOS sera développé selon une approche simulation-first.

Chaque équipement important devra pouvoir être représenté par un équipement
virtuel avant son intégration avec un équipement physique.

Les simulateurs devront permettre de reproduire autant que possible :

- les états des équipements ;
- les commandes ;
- les mesures ;
- les changements d'état ;
- les erreurs ;
- les communications avec les protocoles concernés.

L'architecture devra permettre de remplacer progressivement un simulateur
par un équipement réel sans modifier la logique métier principale.

## Architecture cible

```text
                    BuildingOS
                        │
                  Logique métier
                        │
                Interface commune
                        │
          ┌─────────────┴─────────────┐
          │                           │
      Simulation                  Matériel réel
          │                           │
    ┌─────┼─────┐               ┌─────┼─────┐
    │     │     │               │     │     │
  MQTT Modbus BACnet          MQTT Modbus BACnet
    │     │     │               │     │     │
    └─────┼─────┘               └─────┼─────┘
          │                           │
       Virtuel                    Physique