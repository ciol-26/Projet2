import donnees
import Options

df = donnees.DonneesLNH("Donnees/statsPlayer.csv")
df.garder_colonnes(Options.COLONNES_UTILE)
df.filtrer_saisons(19971998)
df.filtrer_parties(10)
df.nettoyer()

donneesModele = df.construire_cible()
X_train, X_test, y_train, y_test = donneesModele.separer_donnees(Options.CARACTERISTIQUES)

df.sauvegarder("Donnees/donnees_nettoyees.csv")
donneesModele.sauvegarder("Donnees/donnees_modele.csv")

g = df.graphique_joueur("Arber Xhekaj", "penaltyMinutes")
g.afficher()
g.sauvegarder("Graphiques/points.png")

print(df.dataFrame)
print(donneesModele.dataFrame)