# Journal des décisions

Suivi des décisions prises lors du Projet 2 d'INF1007 (Polytechnique Montréal, A2026) — Prédiction des points d'un joueur de la LNH.

---

## 1. Jeu de données — Validation B

- **Date** : 27 octobre 2026
- **Décision** : utiliser `skaters_by_season_summary.csv` du jeu « NHL Statistics » (natashk, Kaggle).
- **Justification** : grand nombre de lignes (47 644), une ligne par joueur et par saison, ce qui permet de prédire la saison suivante. Colonnes numériques et catégorielles disponibles.
Le hockey nous intéresse beaucoup, alors un projet axé sur les joueurs de la LNH peu avoir un bon potentiel, cela nous intéresse et nous motive à faire un projet de qualité.

## 2. Saisons conservées

- **Décision** : garder les saisons à partir de 1997-1998.
- **Justification** : c'est la première saison où `timeOnIcePerGame` est disponible pour tous les joueurs.

## 3. Variable cible et type de problème

- **Date** : 27 octobre 2026
- **Cible** : `points_suivante`, les points du même joueur à la saison suivante afin de prédire les points que joueur fera une saison prochaine.
- **Saisons consécutives seulement** : une saison n'est gardée que si la suivante existe pour le même joueur. Le lock-out de 2004-2005 est donc exclu.
- **Type de problème** : régression, car on prédit un nombre de points.
- **Métrique utilisée** : RMSE, exprimée en points et plus sévère pour les grosses erreurs.

## 4. Caractéristiques du modèle

- **Numériques** : `gamesPlayed`, `goals`, `assists`, `shots`, `penaltyMinutes`, `plusMinus`, `timeOnIcePerGame`
- **Catégorielle** : `positionCode`
- **Exclue — `shootsCatches`** : la main dominante n'influence pas directement la production offensive, et la retirer simplifie l'interface.
- **Exclue — `points`** : redondante, puisqu'elle vaut `goals + assists`. Elle est gardée seulement pour la référence « persistance ».
- **Exclues — `playerId`, `seasonId`, `skaterFullName`** : identifiants, utilisés pour construire la cible, séparer les données et faire la recherche.
- **Autres colonnes retirées** : équipes et décompositions (avantage numérique, etc.), jugées non pertinentes ou redondantes.


