import donnees
import Options

donnees = donnees.DonneesLNH("Donnees/statsPlayer.csv")
donnees.garder_colonnes(Options.COLONNES_UTILE)
donnees.filtrer_saisons(19971998)
donnees.nettoyer()

donneesModele = donnees.construire_cible()
X_train, X_test, y_train, y_test = donneesModele.separer_donnees(Options.CARACTERISTIQUES)

donnees.sauvegarder("Donnees/donnees_nettoyees.csv")
donneesModele.sauvegarder("Donnees/donnees_modele.csv")

print(donnees.dataFrame)