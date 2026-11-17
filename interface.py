import math
import tkinter as tk
import csv
import os
from tkinter import ttk, messagebox

from graphique import Graphique
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from donnees import DonneesLNH
from exception import DonneeInvalideError
from variables import Variable, VariableCategorielle, VariableNumerique

TITRE = "Prédicteur de statistiques de joueurs de hockey"
TOUTES = "Toutes les équipes"
MAX_SUGGESTIONS = 200
POLICE = "Arial"
CHEMIN_HISTORIQUE = os.path.join("historique", "predictions.csv")


def appliquer_style(racine: tk.Tk) -> None:
    """Réglages communs à toute l'application (thème, police par défaut)."""
    style = ttk.Style(racine)
    style.theme_use("clam")
    racine.option_add("*TCombobox*Listbox.font", (POLICE, 10))
    style.configure(".", font=(POLICE, 10))
    for nom in ("TEntry", "TCombobox"): style.configure(nom, fieldbackground = "white", padding = 5)
    style.map("TCombobox", fieldbackground=[("readonly", "white")], selectbackground=[("readonly", "white")], selectforeground=[("readonly", "#0F172A")])


class Ecran(ttk.Frame):
    COULEURS = {
        "fond": "#F1F5F9",
        "carte": "#FFFFFF",
        "bordure": "#CBD5E1",
        "entete": "#0F172A",
        "entete_bouton": "#1E293B",
        "accent": "#2563EB",
        "accent_fonce": "#1D4ED8",
        "accent_pale": "#DBEAFE",
        "texte": "#0F172A",
        "gris": "#64748B",
        "repere": "#DC2626",
    }

    FORMES = {
        "relief_carte": "solid",
        "epaisseur_bordure": 1,
        "marge_carte": 18,
        "marge_ecran": 24,
        "bouton": (24, 9),
        "taille_titre": 15,
        "taille_nombre": 40,
    }

    def __init__(self, app: "Application", titre: str, retour: bool = True) -> None:
        """Crée les styles de l'écran, la bande de titre et self.corps."""
        self._app = app
        self._prefixe = type(self).__name__
        self._creer_styles()
        super().__init__(app, style=self.st("TFrame"))

        entete = ttk.Frame(self, style = self.st("Entete.TFrame"), padding = (20, 14))
        entete.pack(fill = "x")
        if retour:
            ttk.Button(entete, text = "Menu", style = self.st("Retour.TButton"), cursor = "hand2", command = lambda: app.afficher("menu")).pack(side="left")
        ttk.Label(entete, text=titre, style=self.st("Entete.TLabel")).pack(side="left", padx=15)
        self.corps = ttk.Frame(self, style=self.st("TFrame"), padding=self.FORMES["marge_ecran"])
        self.corps.pack(fill="both", expand=True)

    def st(self, nom: str) -> str:
        """Renvoie le nom du style propre à cet écran"""
        return f"{self._prefixe}.{nom}"

    def _creer_styles(self) -> None:
        c = self.COULEURS 
        f = self.FORMES
        style = ttk.Style(self._app)
        conf = lambda nom, **options: style.configure(self.st(nom), **options)

        conf("TFrame", background=c["fond"])
        conf("TLabel", background=c["fond"], foreground=c["texte"])
        conf("Gris.TLabel", background=c["fond"], foreground=c["gris"])
        conf("Sous.TLabel", background=c["fond"], foreground=c["gris"], font=(POLICE, 11))
        conf("Grand.TLabel", background=c["fond"], foreground=c["texte"], font=(POLICE, 20, "bold"))

        conf("Entete.TFrame", background=c["entete"])
        conf("Entete.TLabel", background=c["entete"], foreground="white", font=(POLICE, f["taille_titre"], "bold"))
        conf("Retour.TButton", background=c["entete_bouton"], foreground="white", borderwidth=0, padding=(12, 6))
        style.map(self.st("Retour.TButton"), background=[("active", c["accent"])])

        conf("Carte.TFrame", background=c["carte"], relief=f["relief_carte"], borderwidth=f["epaisseur_bordure"], bordercolor=c["bordure"], lightcolor=c["bordure"], darkcolor=c["bordure"])
        conf("Grille.TFrame", background=c["carte"])
        conf("Carte.TLabel", background=c["carte"], foreground=c["texte"])
        conf("CarteTitre.TLabel", background=c["carte"], foreground=c["texte"], font=(POLICE, 12, "bold"))
        conf("CarteGris.TLabel", background=c["carte"], foreground=c["gris"])
        conf("Nombre.TLabel", background=c["carte"], foreground=c["accent"], font=(POLICE, f["taille_nombre"], "bold"))

        conf("Accent.TButton", background=c["accent"], foreground="white", borderwidth=0, padding=f["bouton"], font=(POLICE, 11, "bold"))
        style.map(self.st("Accent.TButton"), background=[("pressed", c["accent_fonce"]), ("active", c["accent_fonce"])])

        conf("Menu.TButton", background=c["carte"], foreground=c["texte"], bordercolor=c["bordure"], borderwidth=f["epaisseur_bordure"], padding=(20, 16), font=(POLICE, 12))
        style.map(self.st("Menu.TButton"), background=[("active", c["accent_pale"])], bordercolor=[("active", c["accent"])])

        for nom in ("TEntry", "TCombobox"):
            conf(nom, bordercolor=c["bordure"], lightcolor=c["bordure"], darkcolor=c["bordure"])
            style.map(self.st(nom), bordercolor=[("focus", c["accent"])], lightcolor=[("focus", c["accent"])])

    def creer_carte(self, parent: tk.Misc, titre: str = "") -> ttk.Frame:
        """Crée une carte aux couleurs de l'écran, avec un titre facultatif."""
        carte = ttk.Frame(parent, style=self.st("Carte.TFrame"), padding=self.FORMES["marge_carte"])
        if titre:
            ttk.Label(carte, text=titre, style=self.st("CarteTitre.TLabel")).pack(anchor="w", pady=(0, 12))
        return carte
    
    def enregistrer_prediction(self, joueur: str, points: int, entree: dict) -> None:
        """Ajoute la prédiction à la fin du CSV d'historique (crée le fichier au besoin)."""
        ligne = {"joueur": joueur,
             "points": int(entree["goals"] + entree["assists"]),
             "prediction": points,
             **entree}
        self._app.historique.append(ligne)

    def quand_affiche(self):
        """Appelée chaque fois que l'écran est affiché. Ne fait rien par défaut."""


