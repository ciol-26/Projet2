import json
import os

from donnees import DonneesLNH
from interface import Application
from modele import ModeleLNH
from Options import SAISON_MIN, CARACTERISTIQUES, COLONNES_UTILE
from variables import importer_variables
from modele import ModeleLineaire, rmse

DOSSIER_MODELE = "modeles"
CHEMIN_JOBLIB = os.path.join(DOSSIER_MODELE, "modele2.joblib")
CHEMIN_META = os.path.join(DOSSIER_MODELE, "metadonnees.json")
CHEMIN_BRUT = os.path.join("Donnees", "statsPlayer.csv")
with open(CHEMIN_META, "r", encoding="utf-8") as f:
  metadonnees = json.load(f)

Application(ModeleLNH.charger(CHEMIN_JOBLIB), importer_variables(CHEMIN_META), metadonnees, DonneesLNH("Donnees/saisonDerniere.csv")).mainloop()

# donnees = DonneesLNH(os.path.join("Donnees", "statsPlayer.csv"))
# donnees.nettoyer()
# donnees.filtrer_saisons(SAISON_MIN)
# donnees.filtrer_parties(10)
# donnees = donnees.construire_cible()
# donnees.garder_colonnes(COLONNES_UTILE)
# donnees.sauvegarder(os.path.join("Donnees", "donnees_modele.csv"))

# donnees = DonneesLNH("Donnees/statsPlayer.csv")
# donnees.filtrer_saisons(20252026)
# donnees.filtrer_parties(10)
# donnees.garder_colonnes(["playerId", "seasonId", "skaterFullName", "gamesPlayed", "goals", "assists", "shots", "penaltyMinutes", "plusMinus", "positionCode", "evPoints", "ppPoints", "teamAbbrevs", "timeOnIcePerGame"])
# donnees.nettoyer()
# donnees.sauvegarder("Donnees/saisonDerniere.csv")

# cible = DonneesLNH(os.path.join("Donnees", "donnees_modele.csv"))
# X_train, X_test, y_train, y_test = cible.separer_donnees(CARACTERISTIQUES)


# modele = ModeleLineaire()
# modele.entrainer(X_train, y_train)
# rmse_modele = modele.evaluer(X_test, y_test)

# modele.sauvegarder(CHEMIN_JOBLIB, {})