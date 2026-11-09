import matplotlib.pyplot as plt

class Graphique:
    def __init__(self, titre: str, etiquette_x: str, etiquette_y: str, taille: tuple = (8, 5)):
        """ Crée un graphique vide
            titre : titre du graphique
            etiquette_x, etiquette_y : noms des axes
            taille : (largeur, hauteur)
        """
        self.figure, self.axes = plt.subplots(figsize=taille)
        self.titre = titre
        self.etiquette_x = etiquette_x
        self.etiquette_y = etiquette_y
        self.axes.set_title(self.titre)
        self.axes.set_xlabel(self.etiquette_x)
        self.axes.set_ylabel(self.etiquette_y)

    def tracer_courbe(self, x, y, legende: str = "") -> None:
        """ Trace une courbe 
            x: variable en x
            y: variable en y
            legende: identifier le graphique
        """
        self.axes.plot(x, y, marker = "o", label = legende)
        if legende:
            self.axes.legend()

    def tracer_nuage(self, x, y, legende: str = "") -> None:
        """ Trace un nuage de points 
            x: variable en x
            y: variable en y
            legende: identifier le graphique
        """
        self.axes.scatter(x, y, alpha = 0.5, label = legende)
        if legende:
            self.axes.legend()

    def tracer_histogramme(self, valeurs, nb_classes: int = 20) -> None:
        """ Trace la distribution d'une colonne
            valeurs: variable à observer
            nb_classes: nombre de classes sur l'axe des x 
        """
        self.axes.hist(valeurs, bins=nb_classes, edgecolor="black")

    def ajouter_diagonale(self) -> None:
        """ Ajoute la droite y = x 
        """
        bas, haut = self.axes.get_xlim()
        self.axes.plot([bas, haut], [bas, haut], "r--", label="Prédiction parfaite")
        self.axes.legend()

    def effacer(self) -> None:
        """ Vide le graphique en gardant le titre et les axes """
        self.axes.clear()
        self.axes.set_title(self.titre)
        self.axes.set_xlabel(self.etiquette_x)
        self.axes.set_ylabel(self.etiquette_y)

    def sauvegarder(self, chemin: str) -> None:
        """ Enregistre le graphique en image en .png 
            chemin: Répertoire où enregistrer l'image
        """
        try:
            with open(chemin, "wb") as f:
                self.figure.savefig(f, format=chemin.split(".")[-1], bbox_inches="tight")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Le dossier n'existe pas : {chemin}") from e
        except ValueError as e:
            raise ValueError(f"Format d'image non supporté : {chemin}") from e
        
    def afficher(self) -> None:
        """ Affiche le graphique dans une fenêtre """
        plt.show()
    



    
