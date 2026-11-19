import csv
import math
import os
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from donnees import DonneesLNH
from exception import DonneeInvalideError
from graphique import Graphique
from variables import Variable, VariableCategorielle, VariableNumerique

TITRE = "Prédicteur de statistiques de joueurs de hockey"
TOUTES = "Toutes les équipes"
MAX_SUGGESTIONS = 200
POLICE = "Arial"
CHEMIN_HISTORIQUE = os.path.join("historique", "predictions.csv")


class Ecran(tk.Frame):

    COULEURS = {
        "fond": "#F1F5F9",          # arrière-plan de l'écran
        "carte": "#FFFFFF",         # intérieur des cartes
        "bordure": "#CBD5E1",       # contour des cartes et des champs
        "entete": "#0F172A",        # bande de titre
        "accent": "#2563EB",        # boutons principaux et gros chiffre
        "accent_fonce": "#1D4ED8",  # bouton survolé ou enfoncé
        "texte": "#0F172A",
        "gris": "#64748B",          # textes secondaires
    }

    def __init__(self, app, titre: str, retour: bool = True) -> None:
        """ Constructeur
            app : Fenêtre de l'écran
            titre : titre de l'écran dans l'entête
            retour : bouton de retour du menu
        """
        super().__init__(app, bg=self.COULEURS["fond"])
        self._app = app
        c = self.COULEURS

        # Entête =>
        entete = tk.Frame(self, bg=c["entete"], padx=20, pady=12)
        entete.pack(fill="x")
        if retour:
            tk.Button(entete, text="Menu", font=(POLICE, 10), relief="flat", bg=c["accent"], fg="white", padx=12, pady=3, activebackground=c["accent_fonce"], activeforeground="white", command=lambda: app.afficher("menu")).pack(side="left")
        tk.Label(entete, text=titre, bg=c["entete"], fg="white", font=(POLICE, 15, "bold")).pack(side="left", padx=15)

        # Corps => contenu de l'écran
        self.corps = tk.Frame(self, bg=c["fond"], padx=24, pady=24)
        self.corps.pack(fill="both", expand=True)

    def creer_carte(self, cadre: tk.Misc, titre: str = "") -> tk.Frame:
        """ Crée une carte blanche avec bordure et un titre facultatif.
            cadre : cadre où l'on met le widget (tk.Misc = n'importe quel widget)
            titre : le titre du cadre
        """
        c = self.COULEURS
        carte = tk.Frame(cadre, bg=c["carte"], padx=18, pady=18, highlightthickness=1, highlightbackground=c["bordure"], highlightcolor=c["bordure"])
        if titre:
            self.etiquette(carte, titre, taille=12, gras=True).pack(anchor="w", pady=(0, 12))
        return carte

    def etiquette(self, cadre: tk.Misc, texte: str = "", fond: str = "carte", couleur: str = "texte", taille: int = 10, gras: bool = False) -> tk.Label:
        """ Crée une étiquette. fond et couleur sont des clés de COULEURS.
            cadre : Position dans l'écran
            texte : texte à afficher
            fond : couleur de fond (clé du dictionnaire)
            couleur : clé pour obtenir la couleur du texte
            taille : taille de la police
            gras : vrai = texte en gras 
        """
        try:
            label = tk.Label(cadre, text=texte, bg=self.COULEURS[fond], fg=self.COULEURS[couleur], font=(POLICE, taille, "bold" if gras else "normal"))
        except IndexError:
            raise IndexError("Couleur introuvable")
        return label

    def bouton(self, cadre: tk.Misc, texte: str, commande) -> tk.Button:
        """ Crée un bouton principal
            cadre : Position dans l'écran
            texte : Texte dans le bouton (en blanc)
            commande : La fonction que le bouton appelle
        """
        c = self.COULEURS
        try:
            bouton = tk.Button(cadre, text=texte, command=commande, relief="flat", bg=c["accent"], fg="white", font=(POLICE, 11, "bold"), activebackground=c["accent_fonce"], activeforeground="white", padx=24, pady=8, cursor="hand2")
        except IndexError:
            raise IndexError("Couleur introuvable")
        return bouton
    
    def champ(self, cadre: tk.Misc, variable: tk.StringVar, largeur: int) -> tk.Entry:
        """ Crée une zone de texte reliée à variable.
            cadre : Position dans l'écran
            variable : variable qui est dans le champ
            largeur : largeur du champ
        """
        c = self.COULEURS
        return tk.Entry(cadre, textvariable=variable, width=largeur, font=(POLICE, 10), relief="flat", bg="white", fg=c["texte"], highlightthickness=1, highlightbackground=c["bordure"], highlightcolor=c["accent"])

    def menu_deroulant(self, cadre: tk.Misc, variable: tk.StringVar, valeurs: list[str], commande=None) -> tk.OptionMenu:
        """ Crée une liste déroulante
            cadre : Position dans l'écran
            variable : le choix actuel
            valeurs : la liste des choix
            commande : fonction appelée lorsqu'on choisi une valeur
        """
        c = self.COULEURS
        menu = tk.OptionMenu(cadre, variable, *valeurs, command=commande)
        menu.config(font=(POLICE, 10), bg="white", fg=c["texte"], anchor="w", activebackground=c["fond"], relief="flat", highlightthickness=1, highlightbackground=c["bordure"])
        menu["menu"].config(font=(POLICE, 10), bg="white")
        return menu

    def enregistrer_prediction(self, joueur: str, points: int, entree: dict) -> None:
        """ Ajoute une prédiction à l'historique en mémoire.
            joueur : le nom afficher dans l'historique
            points : les points prévus par le modèle
            entree : le dictionnaire de statistiques envoyés au modèle
        """
        ligne = {"joueur": joueur, "points": int(entree["goals"] + entree["assists"]), "prediction": points, **entree}
        self._app.historique.append(ligne)

    def quand_affiche(self) -> None:
        """Appelée chaque fois que l'écran est affiché"""
        pass


