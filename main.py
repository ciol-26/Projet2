"""Point d'entrée : entraîne le modèle, l'évalue, le sauvegarde et trace le graphique."""
import os

from donnees import DonneesLNH
from graphique import Graphique
from Options import SAISON_MIN, CARACTERISTIQUES
from modele import ModeleLineaire, ModeleLNH, rmse, construire_metadonnees

DOSSIER_MODELE = "modeles"
DOSSIER_GRAPHIQUES = "graphiques"

# 1. Préparer les données (à décommenter pour régénérer donnees_modele.csv)
# donnees = DonneesLNH(os.path.join("Donnees", "statsPlayer.csv"))
# donnees.nettoyer()
# donnees.filtrer_saisons(SAISON_MIN)
# donnees.filtrer_parties(10)
# donnees = donnees.construire_cible()
# donnees.sauvegarder(os.path.join("Donnees", "donnees_modele.csv"))

cible = DonneesLNH(os.path.join("Donnees", "donnees_modele.csv"))
X_train, X_test, y_train, y_test = cible.separer_donnees(CARACTERISTIQUES)

# 2. Entraîner et évaluer
#modele = ModeleLineaire()
#modele.entrainer(X_train, y_train)
#rmse_modele = modele.evaluer(X_test, y_test)

# Références : la moyenne pour tout le monde, puis « même nombre de points »
#rmse_moyenne = rmse(y_test, [y_train.mean()] * len(y_test))
#rmse_persistance = rmse(y_test, X_test["points"])

#print(f"RMSE du modèle     : {rmse_modele:.2f} points")
#print(f"RMSE de la moyenne : {rmse_moyenne:.2f} points")
#print(f"RMSE persistance   : {rmse_persistance:.2f} points")

# 3. Sauvegarder le modèle et ses métadonnées
#metriques = {"modele": rmse_modele,
 #            "moyenne": rmse_moyenne,
  #           "persistance": rmse_persistance}
#meta = construire_metadonnees(X_train, metriques)
#modele.sauvegarder(DOSSIER_MODELE, meta)

# Vérification : on recharge le modèle et on prédit un joueur du test
modele_charge = ModeleLNH.charger(DOSSIER_MODELE + "/modele.joblib")

# 4. Graphique prédit contre réel
y_pred = modele_charge.predire_lot(X_test)