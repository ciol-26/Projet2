import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import train_test_split, cross_val_score

def charger_donnees(chemin: str) -> pd.DataFrame:
    """ Charger les données du projet
        chemin : chemin pour accéder au fichier
        Retourne la structure de données
    """
    return pd.read_csv(chemin)

def garder_colonnes(df: pd.DataFrame, colonnes: list) -> pd.DataFrame:
    """ Retourne le tableau utile au projet
        df : structure de données
        colonnes : liste des colonnes à conserver
        Retourne la stucture de données 
    """
    return df[colonnes].copy()

def filtrer_saisons(df: pd.DataFrame, saison_min: int) -> pd.DataFrame:
    """ Retenir les saisons de l'époque moderne
        df : structure de données
        saison_min : saison de départ de l'analyse de données
        Retourne la stucture de données 
    """
    return df[df["seasonId"] >= saison_min].copy()

def nettoyer(df: pd.DataFrame) -> pd.DataFrame:
    """ Retire les doublons et les lignes sans position
        df : structure de données
        Retourne la stucture de données 
    """
    df = df.drop_duplicates()
    df = df.dropna(subset=["positionCode"])
    #df = df.dropna(subset=["timeOnIcePerGame"])
    return df

def construire_cible(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute points_suivante (points du même joueur la saison suivante).

    Ne garde que les paires de saisons consécutives. Les lignes sans
    saison suivante (dernière saison d'un joueur) sont retirées.
    """
    df = df.sort_values(["playerId", "seasonId"]).copy()
    groupes = df.groupby("playerId")
    df["points_suivante"] = groupes["points"].shift(-1)
    df["saison_suivante"] = groupes["seasonId"].shift(-1)
    df = df.dropna(subset=["points_suivante"])
    return df[df["saison_suivante"] - df["seasonId"] == 10001].copy()


def diviserdonnees(df: pd.DataFrame, caracteristique: list, test_size : float = 0.2, random_state : int = 42) :
    # Division des données
    x = df[caracteristique]
    y = df["points_suivante"]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size, random_state)
    return X_train, X_test, y_train, y_test