class CadreResultat(tk.Frame):
    def __init__(self, cadre: tk.Misc, ecran: Ecran) -> None:
        """ Constructeur
            cadre : Position dans l'écran
            écran : Écran ou se trouve le cadre
        """
        c = ecran.COULEURS
        super().__init__(cadre, bg=c["carte"], padx=18, pady=18, highlightthickness=1, highlightbackground=c["bordure"], highlightcolor=c["bordure"])
        ecran.etiquette(self, "Points prévus la saison prochaine", couleur="gris").pack()
        self._nombre = ecran.etiquette(self, "—", couleur="accent", taille=60, gras=True)
        self._nombre.pack()
        self._marge = ecran.etiquette(self)
        self._marge.pack()
        self._contexte = ecran.etiquette(self, couleur="gris")
        self._contexte.pack(pady=(8, 0))

    def afficher(self, points: float, marge: float, contexte: str = "") -> None:
        """ Affiche les points prévus, la marge d'erreur et un contexte
            points : Points prédits
            marge : Marge d'erreur du modèle
            contexte : Taxte à afficher sous le résultat
        """
        self._nombre.config(text=f"{points:.0f}")
        self._marge.config(text=f"marge d'erreur du modèle : ± {marge:.0f} points")
        self._contexte.config(text=contexte)

class EcranMenu(Ecran):
    BOUTONS = [("Prédire à partir d'un joueur réel", "joueur"),
               ("Prédire à partir de statistiques", "statistiques"),
               ("Concevoir des graphiques", "graphique"),
               ("Consulter l'historique", "historique")]

    def __init__(self, app) -> None:
        """ Constructeur
            app : Fenêtre ou se trouve cet écran
        """
        super().__init__(app, TITRE, retour=False)
        c = self.COULEURS
        self.etiquette(self.corps, "Que voulez-vous faire ?", fond="fond", taille=20, gras=True).pack(pady=(30, 4))
        self.etiquette(self.corps, "Estimez les points d'un joueur de la LNH " "pour la saison suivante.", fond="fond", couleur="gris", taille=11).pack(pady=(0, 28))

        for texte, ecran in self.BOUTONS:
            tk.Button(self.corps, text=texte, width=36, font=(POLICE, 12), bg=c["carte"], fg=c["texte"], relief="solid", bd=1, activebackground=c["fond"], pady=12, cursor="hand2", command=lambda e=ecran: app.afficher(e)).pack(pady=7)


