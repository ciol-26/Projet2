SAISON_MIN = 19971998

COLONNES_UTILE = ["playerId", "seasonId", "skaterFullName", "points",
                  "gamesPlayed", "goals", "assists", "shots", "penaltyMinutes", 
                  "plusMinus", "positionCode", "evPoints", "ppPoints", "teamAbbrevs", "timeOnIcePerGame"]

NUMERIQUES = ["points", "gamesPlayed", "goals", "assists", "shots",
              "penaltyMinutes", "plusMinus", "evPoints", "ppPoints", "timeOnIcePerGame"]

CATEGORIELLES = ["positionCode"]

CARACTERISTIQUES = NUMERIQUES + CATEGORIELLES