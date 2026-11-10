from __future__ import annotations
from abc import ABC, abstractmethod
from exception import DonneeInvalideError
import os
import json


class Variable(ABC):
    def __init__(self, nom: str, libelle: str = "") -> None:
        """nom : nom de la colonne
           libelle : texte affiché à l'utilisateur 
        """
        self._nom = nom
        self._libelle = libelle

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def libelle(self) -> str:
        return self._libelle

    @abstractmethod
    def valider(self, texte: str):
        """ Convertit la saisie (texte) en valeur utilisable par le modèle.
            Lève DonneeInvalideError si la saisie n'est pas valide.
        """

    def __str__(self) -> str:
        return self._libelle


class VariableNumerique(Variable):
    def __init__(self, nom: str, minimum: float, maximum: float, libelle: str = "") -> None:
        super().__init__(nom, libelle)
        self._minimum = minimum
        self._maximum = maximum

    def valider(self, texte: str) -> float:
        texte = texte.strip().replace(",", ".")
        if not texte:
            raise DonneeInvalideError(f"{self._libelle} : champ vide.")
        try:
            valeur = float(texte)
        except ValueError:
            raise DonneeInvalideError(f"{self._libelle} : « {texte} » n'est pas un nombre.") from None
        if not self._minimum <= valeur <= self._maximum:
            raise DonneeInvalideError(f"{self._libelle} : doit être entre {self._minimum:g}" f"et {self._maximum:g}.")
        return valeur



class VariableCategorielle(Variable):
    def __init__(self, nom: str, valeurs: list[str], libelle: str = "") -> None:
        super().__init__(nom, libelle)
        self._valeurs = list(valeurs)

    @property
    def valeurs(self) -> list[str]:
        """Copie des valeurs permises (pour remplir une liste déroulante)."""
        return list(self._valeurs)

    def valider(self, texte: str) -> str:
        """Renvoie la saisie (en majuscules) si elle fait partie des valeurs."""
        valeur = texte.strip().upper()
        if not valeur:
            raise DonneeInvalideError(f"{self._libelle} : aucun choix.")
        if valeur not in self._valeurs:
            raise DonneeInvalideError(
                f"{self._libelle} : choisir parmi {', '.join(self._valeurs)}.")
        return valeur

def importer_variables(chemin_json: str) -> list[Variable]:
    if not os.path.exists(chemin_json):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_json}")
    
    with open(chemin_json, "r", encoding="utf-8") as f:
        meta = json.load(f)

    variables = []
    for col in meta["numeriques"]:
        minimum, maximum = meta["intervalles"][col]
        variables.append(VariableNumerique(col, minimum, maximum))
    for col in meta["categorielles"]:
        variables.append(VariableCategorielle(col, meta["categories"][col]))
    return variables