class EcranJoueur(Ecran):
    def __init__(self, app) -> None:
        """ Constructeur
            app : Fenêtre ou se trouve cet écran
        """
        super().__init__(app, "Prédire à partir d'un joueur réel")
        c = self.COULEURS
        gauche = self.creer_carte(self.corps, "Choisir un joueur")
        gauche.pack(side="left", fill="y")
        self._resultat = CadreResultat(self.corps, self)
        self._resultat.pack(side="left", fill="both", expand=True, padx=(20, 0))

        # Filtre par équipe
        self.etiquette(gauche, "Équipe", couleur="gris").pack(anchor="w")
        self._equipe = tk.StringVar(value=TOUTES)
        self.menu_deroulant(gauche, self._equipe, [TOUTES] + app.equipes(), commande=lambda _: self._filtrer()).pack(fill="x", pady=(2, 10))

        # Nom du joueur : la liste se met à jour à chaque lettre tapée
        self.etiquette(gauche, "Nom du joueur", couleur="gris").pack(anchor="w")
        self._nom = tk.StringVar()
        self._nom.trace_add("write", lambda *_: self._filtrer())
        champ = self.champ(gauche, self._nom, 34)
        champ.pack(fill="x", pady=(2, 4), ipady=3)
        champ.bind("<Return>", lambda _: self._predire())
        champ.bind("<Down>", lambda _: self._aller_a_la_liste())

        # Suggestions
        cadre_liste = tk.Frame(gauche, bg=c["carte"])
        cadre_liste.pack(fill="x")
        self._suggestions = tk.Listbox(cadre_liste, height=10, font=(POLICE, 10), activestyle="none", relief="flat", highlightthickness=0, bg=c["carte"], fg=c["texte"], selectbackground=c["accent"], selectforeground="white")
        defilement = tk.Scrollbar(cadre_liste, command=self._suggestions.yview)
        self._suggestions.config(yscrollcommand=defilement.set)
        self._suggestions.pack(side="left", fill="x", expand=True)
        defilement.pack(side="left", fill="y")
        self._suggestions.bind("<<ListboxSelect>>", lambda _: self._choisir())
        self._suggestions.bind("<Double-Button-1>", lambda _: self._predire())
        self._suggestions.bind("<Return>", lambda _: self._predire())

        self.bouton(gauche, "Prédire", self._predire).pack(pady=(14, 0))
        self._filtrer()

    def _filtrer(self) -> None:
        """Remplit la liste avec les joueurs qui correspondent au texte et à l'équipe."""
        equipe = self._equipe.get()
        noms = self._app.noms_joueurs(self._nom.get(), "" if equipe == TOUTES else equipe)
        self._suggestions.delete(0, "end")
        for nom in noms[:MAX_SUGGESTIONS]:
            self._suggestions.insert("end", nom)

    def _choisir(self) -> None:
        """Copie le nom sélectionné dans le champ."""
        selection = self._suggestions.curselection()
        if selection:
            self._nom.set(self._suggestions.get(selection[0]))

    def _aller_a_la_liste(self) -> None:
        """Flèche du bas : passe du champ à la première suggestion."""
        if self._suggestions.size():
            self._suggestions.focus_set()
            self._suggestions.selection_set(0)
            self._suggestions.activate(0)

    def _predire(self) -> None:
        """Cherche le joueur, prédit ses points, les enregistre et les affiche."""
        nom = self._nom.get().strip()
        try:
            entree = self._app.chercher_joueur(nom)
        except DonneeInvalideError as erreur:
            messagebox.showerror("Joueur introuvable", str(erreur))
            return
        points = self._app.predire(entree)
        self.enregistrer_prediction(nom, points, entree)
        self._resultat.afficher(points, self._app.marge, f"{nom}\nd'après sa saison 2025-2026")


