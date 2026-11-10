import tkinter as tk 
from PIL import Image, ImageTk
 
#widget.config()


# Création de la fenêtre principale
fenetre = tk.Tk()

# Dimensions de l'écran'
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()
x = (largeur_ecran - 1100) // 2
y = (hauteur_ecran - hauteur_ecran) // 2

# Appliquer les dimensions et la position
fenetre.geometry(f"{1100}x{hauteur_ecran}+{x}+{y}")

#création de la premiere interface 

# FONCTIONS
def afficher_accueil():
    """Affiche la page d'accueil."""

    frame_reel.pack_forget()
    frame_fictif.pack_forget()
    frame_graphique.pack_forget()

    frame_accueil.pack(fill="both", expand=True)


def afficher_reel():
    """Affiche la page du joueur réel."""

    frame_accueil.pack_forget()
    frame_reel.pack(fill="both", expand=True)


def afficher_fictif():
    """Affiche la page du joueur fictif."""

    frame_accueil.pack_forget()
    frame_fictif.pack(fill="both", expand=True)


def afficher_graphique():
    """Affiche la page des graphiques."""

    frame_accueil.pack_forget()
    frame_graphique.pack(fill="both", expand=True)


# fond
# Charger l'image

# PAGE D'ACCUEIL
frame_accueil = tk.Frame(
    fenetre,
    bg="#101820"
)

# Charger l'image de fond
image = Image.open("Ressources/background_habs.jpg")

# Récupérer les dimensions de l'écran
largeur = fenetre.winfo_screenwidth()
hauteur = fenetre.winfo_screenheight()

# Adapter l'image à l'écran
image = image.resize((largeur, hauteur))

# Convertir l'image pour Tkinter
photo = ImageTk.PhotoImage(image, master=fenetre)

# Afficher l'image dans la page d'accueil
fond = tk.Label(
    frame_accueil,
    image=photo
)

fond.place(
    x=0,
    y=0,
)

titre = tk.Label(
    frame_accueil,
    text="Prédiction des points de la NHL",
    font=("Arial", 32, "bold"),
    fg="white",
    bg="#101820"
)

titre.pack(pady=30)


question = tk.Label(
    frame_accueil,
    text="Que souhaitez-vous faire ?",
    font=("Arial", 18),
    fg="white",
    bg="#101820"
)

question.pack(pady=30)


# Bouton joueur réel
bouton_reel = tk.Button(
    frame_accueil,
    text="JOUEUR RÉEL",
    font=("Arial", 16, "bold"),
    width=25,
    height=3,
    command=afficher_reel
)

bouton_reel.pack(pady=15)


# Bouton joueur fictif
bouton_fictif = tk.Button(
    frame_accueil,
    text="JOUEUR FICTIF",
    font=("Arial", 16, "bold"),
    width=25,
    height=3,
    command=afficher_fictif
)

bouton_fictif.pack(pady=15)


# Bouton graphique
bouton_graphique = tk.Button(
    frame_accueil,
    text="CRÉER UN GRAPHIQUE",
    font=("Arial", 16, "bold"),
    width=25,
    height=3,
    command=afficher_graphique
)

bouton_graphique.pack(pady=15)


# PAGE JOUEUR RÉEL

frame_reel = tk.Frame(
    fenetre,
    bg="#101820"
)

titre_reel = tk.Label(
    frame_reel,
    text="PRÉDICTION D'UN JOUEUR RÉEL",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#101820"
)

titre_reel.pack(pady=40)


bouton_retour_reel = tk.Button(
    frame_reel,
    text="Retour",
    font=("Arial", 14),
    command=afficher_accueil
)
bouton_retour_reel.place(x=20, y=20)


# PAGE JOUEUR FICTIF
frame_fictif = tk.Frame(
    fenetre,
    bg="#101820"
)

titre_fictif = tk.Label(
    frame_fictif,
    text="PRÉDICTION - JOUEUR FICTIF",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#101820"
)

titre_fictif.pack(pady=40)


bouton_retour_fictif = tk.Button(
    frame_fictif,
    text="Retour",
    font=("Arial", 14),
    command=afficher_accueil
)

bouton_retour_fictif.place(x=20, y=20)
# PAGE GRAPHIQUE

frame_graphique = tk.Frame(
    fenetre,
    bg="#101820"
)

titre_graphique = tk.Label(
    frame_graphique,
    text="CRÉATION DE GRAPHIQUES",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#101820"
)

titre_graphique.pack(pady=40)


bouton_retour_graphique = tk.Button(
    frame_graphique,
    text="Retour",
    font=("Arial", 14),
    command=afficher_accueil
)

bouton_retour_graphique.place(x=20, y=20)

# LANCEMENT
frame_accueil.pack(fill="both", expand=True)

fenetre.mainloop()