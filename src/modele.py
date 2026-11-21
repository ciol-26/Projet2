import os
from abc import ABC, abstractmethod
from Options import (NUMERIQUES, CATEGORIELLES)

import joblib
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def rmse(y_reel, y_pred) -> float:
    ecarts = np.asarray(y_reel, dtype = float) - np.asarray(y_pred, dtype = float)
    return float(np.sqrt(np.mean(ecarts ** 2)))

def construire_metadonnees(X_train: pd.DataFrame, metriques: dict[str, float]) -> dict:
    """ Renvoie les infos dont l'interface a besoin pour se construire.
        X_train : données d'entraînement (pour les intervalles et les catégories)
        metriques : RMSE du modèle et des références
    """
    return {
        "numeriques": NUMERIQUES,
        "categorielles": CATEGORIELLES,
        "intervalles": {col: [float(X_train[col].min()), float(X_train[col].max())] for col in NUMERIQUES},
        "categories": {col: sorted(X_train[col].dropna().unique().tolist()) for col in CATEGORIELLES},
        "metriques": metriques,
    }

class ModeleLNH(ABC):
    def __init__(self):
        self._estimateur = None
        self._colonnes = None

    @abstractmethod
    def _creer_estimateur(self):
        """Renvoie l'estimateur scikit-learn."""

    def _preparer(self, X: pd.DataFrame) -> pd.DataFrame:
        """Remplit les valeurs manquantes et transforme les catégories en colonnes 0/1."""
        X = X[NUMERIQUES + CATEGORIELLES].copy()
        X = pd.get_dummies(X, columns=CATEGORIELLES)
        return X.reindex(columns=self._colonnes, fill_value=0)

    def entrainer(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Entraîne le modèle sur l'ensemble d'entraînement."""
        self._colonnes = pd.get_dummies(X_train[NUMERIQUES + CATEGORIELLES], columns=CATEGORIELLES).columns
        self._estimateur = self._creer_estimateur()
        self._estimateur.fit(self._preparer(X_train), y_train)

    def predire_lot(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit pour plusieurs lignes."""
        return self._estimateur.predict(self._preparer(X))

    def predire(self, saisie: dict) -> int:
        """Prédit les points d'un joueur à partir de {colonne: valeur}."""
        return max(0.0, int(self.predire_lot(pd.DataFrame([saisie]))[0]))

    def evaluer(self, X_test: pd.DataFrame, y_test: pd.Series) -> float:
        """Renvoie la RMSE du modèle sur l'ensemble de test."""
        return rmse(y_test, self.predire_lot(X_test))
    
    def sauvegarder(self, dossier: str, metadonnees: dict) -> None:
        """Écrit modele.joblib et metadonnees.json"""
        joblib.dump(self, dossier)
        with open(os.path.join(dossier, "metadonnees.json"), "w", encoding="utf-8") as f:
            json.dump(metadonnees, f, indent=2, ensure_ascii = False)

    @staticmethod
    def charger(chemin: str) -> ModeleLNH:
        """Recharge un modèle sauvegardé. Lève FileNotFoundError s'il manque."""
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Fichier introuvable : {chemin}")
        return joblib.load(chemin)

    def taux_reussite(self, X_test: pd.DataFrame, y_test: pd.Series, seuil: float) -> float:
        """ Renvoie le pourcentage de prédictions à moins de seuil points de la vraie valeur
            X_test, y_test : ensemble de test
            seuil : écart maximal (en points) pour qu'une prédiction compte comme réussie
        """
        ecarts = np.abs(np.asarray(y_test, dtype=float) - self.predire_lot(X_test))
        return float(np.mean(ecarts <= seuil) * 100)


class ModeleLineaire(ModeleLNH):
    def _creer_estimateur(self) -> LinearRegression:
        return LinearRegression()