class EcranStatistiques(Ecran):
    def __init__(self, app, variables: list[Variable]) -> None:
        """ Constructeur
            app : Fenêtre ou se trouve cet écran
            variables : liste de variables pour faire des prédictions
        """
        super().__init__(app, "Prédire à partir de statistiques")
        self._variables = variables
        self._textes = {}

        carte = self.creer_carte(self.corps, "Statistiques de la saison actuelle")
        carte.pack(fill="x")
        grille = tk.Frame(carte, bg=self.COULEURS["carte"])
        grille.pack()
        par_colonne = math.ceil(len(variables) / 2)
        for i, variable in enumerate(variables):
            ligne, colonne = i % par_colonne, 2 * (i // par_colonne)
            self.etiquette(grille, variable.libelle).grid(
                row=ligne, column=colonne, sticky="e", padx=(20, 8), pady=4)
            texte = tk.StringVar()
            if isinstance(variable, VariableCategorielle):
                champ = self.menu_deroulant(grille, texte, variable.valeurs)
                champ.config(width=11)
            else:
                champ = self.champ(grille, texte, 15)
            champ.grid(row=ligne, column=colonne + 1, sticky="w", pady=4, ipady=2)
            self._textes[variable.nom] = texte

        bas = tk.Frame(self.corps, bg=self.COULEURS["fond"])
        bas.pack(fill="both", expand=True, pady=(20, 0))
        self.bouton(bas, "Prédire", self._predire).pack(side="left", anchor="n")
        self._resultat = CadreResultat(bas, self)
        self._resultat.pack(side="left", fill="both", expand=True, padx=(20, 0))

    def lire(self) -> dict:
        """ Valide chaque champ et la cohérence entre eux, puis renvoie {colonne: valeur}.
        """
        entree = {v.nom: v.valider(self._textes[v.nom].get()) for v in self._variables}
        if entree["goals"] > entree["shots"]:
            raise DonneeInvalideError("Il y a plus de buts que de tirs au but.")
        if entree["evPoints"] + entree["ppPoints"] > entree["goals"] + entree["assists"]:
            raise DonneeInvalideError( "Les points à forces égales et en avantage numérique dépassent " "le total des buts et des aides.")
        return entree

    def _predire(self) -> None:
        """Lit le formulaire, prédit, enregistre et affiche le résultat."""
        try:
            entree = self.lire()
        except DonneeInvalideError as erreur:
            messagebox.showerror("Saisie invalide", str(erreur))
            return
        points = self._app.predire(entree)
        self.enregistrer_prediction("Joueur fictif", points, entree)
        self._resultat.afficher(points, self._app.marge)


class EcranGraphique(Ecran):
    def __init__(self, app, variables: list[Variable]) -> None:
        """ Constructeur
            app : Fenêtre ou se trouve cet écran
            variables : liste de variables pour faire des prédictions
        """
        super().__init__(app, "Concevoir des graphiques")
        self._par_libelle = {v.libelle: v.nom for v in variables if isinstance(v, VariableNumerique)}
        self._canevas = None

        barre = tk.Frame(self.corps, bg=self.COULEURS["fond"])
        barre.pack(fill="x", pady=(0, 14))
        self.etiquette(barre, "Statistique à observer", fond="fond").pack(side="left")
        self._choix = tk.StringVar()
        menu = self.menu_deroulant(barre, self._choix, list(self._par_libelle), commande=lambda _: self._tracer())
        menu.config(width=28)
        menu.pack(side="left", padx=10)

        self._carte = self.creer_carte(self.corps)
        self._carte.pack(fill="both", expand=True)
        self._accueil = self.etiquette(self._carte, "Choisissez une statistique pour voir\n" "sa distribution chez tous les joueurs.", couleur="gris")
        self._accueil.pack(expand=True)

    def _tracer(self) -> None:
        """Demande le graphique de la statistique choisie à DonneesLNH et l'affiche."""
        libelle = self._choix.get()
        if not libelle:
            messagebox.showerror("Aucun choix", "Choisissez une statistique.")
            return
        g = self._app.graphique_distribution(self._par_libelle[libelle], libelle)
        self._afficher(g)

    def _afficher(self, g: Graphique) -> None:
        """ Remplace le graphique affiché par celui de g.
            g: Graphique à afficher
        """
        self._accueil.pack_forget()
        if self._canevas is not None:
            self._canevas.get_tk_widget().destroy()
        self._canevas = FigureCanvasTkAgg(g.figure, master=self._carte)
        self._canevas.draw()
        widget = self._canevas.get_tk_widget()
        widget.config(highlightthickness=0)
        widget.pack(fill="both", expand=True)


class EcranHistorique(Ecran):
    COLONNES = [("joueur", "Joueur"),
                ("points", "Points (saison actuelle)"),
                ("prediction", "Points prévus")]
    TAQUETS = (260, 470)

    def __init__(self, app) -> None:
        """ Constructeur
            app : Fenêtre où se trouve cet écran
        """
        super().__init__(app, "Historique des prédictions")
        c = self.COULEURS
        carte = self.creer_carte(self.corps)
        carte.pack(fill="both", expand=True)

        cadre_liste = tk.Frame(carte, bg=c["carte"])
        cadre_liste.pack(fill="both", expand=True)
        self._tableau = tk.Text(cadre_liste, font=(POLICE, 10), relief="flat", highlightthickness=0, bg=c["carte"], fg=c["texte"], tabs=self.TAQUETS, spacing1=3, spacing3=3)
        self._tableau.tag_config("entete", font=(POLICE, 10, "bold"))
        defilement = tk.Scrollbar(cadre_liste, command=self._tableau.yview)
        self._tableau.config(yscrollcommand=defilement.set)
        self._tableau.pack(side="left", fill="both", expand=True)
        defilement.pack(side="left", fill="y")

        self._message = self.etiquette(self.corps, fond="fond", couleur="gris")
        self._message.pack(anchor="w", pady=(10, 0))

    def quand_affiche(self) -> None:
        self._tableau.config(state="normal")
        self._tableau.delete("1.0", "end")

        entete = "\t".join(titre for _, titre in self.COLONNES)
        self._tableau.insert("end", entete + "\n", "entete")

        lignes = self._app.historique
        for ligne in reversed(lignes):
            texte = "\t".join(str(ligne.get(cle, "")) for cle, _ in self.COLONNES)
            self._tableau.insert("end", texte + "\n")

        self._tableau.config(state="disabled")
        self._message.config(text=f"{len(lignes)} prédiction(s)" if lignes else "Aucune prédiction pour l'instant.")


class Application(tk.Tk):
    def __init__(self, modele, variables: list[Variable], metadonnees: dict, donnees: DonneesLNH) -> None:
        """ Constructeur
            modele : modele qui fait les prédiction
            variables : liste des variables que le modèle analyse
            metadonnees : donnees du modèle
            donnees : donnees de la saison dernière
        """
        super().__init__()
        self.title(TITRE)
        self.geometry("900x680")
        self.minsize(820, 600)
        self.protocol("WM_DELETE_WINDOW", self._fermer)

        self._modele = modele
        self._variables = variables
        self._donnees = donnees
        self._marge = metadonnees["metriques"]["modele"]
        self.historique: list[dict] = self._charger_historique()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._ecrans = {
            "menu": EcranMenu(self),
            "joueur": EcranJoueur(self),
            "statistiques": EcranStatistiques(self, variables),
            "graphique": EcranGraphique(self, variables),
            "historique": EcranHistorique(self),
        }

        for ecran in self._ecrans.values():
            ecran.grid(row=0, column=0, sticky="nsew")
        self.afficher("menu")

    @property
    def marge(self) -> float:
        """Marge d'erreur typique du modèle (RMSE), en points."""
        return self._marge

    def afficher(self, nom: str) -> None:
        """Place l'écran demandé par-dessus les autres et le met à jour."""
        self._ecrans[nom].tkraise()
        self._ecrans[nom].quand_affiche()

    def chercher_joueur(self, nom: str) -> dict:
        """Renvoie les statistiques du joueur. Lève DonneeInvalideError s'il est introuvable."""
        colonnes = [v.nom for v in self._variables]
        return self._donnees.stats_joueur(nom, colonnes)

    def equipes(self) -> list[str]:
        """Renvoie les abréviations des équipes, en ordre alphabétique."""
        return self._donnees.equipes()

    def noms_joueurs(self, texte: str, equipe: str) -> list[str]:
        """Renvoie les joueurs dont le nom contient texte (et de l'équipe donnée)."""
        return self._donnees.noms_joueurs(texte, equipe)

    def graphique_distribution(self, colonne: str, libelle: str) -> Graphique:
        """Renvoie l'histogramme de la colonne, construit par DonneesLNH."""
        return self._donnees.graphique_distribution(colonne, libelle)

    def predire(self, entree: dict) -> int:
        """Appelle le modèle et renvoie les points prévus, arrondis."""
        return round(self._modele.predire(entree))

    def _charger_historique(self) -> list[dict]:
        """Lit le CSV d'historique une seule fois. Renvoie [] s'il n'existe pas."""
        if not os.path.exists(CHEMIN_HISTORIQUE):
            return []
        with open(CHEMIN_HISTORIQUE, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def _fermer(self) -> None:
        """Enregistre l'historique dans le CSV, puis ferme complètement l'application."""
        try:
            if self.historique:
                os.makedirs(os.path.dirname(CHEMIN_HISTORIQUE), exist_ok=True)
                with open(CHEMIN_HISTORIQUE, "w", encoding="utf-8", newline="") as f:
                    ecrivain = csv.DictWriter(f, fieldnames=list(self.historique[0]), extrasaction="ignore")
                    ecrivain.writeheader()
                    ecrivain.writerows(self.historique)
        except (PermissionError, ValueError) as erreur:
            messagebox.showwarning("Historique", f"Impossible d'enregistrer l'historique : {erreur}")
        
        plt.close("all")
        self.quit()
        self.destroy()