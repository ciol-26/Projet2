# Prédiction des points d'un joueur de la LNH

Projet 2 d'INF1007 (Polytechnique Montréal, A2026), réalisé par Loïc Rousseau et Jade Karaoulanis.

## Description

Application avec interface graphique qui estime combien de points un joueur de la LNH fera la saison suivante, à partir de ses statistiques de la saison courante.

## Jeu de données

- **Nom** : NHL Statistics, fichier `skaters_by_season_summary.csv`
- **Auteur** : natashk (Kaggle)
- **Lien** : https://www.kaggle.com/datasets/natashk/nhl-statistics
- **Date de consultation** : 2026-10-27
- **Licence** : « Other (specified in description) » 
- **Contenu** : statistiques de saison régulière des patineurs de la LNH, une ligne par joueur et par saison (47 644 lignes et 26 colonnes au départ). Les statistiques sont triées par ordre alphabétique du nom de famille des jouerus selon l'année de la saison (1937 à 2026).

## Étape 1 : exploration et nettoyage (`src/donnees.py`)

### Exploration

Utilisitation de l'outil **pandas** afin de lire, netttoyer et analyser le fichier .csv contenant les statistiques des joueurs de la LNH.

Observations principales :
- `timeOnIcePerGame` est absente pour les saisons avant **1997-1998**.
- Certaines catégories sont superflues, car certaines statistiques se retrouve facilement à l'aide de d'autres colonnes

### Nettoyage et transformations

| Opération | Justification |
|---|---|
| Garder les saisons à partir de 1997-1998 | Première saison où `timeOnIcePerGame` est disponible pour tous les joueurs |
| Retirer les colonnes inutiles (équipes, décompositions en avantage numérique, etc.) | Non pertinentes ou redondantes pour la prédiction |
| Garder `playerId`, `seasonId`, `skaterFullName` sans les utiliser comme entrées | Construction de la cible, séparation par joueur et recherche dans l'interface |
| Construire la cible `points_suivante` | Points du même joueur à la saison suivante |
| Garder seulement les saisons consécutives | Évite d'associer deux saisons éloignées (le lock-out de 2004-2005 est donc exclu) ou les saisons avec blessures |

Résultat : **18 973 lignes** après nettoyage et construction de la cible.

### Caractéristiques retenues

- **Numériques** : nombre de matchs joués : `gamesPlayed`, nombre de buts : `goals`, nombre de mentions d'aide : `assists`, nombre de tirs au but : `shots`, nombre de minutes de pénalité : `penaltyMinutes`, différentiel de la saison : `plusMinus`, temps moyen passé sur la glace par match (en secondes) : `timeOnIcePerGame`
- **Catégorielle** : position du joueur : `positionCode`
- **Cible** : `points_suivante` (régression)

## Étape 2 (entrainement)

Lors de l'entrainement, le modèle a obtenu une précision de 61% lorsqu'il a prédit les résultats avecune marge de +/- 8 points. On peut aussi le constater dans le graphique de corélation suivant (Graphiques/predit_reel.png). 
La RMSE est d'environ 13, donc on a une marge d'erreur de +/- 13 en moyenne sur les points prédits. De plus, comme le hockey est un sport complexe et imprévisible, il est compliqué de prédire à la perfection les sattistiques d'un joueur, car il y a beaucoup d'imprévisibilité.

## Étape 3 (interface)