class CadreResultat(ttk.Frame):
    """Carte qui affiche une prédiction en gros chiffres."""

    def __init__(self, parent: tk.Misc, ecran: Ecran) -> None:
        """Crée la carte avec les styles de l'écran qui la contient."""
        super().__init__(parent, style=ecran.st("Carte.TFrame"), padding=ecran.FORMES["marge_carte"])
        ttk.Label(self, text="Points prévus la saison prochaine", style=ecran.st("CarteGris.TLabel")).pack()
        self._nombre = ttk.Label(self, text="—", style=ecran.st("Nombre.TLabel"))
        self._nombre.pack()
        self._marge = ttk.Label(self, text="", style=ecran.st("Carte.TLabel"))
        self._marge.pack()
        self._contexte = ttk.Label(self, text="", wraplength=260, justify="center", style=ecran.st("CarteGris.TLabel"))
        self._contexte.pack(pady=(8, 0))

    def afficher(self, points: float, marge: float, contexte: str = "") -> None:
        """Affiche les points prévus, la marge d'erreur et un contexte."""
        self._nombre.config(text=f"{points:.0f}")
        self._marge.config(text=f"marge d'erreur du modèle : ± {marge:.0f} points")
        self._contexte.config(text=contexte)


class EcranMenu(Ecran):
    """Menu principal avec un bouton par fonctionnalité."""

    def __init__(self, app: "Application") -> None:
        super().__init__(app, TITRE, retour=False)
        ttk.Label(self.corps, text="Que voulez-vous faire ?", style=self.st("Grand.TLabel")).pack(pady=(30, 4))
        ttk.Label(self.corps, style=self.st("Sous.TLabel"), text="Estimez les points d'un joueur de la LNH pour la saison suivante.").pack(pady=(0, 28))

        boutons = [("Prédire à partir d'un joueur réel", "joueur"),
                   ("Prédire à partir de statistiques", "statistiques"),
                   ("Concevoir des graphiques", "graphique"),
                   ("Consulter l'historique", "historique")]
        
        for texte, ecran in boutons:
            ttk.Button(self.corps, text=texte, style=self.st("Menu.TButton"), width=36, cursor="hand2", command=lambda e=ecran: app.afficher(e)).pack(pady=7)

