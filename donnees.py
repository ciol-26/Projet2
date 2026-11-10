import pandas as pd
from sklearn.model_selection import train_test_split
from graphique import Graphique

class DonneesLNH:
    def __init__ (self, chemin: str = "", df: pd.DataFrame = None):
        if len(chemin): 
            try:
                with open(chemin, "r", encoding="utf-8") as f:
                    self.dataFrame = pd.read_csv(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Fichier introuvable : {chemin}")
        else:
            self.dataFrame = df.copy()

    def garder_colonnes(self, colonnes: list):
        """ Retourne le tableau utile au projet
            colonnes : liste des colonnes à conserver
            Retourne la stucture de données 
        """
        self.dataFrame =  self.dataFrame[colonnes].copy()

    def filtrer_saisons(self, saison_min: int):
        """ Retenir les saisons de l'époque moderne
            saison_min : saison de départ de l'analyse de données
        """
        self.dataFrame = self.dataFrame[self.dataFrame["seasonId"] >= saison_min].copy()

    def filtrer_parties(self, partie_min: int):
        """ Retenir les saisons de plus de 10 matchs
            partie_min : nombre de parties jouées minimales
        """
        self.dataFrame = self.dataFrame[self.dataFrame["gamesPlayed"] >= partie_min].copy()

    def nettoyer(self):
        """ Retire les doublons et les lignes sans position
            Retourne la stucture de données 
        """
        self.dataFrame = self.dataFrame.drop_duplicates()
        self.dataFrame = self.dataFrame.dropna(subset=["positionCode"])
        self.dataFrame = self.dataFrame.dropna(subset=["timeOnIcePerGame"])

    def construire_cible(self) -> DonneesLNH:
        """Ajoute points_suivante (points du même joueur la saison suivante).
        """
        df = self.dataFrame.sort_values(["playerId", "seasonId"]).copy()
        groupes = df.groupby("playerId")
        df["points_suivante"] = groupes["points"].shift(-1)
        df["saison_suivante"] = groupes["seasonId"].shift(-1)
        df = df.dropna(subset=["points_suivante"])
        consecutives = df["saison_suivante"] - df["seasonId"] == 10001
        return DonneesLNH(df=df[consecutives])

    def separer_donnees(self, caracteristique: list, size : float = 0.2, state : int = 42) -> list :
        # Division des données
        x = self.dataFrame[caracteristique]
        y = self.dataFrame["points_suivante"]
        return train_test_split(x, y, test_size = size, random_state = state)

    def sauvegarder(self, chemin: str) -> None:
        """ Écrit les données dans un fichier CSV
            chemin : chemin du fichier à créer
        """
        try:
            with open(chemin, "w", encoding="utf-8", newline="") as f:
                self.dataFrame.to_csv(f, index=False)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Le dossier n'existe pas : {chemin}") from e
        except ValueError as e:
            raise ValueError(f"Format du fichier non supporté : {chemin}") from e

    def graphique_joueur(self, nom: str, colonne: str = "points") -> Graphique:
        """ Crée la courbe d'une statistique d'un joueur par saison
            nom : nom du joueur
            colonne : statistique à afficher (ex. "points", "goals")
            Retourne le graphique
        """
        joueur = self.dataFrame[self.dataFrame["skaterFullName"] == nom].sort_values("seasonId")
        if joueur.empty:
            raise ValueError(f"Joueur introuvable : {nom}")

        g = Graphique(f"{colonne} par saison", "Saison", colonne)
        g.tracer_courbe(joueur["seasonId"].astype(str), joueur[colonne], nom)
        g.axes.tick_params(axis="x", rotation = 45)
        return g

    def graphique_distribution(self, colonne: str, nb_classes: int = 20) -> Graphique:
        """ Crée l'histogramme d'une colonne
            colonne : statistique à afficher
            nb_classes : nombre de classes
            Retourne le graphique
        """
        g = Graphique(f"Distribution de {colonne}", colonne, "Nombre de joueurs")
        g.tracer_histogramme(self.dataFrame[colonne], nb_classes)
        return g