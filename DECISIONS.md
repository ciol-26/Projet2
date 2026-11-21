# Fiche de décisions
 
Projet 2 d'INF1007 (A2026), Loïc Rousseau et Jade Karaoulanis.
 
| Choix | Options envisagées | Choix retenu et justification |
|---|---|---|
| **Domaine** | Sport, jeux vidéo, immobilier | **Hockey (LNH).** Domaine qui nous intéresse, beaucoup de données publiques, question facile à comprendre pour un non-informaticien. |
| **Jeu de données** | Autres jeux de statistiques sportives sur Kaggle | **`skaters_by_season_summary.csv` (Kaggle, natashk).** 47 644 lignes, colonnes numériques et catégorielles (position), une ligne par joueur et par saison, ce qui permet de construire une cible « saison suivante ». |
| **Saisons gardées** | Toutes ; depuis 2005-2006 ; depuis 1997-1998 | **Depuis 1997-1998**, première saison où le temps de glace existe pour tous les joueurs. Plus de données qu'à partir de 2005, sans valeurs manquantes. |
| **Matchs minimum** | Aucun filtre ; 10 matchs ; 20 matchs | **Au moins 10 matchs.** Une saison de 2 ou 3 matchs donne des statistiques sans valeur ; 10 garde la majorité des joueurs. |
| **Cible** | Points de la même saison ; position (classification) ; points de la saison suivante | **`points_suivante` (régression).** Prédire les points de la même saison à partir des buts et des aides serait trivial. La position était un plan B si la cible était trop difficile à construire. |
| **Métrique** | RMSE, MAE, R² | **RMSE**, en points, donc facile à lire. Elle pénalise les grosses erreurs. On garde une seule métrique pour rester simple, calculée avec NumPy et vérifiée contre scikit-learn. |
| **Références** | Moyenne seule ; moyenne et persistance | **Les deux.** La moyenne est la référence triviale demandée (22,27). La persistance (« il refera les mêmes points », 14,68) est plus exigeante : c'est elle qu'il faut battre. |
| **Séparation** | `train_test_split` par ligne | **`train_test_split`, 80/20, graine 42.** Plus simple et vu dans l'énoncé. Limite connue et notée dans le README : un même joueur peut être des deux côtés, le score est peut-être un peu optimiste. |
| **Modèle** | Régression linéaire ; forêt aléatoire ; k plus proches voisins | **Régression linéaire.** Méthode simple et logique|
| **Technologie d'interface** | Tkinter ; PyQt ; Streamlit | **Tkinter.** Inclus avec Python, fonctionne en local, se prête bien à la POO (une classe par écran) et accepte les graphiques Matplotlib. |
| **Organisation de l'interface** | Une seule fenêtre ; plusieurs écrans | **Menu et 4 écrans** (joueur réel, statistiques, graphiques, historique), d'après notre maquette papier. Les champs sont construits à partir de `metadonnees.json`, sans colonne codée en dur. |
| **Outil du chapitre 7** | Décorateur ; générateur ; lambda | **Lambda** : clé de tri des joueurs par nom de famille et commandes des boutons. C'est là qu'il est naturel dans notre code. |
 
