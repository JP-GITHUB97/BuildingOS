# ADR 0004 — Sécurité incendie et contrôle d'accès

## Statut

Accepté

## Contexte

BuildingOS doit pouvoir superviser différents systèmes techniques du
bâtiment, notamment :

- contrôle d'accès ;
- détection incendie ;
- alarmes ;
- équipements de sécurité ;
- événements associés.

Ces fonctions ont un niveau de criticité supérieur à celui d'une commande
classique d'éclairage ou de confort.

Une erreur logicielle ne doit pas pouvoir désactiver ou contourner les
fonctions de sécurité d'un système certifié.

## Décision

BuildingOS sera conçu comme une plateforme de supervision et d'intégration.

Pour les systèmes critiques, BuildingOS ne remplacera pas les équipements
de sécurité dédiés et certifiés.

Les fonctions critiques resteront assurées par les systèmes et contrôleurs
appropriés.

BuildingOS pourra notamment :

- recevoir des états ;
- afficher des alarmes ;
- historiser des événements ;
- transmettre certaines commandes autorisées ;
- notifier les utilisateurs ;
- superviser l'état des équipements.

## Priorité des événements

Les événements critiques auront une priorité supérieure aux commandes
utilisateur ordinaires.

Exemple :

```text
Détection incendie
       │
       ▼
Événement critique
       │
       ├──► Alarme
       ├──► Historisation
       ├──► Notification
       └──► Actions de sécurité configurées