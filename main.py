import donnees
import Options

stats = donnees.charger_donnees("Donnees/statsPlayer.csv")
stats = donnees.garder_colonnes(stats, Options.COLONNES_UTILE)
stats = donnees.filtrer_saisons(stats, Options.SAISON_MIN)
stats = donnees.nettoyer(stats)

print(stats)