class EcranHistorique(Ecran):
    COLONNES = {"joueur": "Joueur", "points": "Points (saison précédente)", "prediction": "Points prévus"}

    def __init__(self, app: "Application") -> None:
        super().__init__(app, "Historique des prédictions")
        carte = self.creer_carte(self.corps)
        carte.pack(fill="both", expand=True)

        self._tableau = ttk.Treeview(carte, columns=list(self.COLONNES), show="headings", height=15)
        for cle, titre in self.COLONNES.items():
            self._tableau.heading(cle, text=titre)
            self._tableau.column(cle, anchor="center", width=160)
        defilement = ttk.Scrollbar(carte, orient="vertical", command=self._tableau.yview)
        self._tableau.config(yscrollcommand=defilement.set)
        self._tableau.pack(side="left", fill="both", expand=True)
        defilement.pack(side="left", fill="y")

        self._message = ttk.Label(self.corps, style=self.st("Gris.TLabel"))
        self._message.pack(anchor="w", pady=(10, 0))

    def quand_affiche(self) -> None:
        """Affiche l'historique gardé en mémoire, la prédiction la plus récente en haut."""
        self._tableau.delete(*self._tableau.get_children())
        lignes = self._app.historique
        for ligne in reversed(lignes):
            self._tableau.insert("", "end", values=[ligne.get(c, "") for c in self.COLONNES])
        self._message.config(text=f"{len(lignes)} prédiction(s)" if lignes else "Aucune prédiction pour l'instant.")

class EcranJoueur(Ecran):
    def __init__(self, app: "Application") -> None:
        super().__init__(app, "Prédire à partir d'un joueur réel")
        gauche = self.creer_carte(self.corps, "Choisir un joueur")
        gauche.pack(side="left", fill="y")
        self._resultat = CadreResultat(self.corps, self)
        self._resultat.pack(side="left", fill="both", expand=True, padx=(20, 0))

        ttk.Label(gauche, text="Équipe", style=self.st("CarteGris.TLabel")).pack(
            anchor="w")
        self._equipe = ttk.Combobox(gauche, state="readonly", width=32, style=self.st("TCombobox"), values=[TOUTES] + app.equipes())
        self._equipe.set(TOUTES)
        self._equipe.pack(anchor="w", pady=(2, 10))
        self._equipe.bind("<<ComboboxSelected>>", lambda _: self._filtrer())

        ttk.Label(gauche, text="Nom du joueur", style=self.st("CarteGris.TLabel")).pack(anchor="w")
        self._nom = tk.StringVar()
        self._nom.trace_add("write", lambda *_: self._filtrer())
        champ = ttk.Entry(gauche, textvariable=self._nom, width=34, style=self.st("TEntry"))
        champ.pack(anchor="w", pady=(2, 4))
        champ.bind("<Return>", lambda _: self._predire())
        champ.bind("<Down>", lambda _: self._aller_a_la_liste())

        cadre_liste = ttk.Frame(gauche, style=self.st("Grille.TFrame"))
        cadre_liste.pack(anchor="w", fill="x")
        self._suggestions = tk.Listbox(
            cadre_liste, height=10, activestyle="none", font=(POLICE, 10),
            relief="flat", borderwidth=0, highlightthickness=0,
            bg=self.COULEURS["carte"], fg=self.COULEURS["texte"],
            selectbackground=self.COULEURS["accent"], selectforeground="white")
        defilement = ttk.Scrollbar(cadre_liste, orient="vertical", command=self._suggestions.yview)
        self._suggestions.config(yscrollcommand=defilement.set)
        self._suggestions.pack(side="left", fill="x", expand=True)
        defilement.pack(side="left", fill="y")
        self._suggestions.bind("<<ListboxSelect>>", lambda _: self._choisir())
        self._suggestions.bind("<Double-Button-1>", lambda _: self._predire())
        self._suggestions.bind("<Return>", lambda _: self._predire())

        ttk.Button(gauche, text="Prédire", style=self.st("Accent.TButton"), cursor="hand2", command=self._predire).pack(pady=(14, 0))
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
        try:
            entree = self._app.chercher_joueur(self._nom.get())
        except DonneeInvalideError as erreur:
            messagebox.showerror("Joueur introuvable", str(erreur))
            return
        points = self._app.predire(entree)
        self.enregistrer_prediction(self._nom.get().strip(), points, entree)
        self._resultat.afficher(points, self._app.marge, f"{self._nom.get().strip()}\nd'après sa saison 2025-2026")

