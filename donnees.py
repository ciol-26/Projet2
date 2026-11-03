import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class DonneesLNH:
    def __init__ (self, chemin: str = "", df: pd.DataFrame = None):
        if len(chemin): 
            with open(chemin, "r", encoding="utf-8") as f:
               self.dataFrame = pd.read_csv(f)
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
            Retourne la stucture de données 
        """
        self.dataFrame = self.dataFrame[self.dataFrame["seasonId"] >= saison_min].copy()

    def nettoyer(self):
        """ Retire les doublons et les lignes sans position
            Retourne la stucture de données 
        """
        self.dataFrame = self.dataFrame.drop_duplicates()
        self.dataFrame = self.dataFrame.dropna(subset=["positionCode"])
        #self.dataFrame = self.dataFrame.dropna(subset=["timeOnIcePerGame"])

    def construire_cible(self) -> DonneesLNH:
        """Ajoute points_suivante (points du même joueur la saison suivante).

        Ne garde que les paires de saisons consécutives. Les lignes sans
        saison suivante (dernière saison d'un joueur) sont retirées.
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
        with open(chemin, "w", encoding="utf-8", newline="") as f:
            self.dataFrame.to_csv(f, index=False)