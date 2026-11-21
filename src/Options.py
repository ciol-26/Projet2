SAISON_MIN = 19971998

COLONNES_UTILE = ["playerId", "seasonId", "skaterFullName", "gamesPlayed", "goals", "assists", "shots", "penaltyMinutes", 
                  "plusMinus", "positionCode", "evPoints", "ppPoints", "teamAbbrevs", "timeOnIcePerGame", "points_suivante"]

NUMERIQUES = ["gamesPlayed", "goals", "assists", "shots",
              "penaltyMinutes", "plusMinus", "evPoints", "ppPoints", "timeOnIcePerGame"]

CATEGORIELLES = ["positionCode"]

CARACTERISTIQUES = NUMERIQUES + CATEGORIELLES