class EcranStatistiques(Ecran):
    FORMES = {**Ecran.FORMES, "relief_carte": "ridge","epaisseur_bordure": 3, "bouton": (32, 12)}

    def __init__(self, app: "Application", variables: list[Variable]) -> None:
        super().__init__(app, "Prédire à partir de statistiques")
        self._variables = variables
        self._textes: dict[str, tk.StringVar] = {}

        carte = self.creer_carte(self.corps, "Statistiques de la saison précédente")
        carte.pack(fill="x")
        grille = ttk.Frame(carte, style=self.st("Grille.TFrame"))
        grille.pack()
        par_colonne = math.ceil(len(variables) / 2)
        for i, variable in enumerate(variables):
            ligne, colonne = i % par_colonne, 2 * (i // par_colonne)
            ttk.Label(grille, text=variable.libelle, style=self.st("Carte.TLabel")).grid(
                row=ligne, column=colonne, sticky="e", padx=(20, 8), pady=4)
            texte = tk.StringVar()
            if isinstance(variable, VariableCategorielle):
                champ = ttk.Combobox(grille, textvariable=texte, width=13, values=variable.valeurs, state="readonly", style=self.st("TCombobox"))
            else:
                champ = ttk.Entry(grille, textvariable=texte, width=15, style=self.st("TEntry"))
            champ.grid(row=ligne, column=colonne + 1, sticky="w", pady=4)
            self._textes[variable.nom] = texte

        bas = ttk.Frame(self.corps, style=self.st("TFrame"))
        bas.pack(fill="both", expand=True, pady=(20, 0))
        ttk.Button(bas, text="Prédire", style=self.st("Accent.TButton"), cursor="hand2", command=self._predire).pack(side="left",anchor="n")
        self._resultat = CadreResultat(bas, self)
        self._resultat.pack(side="left", fill="both", expand=True, padx=(20, 0))

    def lire(self) -> dict[str, float | str]:
        entree = {v.nom: v.valider(self._textes[v.nom].get()) for v in self._variables}
        if entree["shots"] < entree["goals"]:
            messagebox.showerror("Saisie invalide", "Il y a moins de buts que de tirs au but.")
            return {}
        if entree["goals"] + entree["assists"] >= entree["evPoints"] + entree["ppPoints"]:
            messagebox.showerror("Saisie invalide", "Il y a trop de points à forces égales ou en avantage numérique par rapport au nombre de points.")
            return {}
        return entree

    def _predire(self) -> None:
        """Lit le formulaire et affiche la prédiction."""
        try:
            entree = self.lire()
        except DonneeInvalideError as erreur:
            messagebox.showerror("Saisie invalide", str(erreur))
            return
        
        pointsProchaine = self._app.predire(entree)
        self.enregistrer_prediction("Joueur fictif", pointsProchaine, entree)
        self._resultat.afficher(pointsProchaine, self._app.marge)

class EcranGraphique(Ecran):
    """Affiche l'histogramme d'une statistique, construit par DonneesLNH."""
    FORMES = {**Ecran.FORMES, "relief_carte": "flat", "epaisseur_bordure": 0}

    def __init__(self, app: "Application", variables: list[Variable]) -> None:
        """Crée la barre de choix et la zone où s'affichera le graphique."""
        super().__init__(app, "Concevoir des graphiques")
        self._par_libelle = {v.libelle: v.nom for v in variables if isinstance(v, VariableNumerique)}
        self._canevas = None

        barre = ttk.Frame(self.corps, style=self.st("TFrame"))
        barre.pack(fill="x", pady=(0, 14))
        ttk.Label(barre, text="Statistique à observer", style=self.st("TLabel")).pack(side="left")
        self._choix = ttk.Combobox(barre, state="readonly", width=30, values=list(self._par_libelle), style=self.st("TCombobox"))
        self._choix.pack(side="left", padx=10)
        self._choix.bind("<<ComboboxSelected>>", lambda _: self._tracer())

        self._carte = self.creer_carte(self.corps)
        self._carte.pack(fill="both", expand=True)
        self._accueil = ttk.Label(self._carte, style=self.st("CarteGris.TLabel"), justify="center", text="Choisissez une statistique pour voir\n""sa distribution chez tous les joueurs.")
        self._accueil.pack(expand=True)

    def _tracer(self) -> None:
        """Demande le graphique à DonneesLNH, ajoute le repère du joueur et l'affiche."""
        libelle = self._choix.get()
        if not libelle:
            messagebox.showerror("Aucun choix", "Choisissez une statistique.")
            return
        colonne = self._par_libelle[libelle]

        g = self._app.graphique_distribution(colonne, libelle)
        self._afficher(g)

    def _afficher(self, g: Graphique) -> None:
        """Remplace le graphique affiché par celui de g."""
        self._accueil.pack_forget()
        if self._canevas is not None:
            self._canevas.get_tk_widget().destroy()
        self._canevas = FigureCanvasTkAgg(g.figure, master=self._carte)
        self._canevas.draw()
        self._canevas.get_tk_widget().pack(fill="both", expand=True)






## ------------------------------Application----------------------------------------##



class Application(tk.Tk):
    def __init__(self, modele, variables: list[Variable], metadonnees: dict, donnees: DonneesLNH) -> None:
        """Construit les quatre écrans à partir du modèle et des données."""
        super().__init__()
        self.historique = self._charger_historique()
        self.title(TITRE)
        self.geometry("900x680")
        self.minsize(820, 600)
        appliquer_style(self)

        self.protocol("WM_DELETE_WINDOW", self._fermer)

        self._modele = modele
        self._variables = variables
        self._donnees = donnees
        self._marge = metadonnees["metriques"]["modele"]
        self.derniere_entree: dict = {}

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
        self._ecrans[nom].tkraise()
        self._ecrans[nom].quand_affiche()

    def chercher_joueur(self, nom: str) -> tuple[dict, int]:
        colonnes = [v.nom for v in self._variables]
        return self._donnees.stats_joueur(nom, colonnes)

    def equipes(self) -> list[str]:
        """Renvoie les abréviations des équipes, en ordre alphabétique."""
        return self._donnees.equipes()

    def noms_joueurs(self, texte: str, equipe: str) -> list[str]:
        """Renvoie les joueurs dont le nom contient texte."""
        return self._donnees.noms_joueurs(texte, equipe)

    def predire(self, entree: dict) -> int:
        """Appelle le modèle et renvoie les points prévus."""
        self.derniere_entree = entree
        return int(self._modele.predire(entree))
    
    def graphique_distribution(self, colonne: str, libelle: str) -> Graphique:
        """Renvoie l'histogramme de la colonne, construit par DonneesLNH."""
        return self._donnees.graphique_distribution(colonne, libelle)
    
    def _charger_historique(self) -> list[dict]:
        """Lit le CSV d'historique une seule fois. Renvoie [] s'il n'existe pas."""
        if not os.path.exists(CHEMIN_HISTORIQUE):
            return []
        with open(CHEMIN_HISTORIQUE, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def _fermer(self) -> None:
        if self.historique:
            os.makedirs(os.path.dirname(CHEMIN_HISTORIQUE), exist_ok=True)
            try:
                with open(CHEMIN_HISTORIQUE, "w", encoding="utf-8", newline="") as f:
                    ecrivain = csv.DictWriter(f, fieldnames=list(self.historique[0]))
                    ecrivain.writeheader()
                    ecrivain.writerows(self.historique)
            except PermissionError:
                messagebox.showwarning("Historique", "Impossible d'enregistrer l'historique.")
        self.quit()
        self.destroy()