"""
Début

    Définir le fichier top.json

    Fonction charger_top
        Si top.json existe
            Lire son contenu
            Retourner les classements
        Sinon
            Retourner un dictionnaire vide
        Fin Si
    Fin Fonction

    Fonction sauvegarder_top(classements)
        Enregistrer les classements dans top.json
    Fin Fonction

    Fonction formater_temps(temps)
        Convertir les secondes en minutes et secondes
        Retourner le temps formaté
    Fin Fonction

    Fonction trier_classement(classement)
        Trier les scores :
            d'abord selon le nombre d'essais croissant
            puis selon le temps croissant
    Fin Fonction

    Créer la fenêtre graphique

    Afficher :
        les champs minimum et maximum
        le bouton "Lancer une partie"
        le champ de proposition
        le bouton "Deviner"
        le bouton "Abandonner"
        le bouton "Afficher les tops"
        le bouton "Effacer les tops"
        le bouton "Quitter"
        les labels des essais et du chronomètre

    Fonction lancer_partie
        Lire les valeurs minimum et maximum

        Si les valeurs ne sont pas des entiers
            Afficher une erreur
        Sinon si minimum >= maximum
            Afficher une erreur
        Sinon
            Générer un nombre secret entre minimum et maximum
            Initialiser le nombre d'essais à 0
            Démarrer le chronomètre

            Désactiver les champs de l'intervalle
            Activer le champ de proposition
            Activer les boutons "Deviner" et "Abandonner"
            Mettre le curseur dans le champ de proposition
        Fin Si
    Fin Fonction

    Fonction actualiser_chronometre
        Tant qu'une partie est en cours
            Calculer le temps écoulé
            Afficher le temps
            Actualiser régulièrement l'affichage
        Fin Tant que
    Fin Fonction

    Fonction verifier_proposition
        Lire la proposition du joueur

        Si la proposition n'est pas un entier
            Afficher une erreur
        Sinon si la proposition est hors de l'intervalle
            Afficher une erreur
        Sinon
            Ajouter 1 au nombre d'essais

            Si la proposition est inférieure au nombre secret
                Afficher "C'est plus grand !"
            Sinon si la proposition est supérieure au nombre secret
                Afficher "C'est plus petit !"
            Sinon
                Arrêter le chronomètre
                Afficher le message "Bingo !"
                Demander le nom du joueur

                Charger les classements
                Identifier l'intervalle utilisé
                Ajouter le score au classement correspondant
                Trier le classement
                Garder les 10 meilleurs scores
                Sauvegarder les classements

                Afficher le classement
                Réinitialiser l'interface
            Fin Si
        Fin Si
    Fin Fonction

    Fonction abandonner_partie
        Arrêter le chronomètre
        Indiquer que la partie est abandonnée
        Réactiver les champs de l'intervalle
        Désactiver les boutons de jeu
    Fin Fonction

    Fonction afficher_top_intervalle
        Charger les classements
        Récupérer le classement de l'intervalle choisi
        Trier les scores
        Afficher les 10 meilleurs scores
    Fin Fonction

    Fonction afficher_tous_les_tops
        Charger les classements

        Pour chaque intervalle
            Trier le classement
            Afficher les 10 meilleurs scores
        Fin Pour
    Fin Fonction

    Fonction effacer_tops
        Demander une confirmation

        Si la confirmation est acceptée
            Supprimer top.json
            Afficher un message de confirmation
        Fin Si
    Fin Fonction

    Fonction quitter
        Fermer la fenêtre graphique
    Fin Fonction

    Attendre les actions de l'utilisateur :
        clic sur un bouton
        appui sur Entrée
        saisie d'une proposition
        fermeture de la fenêtre

Fin
"""

import json
import random
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, simpledialog


FICHIER_TOP = Path(__file__).parent / "top.json"
FICHIER_CONFIG = Path(__file__).parent / "arcade_config.json"
MOT_DE_PASSE_DEFAUT = "Ghost"
COULEUR_MENU_DEFAUT = "#111827"


def charger_configuration():
    if not FICHIER_CONFIG.exists():
        return {}
    try:
        with open(FICHIER_CONFIG, "r", encoding="utf-8") as fichier:
            configuration = json.load(fichier)
            return configuration if isinstance(configuration, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_configuration(configuration):
    with open(FICHIER_CONFIG, "w", encoding="utf-8") as fichier:
        json.dump(configuration, fichier, indent=4, ensure_ascii=False)


def charger_mot_de_passe():
    return charger_configuration().get(
        "mot_de_passe",
        MOT_DE_PASSE_DEFAUT
    )


def sauvegarder_mot_de_passe(mot_de_passe):
    configuration = charger_configuration()
    configuration["mot_de_passe"] = mot_de_passe
    sauvegarder_configuration(configuration)


def charger_tops():
    if not FICHIER_TOP.exists():
        return {}
    try:
        with open(FICHIER_TOP, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)
            return donnees if isinstance(donnees, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_tops(tops):
    with open(FICHIER_TOP, "w", encoding="utf-8") as fichier:
        json.dump(tops, fichier, indent=4, ensure_ascii=False)


def ajouter_top(jeu, joueur, score, temps=None):
    tops = charger_tops()
    resultat = {"joueur": joueur, "score": score}

    if temps is not None:
        resultat["temps"] = temps

    tops.setdefault(jeu, []).append(resultat)

    if jeu.startswith("Bingo"):
        tops[jeu].sort(
            key=lambda resultat: (
                resultat.get("score", 999999),
                resultat.get("temps", 999999)
            )
        )
    elif jeu == "Aventure plateforme":
        tops[jeu].sort(
            key=lambda resultat: (
                resultat.get("temps", 999999),
                -resultat.get("score", 0)
            )
        )
    else:
        tops[jeu].sort(
            key=lambda resultat: resultat.get("score", 0),
            reverse=True
        )

    tops[jeu] = tops[jeu][:10]
    sauvegarder_tops(tops)


def formater_temps(secondes):
    return f"{int(secondes // 60)} min {secondes % 60:.2f} s"


class JeuxApp:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("🎮 Arcade de jeux")
        self.fenetre.geometry("820x920")
        self.fenetre.resizable(False, False)
        self.fenetre.configure(bg="#111827")

        self.configurer_style()
        self.creer_menu()
        self.creer_bingo()
        self.creer_pfc()
        self.creer_morpion()
        self.creer_puissance4()
        self.creer_bataille()
        self.creer_quiz()
        self.creer_pendu()
        self.creer_2048()
        self.creer_echecs()
        self.creer_snake()
        self.creer_tetris()
        self.creer_plateforme()

        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitter)
        self.fenetre.bind("<Key>", self.touche_2048)
        self.fenetre.bind("<KeyRelease>", self.touche_plateforme_relache)
        self.afficher_menu()

    def configurer_style(self):
        style = ttk.Style(self.fenetre)
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background="#111827"
        )

        style.configure(
            "Menu.TFrame",
            background=COULEUR_MENU_DEFAUT
        )

        style.configure(
            "MenuTitre.TLabel",
            background=COULEUR_MENU_DEFAUT,
            foreground="#f8fafc",
            font=("DejaVu Sans", 28, "bold")
        )

        style.configure(
            "MenuSousTitre.TLabel",
            background=COULEUR_MENU_DEFAUT,
            foreground="#cbd5e1",
            font=("DejaVu Sans", 13)
        )

        style.configure(
            "Titre.TLabel",
            background="#111827",
            foreground="#f8fafc",
            font=("DejaVu Sans", 28, "bold")
        )

        style.configure(
            "SousTitre.TLabel",
            background="#111827",
            foreground="#94a3b8",
            font=("DejaVu Sans", 13)
        )

        style.configure(
            "Carte.TFrame",
            background="#ffffff"
        )

        style.configure(
            "CarteTitre.TLabel",
            background="#ffffff",
            foreground="#1e293b",
            font=("DejaVu Sans", 16, "bold")
        )

        style.configure(
            "Info.TLabel",
            background="#ffffff",
            foreground="#475569",
            font=("DejaVu Sans", 11)
        )

        style.configure(
            "Stats.TLabel",
            background="#ffffff",
            foreground="#4f46e5",
            font=("DejaVu Sans", 13, "bold")
        )

        style.configure(
            "Principal.TButton",
            background="#6366f1",
            foreground="#ffffff",
            font=("DejaVu Sans", 11, "bold"),
            padding=(18, 10),
            borderwidth=0
        )

        style.map(
            "Principal.TButton",
            background=[
                ("active", "#818cf8"),
                ("pressed", "#4338ca")
            ]
        )

        style.configure(
            "Secondaire.TButton",
            background="#dbeafe",
            foreground="#1e40af",
            font=("DejaVu Sans", 11, "bold"),
            padding=(15, 9),
            borderwidth=0
        )

        style.configure(
            "Danger.TButton",
            background="#fee2e2",
            foreground="#b91c1c",
            font=("DejaVu Sans", 11, "bold"),
            padding=(15, 9),
            borderwidth=0
        )

        style.configure(
            "TEntry",
            padding=8,
            fieldbackground="#f8fafc",
            foreground="#1e293b"
        )

        style.configure(
            "TRadiobutton",
            background="#ffffff",
            foreground="#334155",
            font=("DejaVu Sans", 11)
        )

    def bouton_menu(self, parent):
        ttk.Button(
            parent,
            text="🏠 Menu principal",
            command=self.afficher_menu,
            style="Secondaire.TButton"
        ).pack(side="bottom", pady=10)

    def masquer_frames(self):
        for frame in (
            self.frame_menu,
            self.frame_bingo,
            self.frame_pfc,
            self.frame_morpion,
            self.frame_puissance4,
            self.frame_bataille,
            self.frame_quiz,
            self.frame_pendu,
            self.frame_2048,
            self.frame_echecs_choix,
            self.frame_echecs,
            self.frame_snake,
            self.frame_tetris_choix,
            self.frame_tetris,
            self.frame_plateforme_choix,
            self.frame_plateforme
        ):
            frame.pack_forget()

    def afficher_menu(self):
        self.arreter_bingo()
        self.pfc_en_cours = False
        self.morpion_en_cours = False
        self.puissance4_en_cours = False
        self.bataille_en_cours = False
        self.quiz_en_cours = False
        self.pendu_en_cours = False
        self.jeu2048_en_cours = False
        self.echecs_en_cours = False
        self.snake_en_cours = False
        if self.snake_timer is not None:
            self.fenetre.after_cancel(self.snake_timer)
            self.snake_timer = None
        self.tetris_en_cours = False
        if self.tetris_timer is not None:
            self.fenetre.after_cancel(self.tetris_timer)
            self.tetris_timer = None
        self.plateforme_en_cours = False
        if self.plateforme_timer is not None:
            self.fenetre.after_cancel(self.plateforme_timer)
            self.plateforme_timer = None

        self.masquer_frames()
        self.frame_menu.pack(fill="both", expand=True)

    # =====================================================
    # MENU
    # =====================================================

    def creer_menu(self):
        self.frame_menu = ttk.Frame(
            self.fenetre,
            style="Menu.TFrame"
        )

        ttk.Label(
            self.frame_menu,
            text="🎮 Mes jeux",
            style="MenuTitre.TLabel"
        ).pack(pady=(30, 5))

        ttk.Label(
            self.frame_menu,
            text="Choisis un jeu",
            style="MenuSousTitre.TLabel"
        ).pack(pady=(0, 15))

        self.jeux_menu = (
            ("bingo", "🎯 Bingo", self.afficher_bingo),
            ("pfc", "✊ Pierre-Feuille-Ciseau-Lézard-Spock", self.afficher_pfc),
            ("morpion", "⭕ Morpion", self.afficher_morpion),
            ("puissance4", "🔴 Puissance 4", self.afficher_puissance4),
            ("bataille", "⚓ Bataille navale", self.afficher_bataille),
            ("quiz", "🧠 Quiz", self.afficher_quiz),
            ("pendu", "🔤 Pendu", self.afficher_pendu),
            ("2048", "🔢 2048", self.afficher_2048),
            ("echecs", "♟ Échecs", self.afficher_echecs),
            ("snake", "🐍 Snake", self.afficher_snake),
            ("tetris", "🧱 Tetris", self.afficher_tetris),
            ("plateforme", "🌟 Aventure plateforme", self.afficher_plateforme)
        )
        self.jeux_menu_frame = ttk.Frame(
            self.frame_menu,
            style="Menu.TFrame"
        )
        self.jeux_menu_frame.pack()
        self.construire_menu_jeux()

        ttk.Button(
            self.frame_menu,
            text="🏆 Afficher un top",
            command=self.afficher_tops,
            style="Secondaire.TButton"
        ).pack(pady=6)

        ttk.Button(
            self.frame_menu,
            text="🏆 Gérer les classements",
            command=self.effacer_tops,
            style="Secondaire.TButton"
        ).pack(pady=3)

        ttk.Button(
            self.frame_menu,
            text="⚙ Paramètres",
            command=self.ouvrir_parametres,
            style="Secondaire.TButton"
        ).pack(pady=3)

        ttk.Button(
            self.frame_menu,
            text="✕ Quitter",
            command=self.quitter,
            style="Danger.TButton"
        ).pack(pady=12)

        configuration = charger_configuration()
        self.appliquer_couleur_menu(
            configuration.get("couleur_menu", COULEUR_MENU_DEFAUT)
        )

    def construire_menu_jeux(self):
        for bouton in self.jeux_menu_frame.winfo_children():
            bouton.destroy()

        definitions = {identifiant: (texte, commande) for identifiant, texte, commande in self.jeux_menu}
        ordre = charger_configuration().get("ordre_jeux", [])
        ordre = [identifiant for identifiant in ordre if identifiant in definitions]
        ordre.extend(
            identifiant for identifiant, _, _ in self.jeux_menu
            if identifiant not in ordre
        )

        for identifiant in ordre:
            texte, commande = definitions[identifiant]
            ttk.Button(
                self.jeux_menu_frame,
                text=texte,
                command=commande,
                style="Principal.TButton",
                width=42
            ).pack(pady=5, padx=30)

    def appliquer_couleur_menu(self, couleur):
        style = ttk.Style(self.fenetre)
        style.configure("Menu.TFrame", background=couleur)
        style.configure("MenuTitre.TLabel", background=couleur)
        style.configure("MenuSousTitre.TLabel", background=couleur)

    # =====================================================
    # BINGO
    # =====================================================

    def creer_bingo(self):
        self.frame_bingo = ttk.Frame(self.fenetre)

        ttk.Label(
            self.frame_bingo,
            text="🎯 BINGO",
            style="Titre.TLabel"
        ).pack(pady=15)

        config = ttk.Frame(
            self.frame_bingo,
            style="Carte.TFrame",
            padding=15
        )
        config.pack(padx=35, fill="x")

        ttk.Label(config, text="Minimum").grid(row=0, column=0)
        self.bingo_minimum = ttk.Entry(config, width=10)
        self.bingo_minimum.grid(row=0, column=1, padx=5)

        ttk.Label(config, text="Maximum").grid(row=0, column=2)
        self.bingo_maximum = ttk.Entry(config, width=10)
        self.bingo_maximum.grid(row=0, column=3, padx=5)

        ttk.Button(
            config,
            text="▶ Lancer",
            command=self.lancer_bingo,
            style="Principal.TButton"
        ).grid(row=1, column=0, columnspan=4, pady=10)

        jeu = ttk.Frame(
            self.frame_bingo,
            style="Carte.TFrame",
            padding=15
        )
        jeu.pack(padx=35, pady=10, fill="x")

        self.bingo_info = ttk.Label(
            jeu,
            text="Choisis un intervalle.",
            style="CarteTitre.TLabel"
        )
        self.bingo_info.pack()

        self.bingo_essais_label = ttk.Label(
            jeu,
            text="Essais : 0",
            style="Stats.TLabel"
        )
        self.bingo_essais_label.pack()

        self.bingo_temps_label = ttk.Label(
            jeu,
            text="Temps : 0 min 0.00 s",
            style="Stats.TLabel"
        )
        self.bingo_temps_label.pack()

        self.bingo_proposition = ttk.Entry(jeu, width=15)
        self.bingo_proposition.pack(pady=8)
        self.bingo_proposition.bind(
            "<Return>",
            lambda event: self.verifier_bingo()
        )

        boutons = ttk.Frame(jeu)
        boutons.pack()

        self.bingo_deviner = ttk.Button(
            boutons,
            text="Deviner",
            command=self.verifier_bingo,
            state="disabled",
            style="Principal.TButton"
        )
        self.bingo_deviner.pack(side="left", padx=5)

        self.bingo_abandonner = ttk.Button(
            boutons,
            text="Abandonner",
            command=self.abandonner_bingo,
            state="disabled",
            style="Danger.TButton"
        )
        self.bingo_abandonner.pack(side="left", padx=5)

        self.bouton_menu(self.frame_bingo)
        self.bingo_en_cours = False
        self.bingo_timer = None

    def afficher_bingo(self):
        self.masquer_frames()
        self.frame_bingo.pack(fill="both", expand=True)

    def lancer_bingo(self):
        try:
            minimum = int(self.bingo_minimum.get())
            maximum = int(self.bingo_maximum.get())
        except ValueError:
            messagebox.showerror("Erreur", "Entre deux entiers.")
            return

        if minimum >= maximum:
            messagebox.showerror(
                "Erreur",
                "Le minimum doit être inférieur au maximum."
            )
            return

        self.bingo_min = minimum
        self.bingo_max = maximum
        self.bingo_secret = random.randint(minimum, maximum)
        self.bingo_essais = 0
        self.bingo_debut = time.perf_counter()
        self.bingo_en_cours = True

        self.bingo_minimum.config(state="disabled")
        self.bingo_maximum.config(state="disabled")
        self.bingo_deviner.config(state="normal")
        self.bingo_abandonner.config(state="normal")
        self.bingo_info.config(
            text=f"Devine entre {minimum} et {maximum}."
        )
        self.actualiser_bingo()
        self.bingo_proposition.focus()

    def actualiser_bingo(self):
        if self.bingo_en_cours:
            temps = time.perf_counter() - self.bingo_debut
            self.bingo_temps_label.config(
                text=f"Temps : {formater_temps(temps)}"
            )
            self.bingo_timer = self.fenetre.after(
                100,
                self.actualiser_bingo
            )

    def verifier_bingo(self):
        if not self.bingo_en_cours:
            return

        try:
            proposition = int(self.bingo_proposition.get())
        except ValueError:
            messagebox.showerror("Erreur", "Entre un entier.")
            return

        if not self.bingo_min <= proposition <= self.bingo_max:
            messagebox.showwarning(
                "Erreur",
                "Nombre hors de l'intervalle."
            )
            return

        self.bingo_essais += 1
        self.bingo_essais_label.config(
            text=f"Essais : {self.bingo_essais}"
        )
        self.bingo_proposition.delete(0, tk.END)

        if proposition < self.bingo_secret:
            self.bingo_info.config(text="C'est plus grand !")
        elif proposition > self.bingo_secret:
            self.bingo_info.config(text="C'est plus petit !")
        else:
            self.gagner_bingo()

    def gagner_bingo(self):
        self.arreter_bingo()
        temps = time.perf_counter() - self.bingo_debut
        joueur = simpledialog.askstring(
            "Classement",
            "Ton nom :",
            parent=self.fenetre
        ) or "Anonyme"

        ajouter_top(
            f"Bingo {self.bingo_min}-{self.bingo_max}",
            joueur,
            self.bingo_essais,
            temps
        )

        messagebox.showinfo(
            "Bingo",
            f"Bravo !\nEssais : {self.bingo_essais}\n"
            f"Temps : {formater_temps(temps)}"
        )
        self.reinitialiser_bingo()

    def arreter_bingo(self):
        self.bingo_en_cours = False

        if self.bingo_timer is not None:
            self.fenetre.after_cancel(self.bingo_timer)
            self.bingo_timer = None

    def abandonner_bingo(self):
        self.arreter_bingo()
        self.bingo_info.config(text="Partie abandonnée.")
        self.reinitialiser_bingo()

    def reinitialiser_bingo(self):
        self.bingo_minimum.config(state="normal")
        self.bingo_maximum.config(state="normal")
        self.bingo_deviner.config(state="disabled")
        self.bingo_abandonner.config(state="disabled")

    # =====================================================
    # PIERRE-FEUILLE-CISEAU-LÉZARD-SPOCK
    # =====================================================

    def creer_pfc(self):
        self.frame_pfc = ttk.Frame(self.fenetre)
        self.pfc_en_cours = False
        self.pfc_mode = tk.StringVar(value="ordinateur")
        self.pfc_choix = {
            1: "Pierre",
            2: "Feuille",
            3: "Ciseau",
            4: "Lézard",
            5: "Spock"
        }
        self.pfc_victoires = {
            (1, 3), (1, 4),
            (2, 1), (2, 5),
            (3, 2), (3, 4),
            (4, 2), (4, 5),
            (5, 1), (5, 3)
        }

        ttk.Label(
            self.frame_pfc,
            text="✊ PIERRE-FEUILLE-CISEAU-LÉZARD-SPOCK",
            style="Titre.TLabel"
        ).pack(pady=15)

        config = ttk.Frame(
            self.frame_pfc,
            style="Carte.TFrame",
            padding=10
        )
        config.pack(padx=30, fill="x")

        ttk.Radiobutton(
            config,
            text="Contre l'ordinateur",
            variable=self.pfc_mode,
            value="ordinateur"
        ).pack()

        ttk.Radiobutton(
            config,
            text="Deux joueurs",
            variable=self.pfc_mode,
            value="joueur"
        ).pack()

        self.pfc_nom1 = ttk.Entry(config, width=22)
        self.pfc_nom1.insert(0, "Joueur 1")
        self.pfc_nom1.pack(pady=3)

        self.pfc_nom2 = ttk.Entry(config, width=22)
        self.pfc_nom2.insert(0, "Joueur 2")
        self.pfc_nom2.pack(pady=3)

        ttk.Button(
            config,
            text="▶ Commencer",
            command=self.lancer_pfc,
            style="Principal.TButton"
        ).pack()

        jeu = ttk.Frame(
            self.frame_pfc,
            style="Carte.TFrame",
            padding=10
        )
        jeu.pack(padx=30, pady=10, fill="x")

        self.pfc_info = ttk.Label(
            jeu,
            text="Commence une partie.",
            style="CarteTitre.TLabel"
        )
        self.pfc_info.pack()

        self.pfc_score = ttk.Label(
            jeu,
            text="Score : 0 - 0",
            style="Stats.TLabel"
        )
        self.pfc_score.pack(pady=5)

        for numero, nom in self.pfc_choix.items():
            ttk.Button(
                jeu,
                text=f"{numero} - {nom}",
                command=lambda valeur=numero:
                self.jouer_pfc(valeur),
                style="Secondaire.TButton"
            ).pack(side="left", padx=2)

        self.bouton_menu(self.frame_pfc)

    def afficher_pfc(self):
        self.masquer_frames()
        self.frame_pfc.pack(fill="both", expand=True)

    def lancer_pfc(self):
        self.pfc_joueur1 = self.pfc_nom1.get() or "Joueur 1"
        self.pfc_joueur2 = (
            "Ordinateur"
            if self.pfc_mode.get() == "ordinateur"
            else self.pfc_nom2.get() or "Joueur 2"
        )
        self.pfc_score1 = 0
        self.pfc_score2 = 0
        self.pfc_tour = 0
        self.pfc_choix_j1 = None
        self.pfc_en_cours = True
        self.pfc_score.config(text="Score : 0 - 0")
        self.pfc_info.config(text="Choisis un symbole.")

    def jouer_pfc(self, choix):
        if not self.pfc_en_cours:
            return

        if self.pfc_mode.get() == "joueur":
            if self.pfc_choix_j1 is None:
                self.pfc_choix_j1 = choix
                self.pfc_info.config(
                    text=f"{self.pfc_joueur2}, choisis."
                )
                return

            choix1 = self.pfc_choix_j1
            choix2 = choix
            self.pfc_choix_j1 = None
        else:
            choix1 = choix
            choix2 = random.randint(1, 5)

        self.pfc_tour += 1

        if choix1 == choix2:
            resultat = "Égalité !"
        elif (choix1, choix2) in self.pfc_victoires:
            self.pfc_score1 += 1
            resultat = f"{self.pfc_joueur1} gagne."
        else:
            self.pfc_score2 += 1
            resultat = f"{self.pfc_joueur2} gagne."

        self.pfc_score.config(
            text=f"Score : {self.pfc_score1} - {self.pfc_score2}"
        )
        self.pfc_info.config(
            text=(
                f"{self.pfc_choix[choix1]} contre "
                f"{self.pfc_choix[choix2]}\n{resultat}"
            )
        )

        if self.pfc_tour == 5:
            self.pfc_en_cours = False

            if self.pfc_score1 > self.pfc_score2:
                gagnant, score = self.pfc_joueur1, self.pfc_score1
            elif self.pfc_score2 > self.pfc_score1:
                gagnant, score = self.pfc_joueur2, self.pfc_score2
            else:
                gagnant, score = "Égalité", 0

            if gagnant != "Égalité":
                ajouter_top(
                    "Pierre-Feuille-Ciseau-Lézard-Spock",
                    gagnant,
                    score
                )

            messagebox.showinfo("Fin de partie", f"{gagnant} gagne !")

    # =====================================================
    # MORPION
    # =====================================================

    def creer_morpion(self):
        self.frame_morpion = ttk.Frame(self.fenetre)
        self.morpion_en_cours = False
        self.morpion_mode = tk.StringVar(value="ordinateur")
        self.morpion_cases = []

        ttk.Label(
            self.frame_morpion,
            text="⭕ MORPION",
            style="Titre.TLabel"
        ).pack(pady=15)

        config = ttk.Frame(
            self.frame_morpion,
            style="Carte.TFrame",
            padding=10
        )
        config.pack(padx=30, fill="x")

        ttk.Radiobutton(
            config,
            text="Contre l'ordinateur",
            variable=self.morpion_mode,
            value="ordinateur"
        ).pack()

        ttk.Radiobutton(
            config,
            text="Deux joueurs",
            variable=self.morpion_mode,
            value="joueur"
        ).pack()

        self.morpion_nom1 = ttk.Entry(config, width=22)
        self.morpion_nom1.insert(0, "Joueur 1")
        self.morpion_nom1.pack(pady=3)

        self.morpion_nom2 = ttk.Entry(config, width=22)
        self.morpion_nom2.insert(0, "Joueur 2")
        self.morpion_nom2.pack(pady=3)

        ttk.Button(
            config,
            text="▶ Commencer",
            command=self.lancer_morpion,
            style="Principal.TButton"
        ).pack()

        self.morpion_info = ttk.Label(
            self.frame_morpion,
            text="Commence une partie.",
            style="CarteTitre.TLabel"
        )
        self.morpion_info.pack(pady=8)

        grille = ttk.Frame(self.frame_morpion)
        grille.pack()

        for position in range(9):
            bouton = tk.Button(
                grille,
                text="",
                width=4,
                height=2,
                font=("Arial", 22, "bold"),
                command=lambda p=position:
                self.jouer_morpion(p)
            )
            bouton.grid(
                row=position // 3,
                column=position % 3,
                padx=3,
                pady=3
            )
            self.morpion_cases.append(bouton)

        self.bouton_menu(self.frame_morpion)

    def afficher_morpion(self):
        self.masquer_frames()
        self.frame_morpion.pack(fill="both", expand=True)

    def lancer_morpion(self):
        self.morpion_j1 = self.morpion_nom1.get() or "Joueur 1"
        self.morpion_j2 = (
            "Ordinateur"
            if self.morpion_mode.get() == "ordinateur"
            else self.morpion_nom2.get() or "Joueur 2"
        )
        self.morpion_plateau = [""] * 9
        self.morpion_joueur = "X"
        self.morpion_en_cours = True

        for bouton in self.morpion_cases:
            bouton.config(text="", state="normal")

        self.morpion_info.config(
            text=f"{self.morpion_j1} joue avec X."
        )

    def jouer_morpion(self, position):
        if (
            not self.morpion_en_cours
            or self.morpion_plateau[position]
        ):
            return

        joueur = self.morpion_joueur
        self.morpion_plateau[position] = joueur
        self.morpion_cases[position].config(text=joueur)

        if self.victoire_morpion(joueur):
            nom = self.morpion_j1 if joueur == "X" else self.morpion_j2
            self.fin_morpion(f"{nom} gagne !", nom)
            return

        if "" not in self.morpion_plateau:
            self.fin_morpion("Match nul !", None)
            return

        if (
            self.morpion_mode.get() == "ordinateur"
            and joueur == "X"
        ):
            self.morpion_joueur = "O"
            self.fenetre.after(
                350,
                self.tour_ordinateur_morpion
            )
        else:
            self.morpion_joueur = "O" if joueur == "X" else "X"

    def tour_ordinateur_morpion(self):
        if not self.morpion_en_cours:
            return

        libres = [
            index for index, valeur in enumerate(self.morpion_plateau)
            if not valeur
        ]

        if not libres:
            return

        position = random.choice(libres)
        self.morpion_plateau[position] = "O"
        self.morpion_cases[position].config(text="O")

        if self.victoire_morpion("O"):
            self.fin_morpion("L'ordinateur gagne !", "Ordinateur")
        elif "" not in self.morpion_plateau:
            self.fin_morpion("Match nul !", None)
        else:
            self.morpion_joueur = "X"
            self.morpion_info.config(
                text=f"{self.morpion_j1}, à toi."
            )

    def victoire_morpion(self, symbole):
        combinaisons = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )

        return any(
            all(
                self.morpion_plateau[index] == symbole
                for index in ligne
            )
            for ligne in combinaisons
        )

    def fin_morpion(self, message, gagnant):
        self.morpion_en_cours = False

        for bouton in self.morpion_cases:
            bouton.config(state="disabled")

        if gagnant:
            ajouter_top("Morpion", gagnant, 1)

        messagebox.showinfo("Morpion", message)

    # =====================================================
    # PUISSANCE 4
    # =====================================================

    def creer_puissance4(self):
        self.frame_puissance4 = ttk.Frame(self.fenetre)
        self.puissance4_en_cours = False
        self.puissance4_mode = tk.StringVar(value="ordinateur")

        ttk.Label(
            self.frame_puissance4,
            text="🔴 PUISSANCE 4",
            style="Titre.TLabel"
        ).pack(pady=10)

        config = ttk.Frame(
            self.frame_puissance4,
            style="Carte.TFrame",
            padding=8
        )
        config.pack(padx=25, fill="x")

        ttk.Radiobutton(
            config,
            text="Contre l'ordinateur",
            variable=self.puissance4_mode,
            value="ordinateur"
        ).pack()

        ttk.Radiobutton(
            config,
            text="Deux joueurs",
            variable=self.puissance4_mode,
            value="joueur"
        ).pack()

        self.puissance4_nom1 = ttk.Entry(config, width=22)
        self.puissance4_nom1.insert(0, "Joueur 1")
        self.puissance4_nom1.pack(pady=2)

        self.puissance4_nom2 = ttk.Entry(config, width=22)
        self.puissance4_nom2.insert(0, "Joueur 2")
        self.puissance4_nom2.pack(pady=2)

        ttk.Button(
            config,
            text="▶ Commencer",
            command=self.lancer_puissance4,
            style="Principal.TButton"
        ).pack()

        self.puissance4_info = ttk.Label(
            self.frame_puissance4,
            text="Commence une partie.",
            style="CarteTitre.TLabel"
        )
        self.puissance4_info.pack(pady=5)

        self.puissance4_canvas = tk.Canvas(
            self.frame_puissance4,
            width=420,
            height=360,
            bg="#2563eb",
            highlightthickness=0
        )
        self.puissance4_canvas.pack()
        self.puissance4_canvas.bind(
            "<Button-1>",
            self.clic_puissance4
        )

        self.bouton_menu(self.frame_puissance4)

    def afficher_puissance4(self):
        self.masquer_frames()
        self.frame_puissance4.pack(fill="both", expand=True)

    def lancer_puissance4(self):
        self.puissance4_j1 = self.puissance4_nom1.get() or "Joueur 1"
        self.puissance4_j2 = (
            "Ordinateur"
            if self.puissance4_mode.get() == "ordinateur"
            else self.puissance4_nom2.get() or "Joueur 2"
        )
        self.puissance4_plateau = [
            [0 for _ in range(7)] for _ in range(6)
        ]
        self.puissance4_joueur = 1
        self.puissance4_en_cours = True
        self.dessiner_puissance4()

    def dessiner_puissance4(self):
        self.puissance4_canvas.delete("all")

        for ligne in range(6):
            for colonne in range(7):
                x = colonne * 60 + 30
                y = ligne * 60 + 30
                valeur = self.puissance4_plateau[ligne][colonne]
                couleur = (
                    "#f8fafc" if valeur == 0
                    else "#ef4444" if valeur == 1
                    else "#facc15"
                )

                self.puissance4_canvas.create_oval(
                    x - 24, y - 24, x + 24, y + 24,
                    fill=couleur,
                    outline="#1e3a8a",
                    width=2
                )

    def clic_puissance4(self, evenement):
        if not self.puissance4_en_cours:
            return

        if (
            self.puissance4_mode.get() == "ordinateur"
            and self.puissance4_joueur == 2
        ):
            return

        self.jouer_colonne_puissance4(
            int(evenement.x // 60)
        )

    def jouer_colonne_puissance4(self, colonne):
        if not 0 <= colonne < 7:
            return

        ligne = None

        for index in range(5, -1, -1):
            if self.puissance4_plateau[index][colonne] == 0:
                ligne = index
                break

        if ligne is None:
            return

        joueur = self.puissance4_joueur
        self.puissance4_plateau[ligne][colonne] = joueur
        self.dessiner_puissance4()

        if self.victoire_puissance4(joueur):
            nom = self.puissance4_j1 if joueur == 1 else self.puissance4_j2
            self.fin_puissance4(f"{nom} gagne !", nom)
            return

        if all(self.puissance4_plateau[0][c] for c in range(7)):
            self.fin_puissance4("Match nul !", None)
            return

        self.puissance4_joueur = 2 if joueur == 1 else 1

        if (
            self.puissance4_mode.get() == "ordinateur"
            and self.puissance4_joueur == 2
        ):
            self.fenetre.after(
                400,
                self.tour_ordinateur_puissance4
            )

    def tour_ordinateur_puissance4(self):
        colonnes = [
            colonne for colonne in range(7)
            if self.puissance4_plateau[0][colonne] == 0
        ]

        if colonnes:
            self.jouer_colonne_puissance4(
                random.choice(colonnes)
            )

    def victoire_puissance4(self, joueur):
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))

        for ligne in range(6):
            for colonne in range(7):
                for dl, dc in directions:
                    positions = []

                    for index in range(4):
                        l = ligne + index * dl
                        c = colonne + index * dc

                        if not (0 <= l < 6 and 0 <= c < 7):
                            break

                        positions.append(
                            self.puissance4_plateau[l][c]
                        )

                    if positions == [joueur] * 4:
                        return True

        return False

    def fin_puissance4(self, message, gagnant):
        self.puissance4_en_cours = False

        if gagnant:
            ajouter_top("Puissance 4", gagnant, 1)

        messagebox.showinfo("Puissance 4", message)

    # =====================================================
    # BATAILLE NAVALE
    # =====================================================

    def creer_bataille(self):
        self.frame_bataille = ttk.Frame(self.fenetre)
        self.bataille_en_cours = False

        ttk.Label(
            self.frame_bataille,
            text="⚓ BATAILLE NAVALE",
            style="Titre.TLabel"
        ).pack(pady=10)

        config = ttk.Frame(
            self.frame_bataille,
            style="Carte.TFrame",
            padding=10
        )
        config.pack(padx=25, fill="x")

        self.bataille_nom = ttk.Entry(config, width=25)
        self.bataille_nom.insert(0, "Joueur")
        self.bataille_nom.pack(pady=5)

        ttk.Button(
            config,
            text="▶ Commencer",
            command=self.lancer_bataille,
            style="Principal.TButton"
        ).pack()

        self.bataille_info = ttk.Label(
            self.frame_bataille,
            text="Clique sur une case pour tirer.",
            style="CarteTitre.TLabel"
        )
        self.bataille_info.pack(pady=8)

        self.bataille_canvas = tk.Canvas(
            self.frame_bataille,
            width=400,
            height=400,
            bg="#2563eb",
            highlightthickness=0
        )
        self.bataille_canvas.pack()
        self.bataille_canvas.bind(
            "<Button-1>",
            self.clic_bataille
        )

        self.bouton_menu(self.frame_bataille)

    def afficher_bataille(self):
        self.masquer_frames()
        self.frame_bataille.pack(fill="both", expand=True)

    def grille_vide(self):
        return [[0 for _ in range(8)] for _ in range(8)]

    def placer_navires(self, grille):
        for taille in (4, 3, 3, 2):
            while True:
                direction = random.choice(("horizontal", "vertical"))
                ligne = random.randrange(8)
                colonne = random.randrange(8)
                cases = []

                for index in range(taille):
                    l = ligne + index if direction == "vertical" else ligne
                    c = colonne + index if direction == "horizontal" else colonne

                    if not (0 <= l < 8 and 0 <= c < 8):
                        break

                    cases.append((l, c))
                else:
                    if all(grille[l][c] == 0 for l, c in cases):
                        for l, c in cases:
                            grille[l][c] = 1
                        break

    def lancer_bataille(self):
        self.bataille_nom_joueur = (
            self.bataille_nom.get().strip() or "Joueur"
        )
        self.bataille_grille = self.grille_vide()
        self.bataille_tirs = self.grille_vide()
        self.placer_navires(self.bataille_grille)
        self.bataille_en_cours = True
        self.dessiner_bataille()
        self.bataille_info.config(text="À toi de jouer.")

    def dessiner_bataille(self):
        self.bataille_canvas.delete("all")

        for ligne in range(8):
            for colonne in range(8):
                x1 = colonne * 50
                y1 = ligne * 50
                tir = self.bataille_tirs[ligne][colonne]
                couleur = "#60a5fa"

                if tir == 2:
                    couleur = "#dc2626"
                elif tir == 3:
                    couleur = "#e5e7eb"

                self.bataille_canvas.create_rectangle(
                    x1,
                    y1,
                    x1 + 50,
                    y1 + 50,
                    fill=couleur,
                    outline="#1e3a8a"
                )

    def clic_bataille(self, evenement):
        if not self.bataille_en_cours:
            return

        ligne = int(evenement.y // 50)
        colonne = int(evenement.x // 50)

        if not (0 <= ligne < 8 and 0 <= colonne < 8):
            return

        if self.bataille_tirs[ligne][colonne] != 0:
            return

        if self.bataille_grille[ligne][colonne] == 1:
            self.bataille_tirs[ligne][colonne] = 2
            self.bataille_info.config(text="Touché !")
        else:
            self.bataille_tirs[ligne][colonne] = 3
            self.bataille_info.config(text="À l'eau !")

        self.dessiner_bataille()

        if all(
            self.bataille_grille[l][c] == 0
            or self.bataille_tirs[l][c] == 2
            for l in range(8)
            for c in range(8)
        ):
            self.bataille_en_cours = False
            ajouter_top(
                "Bataille navale",
                self.bataille_nom_joueur,
                1
            )
            messagebox.showinfo(
                "Bataille navale",
                "Bravo, tu as gagné !"
            )

    # =====================================================
    # QUIZ
    # =====================================================

    def creer_quiz(self):
        self.frame_quiz = ttk.Frame(self.fenetre)

        ttk.Label(
            self.frame_quiz,
            text="🧠 QUIZ",
            style="Titre.TLabel"
        ).pack(pady=15)

        config = ttk.Frame(
            self.frame_quiz,
            style="Carte.TFrame",
            padding=15
        )
        config.pack(padx=35, fill="x")

        self.quiz_categorie = tk.StringVar(
            value="Tables de multiplication"
        )

        categories = (
            "Tables de multiplication",
            "Culture générale",
            "Sciences",
            "Géographie"
        )

        for categorie in categories:
            ttk.Radiobutton(
                config,
                text=categorie,
                variable=self.quiz_categorie,
                value=categorie
            ).pack(anchor="w")

        self.quiz_nom = ttk.Entry(config, width=24)
        self.quiz_nom.insert(0, "Joueur")
        self.quiz_nom.pack(pady=8)

        ttk.Button(
            config,
            text="▶ Commencer",
            command=self.lancer_quiz,
            style="Principal.TButton"
        ).pack()

        jeu = ttk.Frame(
            self.frame_quiz,
            style="Carte.TFrame",
            padding=20
        )
        jeu.pack(padx=35, pady=15, fill="x")

        self.quiz_progression = ttk.Label(
            jeu,
            text="Question : 0/10",
            style="Stats.TLabel"
        )
        self.quiz_progression.pack()

        self.quiz_question = ttk.Label(
            jeu,
            text="Commence une partie.",
            style="CarteTitre.TLabel",
            wraplength=600
        )
        self.quiz_question.pack(pady=15)

        self.quiz_reponse = ttk.Entry(jeu, width=25)
        self.quiz_reponse.pack(pady=5)
        self.quiz_reponse.bind(
            "<Return>",
            lambda event: self.verifier_quiz()
        )

        self.quiz_bouton = ttk.Button(
            jeu,
            text="Répondre",
            command=self.verifier_quiz,
            state="disabled",
            style="Principal.TButton"
        )
        self.quiz_bouton.pack()

        self.quiz_resultat = ttk.Label(
            jeu,
            text="",
            style="Info.TLabel"
        )
        self.quiz_resultat.pack(pady=8)

        self.bouton_menu(self.frame_quiz)
        self.quiz_en_cours = False

    def afficher_quiz(self):
        self.masquer_frames()
        self.frame_quiz.pack(fill="both", expand=True)

    def lancer_quiz(self):
        self.quiz_nom_joueur = self.quiz_nom.get() or "Joueur"
        categorie = self.quiz_categorie.get()

        if categorie == "Tables de multiplication":
            questions = [
                (
                    f"{a} × {b} = ?",
                    str(a * b)
                )
                for a, b in (
                    (
                        random.randint(1, 10),
                        random.randint(1, 10)
                    )
                    for _ in range(10)
                )
            ]
        elif categorie == "Culture générale":
            questions = [
                ("Capitale de la France ?", "paris"),
                ("Nombre de continents ?", "7"),
                ("Peintre de la Joconde ?", "leonard de vinci"),
                ("Plus grand océan ?", "pacifique"),
                ("Côtés d'un triangle ?", "3"),
                ("Langue du Brésil ?", "portugais"),
                ("Planète rouge ?", "mars"),
                ("Animal qui miaule ?", "chat"),
                ("Mois dans une année ?", "12"),
                ("Contraire de chaud ?", "froid")
            ]
        elif categorie == "Sciences":
            questions = [
                ("Formule de l'eau ?", "h2o"),
                ("Pattes d'une araignée ?", "8"),
                ("Organe qui pompe le sang ?", "coeur"),
                ("Planète proche du Soleil ?", "mercure"),
                ("État de la glace ?", "solide"),
                ("Force qui attire au sol ?", "gravite"),
                ("Organe de la vue ?", "oeil"),
                ("Os chez l'adulte ?", "206"),
                ("Gaz nécessaire pour respirer ?", "oxygene"),
                ("Animal qui allaite ?", "mammifere")
            ]
        else:
            questions = [
                ("Capitale de l'Espagne ?", "madrid"),
                ("Capitale de l'Italie ?", "rome"),
                ("Capitale de l'Allemagne ?", "berlin"),
                ("Capitale du Portugal ?", "lisbonne"),
                ("Pays de Tokyo ?", "japon"),
                ("Pays en forme de botte ?", "italie"),
                ("Continent de l'Égypte ?", "afrique"),
                ("Plus grand pays ?", "russie"),
                ("Capitale du Royaume-Uni ?", "londres"),
                ("Océan à l'ouest de la France ?", "atlantique")
            ]

        self.quiz_categorie_active = categorie
        self.quiz_questions = questions
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_en_cours = True
        self.quiz_bouton.config(state="normal")
        self.afficher_question_quiz()

    def afficher_question_quiz(self):
        question, _ = self.quiz_questions[self.quiz_index]
        self.quiz_progression.config(
            text=f"Question : {self.quiz_index + 1}/10"
        )
        self.quiz_question.config(text=question)
        self.quiz_reponse.delete(0, tk.END)
        self.quiz_reponse.focus()

    def normaliser(self, texte):
        return (
            texte.lower()
            .strip()
            .replace("é", "e")
            .replace("è", "e")
            .replace("ê", "e")
            .replace("à", "a")
            .replace("î", "i")
            .replace("ô", "o")
            .replace("û", "u")
        )

    def verifier_quiz(self):
        if not self.quiz_en_cours:
            return

        reponse = self.normaliser(self.quiz_reponse.get())
        _, solution = self.quiz_questions[self.quiz_index]

        if reponse == self.normaliser(solution):
            self.quiz_score += 1
            self.quiz_resultat.config(text="✅ Bonne réponse !")
        else:
            self.quiz_resultat.config(
                text=f"❌ Réponse : {solution}"
            )

        self.quiz_index += 1

        if self.quiz_index == 10:
            self.terminer_quiz()
        else:
            self.fenetre.after(
                600,
                self.afficher_question_quiz
            )

    def terminer_quiz(self):
        self.quiz_en_cours = False
        self.quiz_bouton.config(state="disabled")

        ajouter_top(
            f"Quiz - {self.quiz_categorie_active}",
            self.quiz_nom_joueur,
            self.quiz_score
        )

        messagebox.showinfo(
            "Quiz terminé",
            f"Score : {self.quiz_score}/10"
        )

    # =====================================================
    # PENDU
    # =====================================================

    def creer_pendu(self):
        self.frame_pendu = ttk.Frame(self.fenetre)

        ttk.Label(
            self.frame_pendu,
            text="🔤 JEU DU PENDU",
            style="Titre.TLabel"
        ).pack(pady=15)

        config = ttk.Frame(
            self.frame_pendu,
            style="Carte.TFrame",
            padding=15
        )
        config.pack(padx=35, fill="x")

        self.pendu_nom = ttk.Entry(config, width=25)
        self.pendu_nom.insert(0, "Joueur")
        self.pendu_nom.pack(pady=5)

        ttk.Button(
            config,
            text="▶ Nouvelle partie",
            command=self.lancer_pendu,
            style="Principal.TButton"
        ).pack()

        jeu = ttk.Frame(
            self.frame_pendu,
            style="Carte.TFrame",
            padding=20
        )
        jeu.pack(padx=35, pady=15, fill="x")

        self.pendu_mot_label = ttk.Label(
            jeu,
            text="Clique sur Nouvelle partie.",
            style="CarteTitre.TLabel",
            font=("Arial", 20, "bold")
        )
        self.pendu_mot_label.pack(pady=15)

        self.pendu_info = ttk.Label(
            jeu,
            text="",
            style="Stats.TLabel"
        )
        self.pendu_info.pack(pady=5)

        self.pendu_lettre = ttk.Entry(
            jeu,
            width=10,
            justify="center"
        )
        self.pendu_lettre.pack(pady=5)
        self.pendu_lettre.bind(
            "<Return>",
            lambda event: self.proposer_lettre()
        )

        self.pendu_bouton = ttk.Button(
            jeu,
            text="Proposer",
            command=self.proposer_lettre,
            state="disabled",
            style="Principal.TButton"
        )
        self.pendu_bouton.pack()

        self.pendu_resultat = ttk.Label(
            jeu,
            text="",
            style="Info.TLabel"
        )
        self.pendu_resultat.pack(pady=8)

        self.bouton_menu(self.frame_pendu)
        self.pendu_en_cours = False

    def afficher_pendu(self):
        self.masquer_frames()
        self.frame_pendu.pack(fill="both", expand=True)

    def lancer_pendu(self):
        mots = (
            "ordinateur",
            "python",
            "clavier",
            "fenetre",
            "montagne",
            "chocolat",
            "telephone",
            "vacances",
            "bibliotheque",
            "arcenciel",
            "elephant"
        )

        self.pendu_mot = random.choice(mots)
        self.pendu_nom_joueur = self.pendu_nom.get() or "Joueur"
        self.pendu_trouvees = set()
        self.pendu_ratees = set()
        self.pendu_erreurs = 0
        self.pendu_max_erreurs = 7
        self.pendu_en_cours = True

        self.pendu_bouton.config(state="normal")
        self.pendu_lettre.config(state="normal")
        self.pendu_resultat.config(text="")
        self.actualiser_pendu()
        self.pendu_lettre.focus()

    def actualiser_pendu(self):
        affichage = " ".join(
            lettre if lettre in self.pendu_trouvees else "_"
            for lettre in self.pendu_mot
        )

        self.pendu_mot_label.config(text=affichage)
        self.pendu_info.config(
            text=(
                f"Erreurs : {self.pendu_erreurs}/"
                f"{self.pendu_max_erreurs}\n"
                f"Lettres ratées : "
                f"{', '.join(sorted(self.pendu_ratees))}"
            )
        )

    def proposer_lettre(self):
        if not self.pendu_en_cours:
            return

        lettre = self.pendu_lettre.get().strip().lower()
        self.pendu_lettre.delete(0, tk.END)

        if len(lettre) != 1 or not lettre.isalpha():
            messagebox.showwarning(
                "Erreur",
                "Entre une seule lettre."
            )
            return

        if lettre in self.pendu_trouvees or lettre in self.pendu_ratees:
            messagebox.showwarning(
                "Erreur",
                "Cette lettre a déjà été proposée."
            )
            return

        if lettre in self.pendu_mot:
            self.pendu_trouvees.add(lettre)
            self.pendu_resultat.config(text="✅ Bonne lettre !")
        else:
            self.pendu_ratees.add(lettre)
            self.pendu_erreurs += 1
            self.pendu_resultat.config(text="❌ Mauvaise lettre !")

        self.actualiser_pendu()

        if all(
            lettre in self.pendu_trouvees
            for lettre in self.pendu_mot
        ):
            self.terminer_pendu(True)
        elif self.pendu_erreurs >= self.pendu_max_erreurs:
            self.terminer_pendu(False)

    def terminer_pendu(self, gagne):
        self.pendu_en_cours = False
        self.pendu_bouton.config(state="disabled")
        self.pendu_lettre.config(state="disabled")

        if gagne:
            score = self.pendu_max_erreurs - self.pendu_erreurs
            ajouter_top(
                "Pendu",
                self.pendu_nom_joueur,
                score
            )
            message = (
                f"Bravo !\nMot : {self.pendu_mot}\n"
                f"Score : {score}/7"
            )
        else:
            message = f"Perdu !\nLe mot était : {self.pendu_mot}"

        self.pendu_mot_label.config(text=self.pendu_mot)
        messagebox.showinfo("Pendu", message)

    # =====================================================
    # ECHECS
    # =====================================================

    def creer_echecs(self):
        self.frame_echecs_choix = ttk.Frame(self.fenetre)
        ttk.Label(
            self.frame_echecs_choix,
            text="♟ ÉCHECS",
            style="Titre.TLabel"
        ).pack(pady=(90, 10))
        ttk.Label(
            self.frame_echecs_choix,
            text="Choisis le mode de jeu",
            style="SousTitre.TLabel"
        ).pack(pady=5)
        ttk.Button(
            self.frame_echecs_choix,
            text="♟ Jouer contre l'ordinateur",
            command=lambda: self.preparer_echecs("ordinateur"),
            style="Principal.TButton",
            width=34
        ).pack(pady=8)
        ttk.Button(
            self.frame_echecs_choix,
            text="♟ Jouer à deux joueurs",
            command=lambda: self.preparer_echecs("joueur"),
            style="Principal.TButton",
            width=34
        ).pack(pady=8)
        self.bouton_menu(self.frame_echecs_choix)

        self.frame_echecs = ttk.Frame(self.fenetre)
        self.echecs_cases = []
        self.echecs_en_cours = False
        self.echecs_mode = tk.StringVar(value="ordinateur")
        self.echecs_ordinateur_joue = False

        ttk.Label(
            self.frame_echecs,
            text="♟ ÉCHECS",
            style="Titre.TLabel"
        ).pack(pady=(18, 5))

        configuration = ttk.Frame(
            self.frame_echecs,
            style="Carte.TFrame",
            padding=8
        )
        configuration.pack(padx=30, fill="x")

        ttk.Radiobutton(
            configuration,
            text="Jouer contre l'ordinateur",
            variable=self.echecs_mode,
            value="ordinateur"
        ).pack()
        ttk.Radiobutton(
            configuration,
            text="Jouer contre un joueur",
            variable=self.echecs_mode,
            value="joueur"
        ).pack()

        statut = ttk.Frame(
            self.frame_echecs,
            style="Carte.TFrame",
            padding=(16, 7)
        )
        statut.pack(padx=30, pady=(8, 2), fill="x")

        self.echecs_info = ttk.Label(
            statut,
            text="Lance une partie.",
            style="CarteTitre.TLabel"
        )
        self.echecs_info.pack()

        grille = tk.Frame(
            self.frame_echecs,
            bg="#263238",
            padx=9,
            pady=9,
            relief="ridge",
            borderwidth=2
        )
        grille.pack(pady=8)

        for ligne in range(8):
            ligne_cases = []
            for colonne in range(8):
                case = tk.Button(
                    grille,
                    width=2,
                    height=1,
                    font=("DejaVu Sans", 30, "bold"),
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                    padx=11,
                    pady=4,
                    command=lambda l=ligne, c=colonne:
                    self.jouer_echecs(l, c)
                )
                case.grid(row=ligne, column=colonne, padx=1, pady=1)
                ligne_cases.append(case)
            self.echecs_cases.append(ligne_cases)

        ttk.Button(
            self.frame_echecs,
            text="🔄 Nouvelle partie",
            command=self.lancer_echecs,
            style="Principal.TButton"
        ).pack(pady=6)

        self.bouton_menu(self.frame_echecs)

    def afficher_echecs(self):
        self.masquer_frames()
        self.frame_echecs_choix.pack(fill="both", expand=True)

    def preparer_echecs(self, mode):
        self.echecs_mode.set(mode)
        self.frame_echecs_choix.pack_forget()
        self.frame_echecs.pack(fill="both", expand=True)
        self.lancer_echecs()

    def lancer_echecs(self):
        if self.echecs_mode.get() == "joueur":
            nom_blanc = simpledialog.askstring(
                "Joueur 1", "Nom du joueur avec les blancs :",
                parent=self.fenetre
            )
            nom_noir = simpledialog.askstring(
                "Joueur 2", "Nom du joueur avec les noirs :",
                parent=self.fenetre
            )
            self.echecs_noms = {
                "blanc": nom_blanc or "Joueur 1",
                "noir": nom_noir or "Joueur 2"
            }
        else:
            nom_blanc = simpledialog.askstring(
                "Joueur", "Ton nom :", parent=self.fenetre
            )
            self.echecs_noms = {
                "blanc": nom_blanc or "Joueur",
                "noir": "Ordinateur"
            }

        self.echecs_plateau = [
            list("rnbqkbnr"),
            list("pppppppp"),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("PPPPPPPP"),
            list("RNBQKBNR")
        ]
        self.echecs_joueur = "blanc"
        self.echecs_selection = None
        self.echecs_en_cours = True
        self.echecs_ordinateur_joue = False
        self.echecs_roques = {
            "blanc": {"petit": True, "grand": True},
            "noir": {"petit": True, "grand": True}
        }
        self.actualiser_echecs()

    def actualiser_echecs(self):
        symboles = {
            "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
            "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
            ".": ""
        }

        for ligne in range(8):
            for colonne in range(8):
                case = self.echecs_cases[ligne][colonne]
                case_claire = (ligne + colonne) % 2 == 0
                couleur = "#c99862" if case_claire else "#38634f"
                piece = self.echecs_plateau[ligne][colonne]
                couleur_piece = (
                    "#ffffff" if piece.isupper() else "#111827"
                )
                if self.echecs_selection == (ligne, colonne):
                    couleur = "#e2aa3b"
                case.config(
                    text=symboles[piece],
                    bg=couleur,
                    fg=couleur_piece,
                    activebackground="#f0c75e"
                )

        self.echecs_info.config(
            text=(
                f"{self.echecs_noms[self.echecs_joueur]}, à toi. "
                "Clique une pièce puis sa destination."
            )
        )

    def couleur_piece_echecs(self, piece):
        if piece == ".":
            return None
        return "blanc" if piece.isupper() else "noir"

    def chemin_libre_echecs(self, depart, arrivee):
        ligne, colonne = depart
        destination_ligne, destination_colonne = arrivee
        pas_ligne = (destination_ligne > ligne) - (destination_ligne < ligne)
        pas_colonne = (destination_colonne > colonne) - (destination_colonne < colonne)
        ligne += pas_ligne
        colonne += pas_colonne

        while (ligne, colonne) != arrivee:
            if self.echecs_plateau[ligne][colonne] != ".":
                return False
            ligne += pas_ligne
            colonne += pas_colonne
        return True

    def roque_possible_echecs(self, depart, arrivee):
        ligne, colonne = depart
        destination_ligne, destination_colonne = arrivee
        couleur = self.echecs_joueur
        ligne_depart = 7 if couleur == "blanc" else 0

        if (
            ligne != ligne_depart
            or colonne != 4
            or destination_ligne != ligne_depart
            or destination_colonne not in (2, 6)
            or self.roi_en_echec_echecs(couleur)
        ):
            return False

        cote = "petit" if destination_colonne == 6 else "grand"
        colonne_tour = 7 if cote == "petit" else 0
        tour = "R" if couleur == "blanc" else "r"
        if (
            not self.echecs_roques[couleur][cote]
            or self.echecs_plateau[ligne_depart][colonne_tour] != tour
            or not self.chemin_libre_echecs(
                (ligne_depart, colonne),
                (ligne_depart, colonne_tour)
            )
        ):
            return False

        ancien_roi = self.echecs_plateau[ligne_depart][colonne]
        for colonne_roi in (5, 6) if cote == "petit" else (3, 2):
            self.echecs_plateau[ligne_depart][colonne] = "."
            self.echecs_plateau[ligne_depart][colonne_roi] = ancien_roi
            menace = self.roi_en_echec_echecs(couleur)
            self.echecs_plateau[ligne_depart][colonne_roi] = "."
            self.echecs_plateau[ligne_depart][colonne] = ancien_roi
            if menace:
                return False
        return True

    def mouvement_valide_echecs(self, depart, arrivee):
        ligne, colonne = depart
        destination_ligne, destination_colonne = arrivee
        piece = self.echecs_plateau[ligne][colonne]
        cible = self.echecs_plateau[destination_ligne][destination_colonne]
        if piece == "." or self.couleur_piece_echecs(piece) != self.echecs_joueur:
            return False
        if cible != "." and self.couleur_piece_echecs(cible) == self.echecs_joueur:
            return False

        delta_ligne = destination_ligne - ligne
        delta_colonne = destination_colonne - colonne
        type_piece = piece.lower()

        if type_piece == "p":
            direction = -1 if piece.isupper() else 1
            ligne_depart = 6 if piece.isupper() else 1
            if delta_colonne == 0 and cible == ".":
                return delta_ligne == direction or (
                    ligne == ligne_depart
                    and delta_ligne == 2 * direction
                    and self.echecs_plateau[ligne + direction][colonne] == "."
                )
            return abs(delta_colonne) == 1 and delta_ligne == direction and cible != "."

        if type_piece == "n":
            return sorted((abs(delta_ligne), abs(delta_colonne))) == [1, 2]
        if type_piece == "k":
            if abs(delta_colonne) == 2 and delta_ligne == 0:
                return self.roque_possible_echecs(depart, arrivee)
            return max(abs(delta_ligne), abs(delta_colonne)) == 1
        if type_piece == "r" and (delta_ligne == 0 or delta_colonne == 0):
            return self.chemin_libre_echecs(depart, arrivee)
        if type_piece == "b" and abs(delta_ligne) == abs(delta_colonne):
            return self.chemin_libre_echecs(depart, arrivee)
        if type_piece == "q" and (
            delta_ligne == 0
            or delta_colonne == 0
            or abs(delta_ligne) == abs(delta_colonne)
        ):
            return self.chemin_libre_echecs(depart, arrivee)
        return False

    def roi_en_echec_echecs(self, couleur):
        roi = "K" if couleur == "blanc" else "k"
        position_roi = None

        for ligne in range(8):
            for colonne in range(8):
                if self.echecs_plateau[ligne][colonne] == roi:
                    position_roi = (ligne, colonne)
                    break
            if position_roi is not None:
                break

        if position_roi is None:
            return True

        adversaire = "noir" if couleur == "blanc" else "blanc"
        ancien_joueur = self.echecs_joueur
        self.echecs_joueur = adversaire

        menacee = any(
            self.mouvement_valide_echecs(
                (ligne, colonne), position_roi
            )
            for ligne in range(8)
            for colonne in range(8)
            if self.couleur_piece_echecs(
                self.echecs_plateau[ligne][colonne]
            ) == adversaire
        )

        self.echecs_joueur = ancien_joueur
        return menacee

    def coup_legal_echecs(self, depart, arrivee, couleur):
        ancien_plateau = [ligne[:] for ligne in self.echecs_plateau]
        piece = self.echecs_plateau[depart[0]][depart[1]]
        self.echecs_plateau[arrivee[0]][arrivee[1]] = piece
        self.echecs_plateau[depart[0]][depart[1]] = "."

        if piece.lower() == "k" and abs(arrivee[1] - depart[1]) == 2:
            colonne_tour_depart = 7 if arrivee[1] == 6 else 0
            colonne_tour_arrivee = 5 if arrivee[1] == 6 else 3
            self.echecs_plateau[arrivee[0]][colonne_tour_arrivee] = (
                self.echecs_plateau[arrivee[0]][colonne_tour_depart]
            )
            self.echecs_plateau[arrivee[0]][colonne_tour_depart] = "."

        if piece == "P" and arrivee[0] == 0:
            self.echecs_plateau[arrivee[0]][arrivee[1]] = "Q"
        elif piece == "p" and arrivee[0] == 7:
            self.echecs_plateau[arrivee[0]][arrivee[1]] = "q"

        legal = not self.roi_en_echec_echecs(couleur)
        self.echecs_plateau = ancien_plateau
        return legal

    def coups_legaux_echecs(self, couleur):
        ancien_joueur = self.echecs_joueur
        self.echecs_joueur = couleur
        coups = []

        for ligne in range(8):
            for colonne in range(8):
                if self.couleur_piece_echecs(
                    self.echecs_plateau[ligne][colonne]
                ) != couleur:
                    continue
                for destination_ligne in range(8):
                    for destination_colonne in range(8):
                        depart = (ligne, colonne)
                        arrivee = (destination_ligne, destination_colonne)
                        if (
                            self.mouvement_valide_echecs(depart, arrivee)
                            and self.coup_legal_echecs(
                                depart, arrivee, couleur
                            )
                        ):
                            coups.append((depart, arrivee))

        self.echecs_joueur = ancien_joueur
        return coups

    def jouer_echecs(self, ligne, colonne):
        if not self.echecs_en_cours:
            return
        if (
            self.echecs_mode.get() == "ordinateur"
            and self.echecs_joueur == "noir"
            and not self.echecs_ordinateur_joue
        ):
            return

        if self.echecs_selection is None:
            piece = self.echecs_plateau[ligne][colonne]
            if self.couleur_piece_echecs(piece) == self.echecs_joueur:
                self.echecs_selection = (ligne, colonne)
                self.actualiser_echecs()
            return

        depart = self.echecs_selection
        if not self.mouvement_valide_echecs(depart, (ligne, colonne)) or not self.coup_legal_echecs(
            depart, (ligne, colonne), self.echecs_joueur
        ):
            self.echecs_selection = None
            self.actualiser_echecs()
            return

        piece = self.echecs_plateau[depart[0]][depart[1]]
        cible = self.echecs_plateau[ligne][colonne]

        if piece.lower() == "k":
            self.echecs_roques[self.echecs_joueur]["petit"] = False
            self.echecs_roques[self.echecs_joueur]["grand"] = False
        elif piece.lower() == "r":
            if depart == (7, 0) or depart == (0, 0):
                self.echecs_roques[self.echecs_joueur]["grand"] = False
            elif depart == (7, 7) or depart == (0, 7):
                self.echecs_roques[self.echecs_joueur]["petit"] = False

        couleur_adverse = "noir" if self.echecs_joueur == "blanc" else "blanc"
        if cible.lower() == "r":
            if ligne == (7 if couleur_adverse == "blanc" else 0) and colonne == 0:
                self.echecs_roques[couleur_adverse]["grand"] = False
            elif ligne == (7 if couleur_adverse == "blanc" else 0) and colonne == 7:
                self.echecs_roques[couleur_adverse]["petit"] = False

        self.echecs_plateau[ligne][colonne] = piece
        self.echecs_plateau[depart[0]][depart[1]] = "."

        if piece.lower() == "k" and abs(colonne - depart[1]) == 2:
            colonne_tour_depart = 7 if colonne == 6 else 0
            colonne_tour_arrivee = 5 if colonne == 6 else 3
            self.echecs_plateau[ligne][colonne_tour_arrivee] = (
                self.echecs_plateau[ligne][colonne_tour_depart]
            )
            self.echecs_plateau[ligne][colonne_tour_depart] = "."

        if piece == "P" and ligne == 0:
            self.echecs_plateau[ligne][colonne] = "Q"
        elif piece == "p" and ligne == 7:
            self.echecs_plateau[ligne][colonne] = "q"

        self.echecs_selection = None
        if cible.lower() == "k":
            gagnant = self.echecs_noms[self.echecs_joueur]
            self.echecs_en_cours = False
            ajouter_top("Échecs", gagnant, 1)
            self.actualiser_echecs()
            messagebox.showinfo("Échecs", f"{gagnant} gagne !")
            return

        self.echecs_joueur = "noir" if self.echecs_joueur == "blanc" else "blanc"
        self.actualiser_echecs()

        coups_adversaire = self.coups_legaux_echecs(self.echecs_joueur)
        if not coups_adversaire:
            self.echecs_en_cours = False
            if self.roi_en_echec_echecs(self.echecs_joueur):
                gagnant = self.echecs_noms[
                    "noir" if self.echecs_joueur == "blanc" else "blanc"
                ]
                ajouter_top("Échecs", gagnant, 1)
                message = f"Échec et mat ! {gagnant} gagne !"
            else:
                message = "Pat ! La partie est nulle."
            messagebox.showinfo("Échecs", message)
            return

        if (
            self.echecs_mode.get() == "ordinateur"
            and self.echecs_joueur == "noir"
        ):
            self.echecs_ordinateur_joue = True
            self.fenetre.after(350, self.tour_ordinateur_echecs)

    def tour_ordinateur_echecs(self):
        if not self.echecs_en_cours or self.echecs_joueur != "noir":
            return

        coups_possibles = []
        for ligne in range(8):
            for colonne in range(8):
                if self.couleur_piece_echecs(
                    self.echecs_plateau[ligne][colonne]
                ) != "noir":
                    continue
                for destination_ligne in range(8):
                    for destination_colonne in range(8):
                        if self.mouvement_valide_echecs(
                            (ligne, colonne),
                            (destination_ligne, destination_colonne)
                        ) and self.coup_legal_echecs(
                            (ligne, colonne),
                            (destination_ligne, destination_colonne),
                            "noir"
                        ):
                            coups_possibles.append(
                                (
                                    (ligne, colonne),
                                    (destination_ligne, destination_colonne)
                                )
                            )

        if coups_possibles:
            depart, destination = random.choice(coups_possibles)
            self.echecs_selection = depart
            self.jouer_echecs(*destination)
        self.echecs_ordinateur_joue = False

    # =====================================================
    # SNAKE
    # =====================================================

    def creer_snake(self):
        self.frame_snake = ttk.Frame(self.fenetre)
        self.snake_timer = None
        self.snake_en_cours = False

        ttk.Label(
            self.frame_snake,
            text="🐍 SNAKE",
            style="Titre.TLabel"
        ).pack(pady=(18, 5))

        self.snake_score_label = ttk.Label(
            self.frame_snake,
            text="Score : 0",
            style="Stats.TLabel"
        )
        self.snake_score_label.pack()

        ttk.Label(
            self.frame_snake,
            text="Utilise les flèches du clavier pour diriger le serpent.",
            style="SousTitre.TLabel"
        ).pack(pady=5)

        self.snake_canvas = tk.Canvas(
            self.frame_snake,
            width=400,
            height=400,
            bg="#102a43",
            takefocus=True,
            highlightthickness=0,
            relief="ridge",
            borderwidth=6,
            highlightbackground="#38b2ac"
        )
        self.snake_canvas.pack(pady=10)

        ttk.Button(
            self.frame_snake,
            text="🔄 Nouvelle partie",
            command=self.lancer_snake,
            style="Principal.TButton"
        ).pack(pady=5)

        self.bouton_menu(self.frame_snake)

    def afficher_snake(self):
        self.masquer_frames()
        self.frame_snake.pack(fill="both", expand=True)
        self.lancer_snake()
        self.snake_canvas.focus_set()

    def lancer_snake(self):
        if self.snake_timer is not None:
            self.fenetre.after_cancel(self.snake_timer)

        self.snake_taille = 20
        self.snake_serpent = [(10, 10), (9, 10), (8, 10)]
        self.snake_direction = None
        self.snake_prochaine_direction = None
        self.snake_score = 0
        self.snake_en_cours = True
        self.snake_nourriture = self.creer_nourriture_snake()
        self.actualiser_snake()

    def creer_nourriture_snake(self):
        cases_libres = [
            (colonne, ligne)
            for colonne in range(20)
            for ligne in range(20)
            if (colonne, ligne) not in self.snake_serpent
        ]
        return random.choice(cases_libres)

    def actualiser_snake(self):
        self.snake_canvas.delete("all")
        taille = self.snake_taille

        for position, (colonne, ligne) in enumerate(self.snake_serpent):
            marge = 2
            self.snake_canvas.create_rectangle(
                colonne * taille + marge,
                ligne * taille + marge,
                (colonne + 1) * taille - marge,
                (ligne + 1) * taille - marge,
                fill="#68d391" if position == 0 else "#38a169",
                outline=""
            )

        colonne, ligne = self.snake_nourriture
        self.snake_canvas.create_oval(
            colonne * taille + 4,
            ligne * taille + 4,
            (colonne + 1) * taille - 4,
            (ligne + 1) * taille - 4,
            fill="#f56565",
            outline=""
        )
        self.snake_score_label.config(text=f"Score : {self.snake_score}")

    def touche_snake(self, evenement):
        directions = {
            "Left": (-1, 0),
            "Right": (1, 0),
            "Up": (0, -1),
            "Down": (0, 1)
        }
        nouvelle_direction = directions.get(evenement.keysym)
        if nouvelle_direction is None:
            return

        if self.snake_direction is None:
            self.snake_direction = nouvelle_direction
            self.snake_prochaine_direction = nouvelle_direction
            self.avancer_snake()
            return

        direction_actuelle = self.snake_direction
        if nouvelle_direction == (
            -direction_actuelle[0],
            -direction_actuelle[1]
        ):
            return
        self.snake_prochaine_direction = nouvelle_direction

    def avancer_snake(self):
        if not self.snake_en_cours:
            return

        if self.snake_prochaine_direction is None:
            return

        self.snake_direction = self.snake_prochaine_direction
        tete_colonne, tete_ligne = self.snake_serpent[0]
        direction_colonne, direction_ligne = self.snake_direction
        nouvelle_tete = (
            tete_colonne + direction_colonne,
            tete_ligne + direction_ligne
        )

        collision_mur = not (
            0 <= nouvelle_tete[0] < 20
            and 0 <= nouvelle_tete[1] < 20
        )
        collision_serpent = nouvelle_tete in self.snake_serpent[:-1]
        if collision_mur:
            self.terminer_snake("Le serpent a touché un mur.")
            return
        if collision_serpent:
            self.terminer_snake("Le serpent s'est mordu.")
            return

        self.snake_serpent.insert(0, nouvelle_tete)
        if nouvelle_tete == self.snake_nourriture:
            self.snake_score += 1
            self.snake_nourriture = self.creer_nourriture_snake()
        else:
            self.snake_serpent.pop()

        self.actualiser_snake()
        self.snake_timer = self.fenetre.after(110, self.avancer_snake)

    def terminer_snake(self, raison):
        self.snake_en_cours = False
        self.snake_timer = None
        joueur = simpledialog.askstring(
            "Classement Snake",
            "Ton nom :",
            parent=self.fenetre
        ) or "Anonyme"
        ajouter_top("Snake", joueur, self.snake_score)
        messagebox.showinfo(
            "Snake",
            f"{raison}\nScore : {self.snake_score}",
            parent=self.fenetre
        )

    # =====================================================
    # TETRIS
    # =====================================================

    def creer_tetris(self):
        self.frame_tetris_choix = ttk.Frame(self.fenetre)
        self.frame_tetris = ttk.Frame(self.fenetre)
        self.tetris_timer = None
        self.tetris_en_cours = False
        self.tetris_difficulte = "facile"

        ttk.Label(
            self.frame_tetris_choix,
            text="🧱 TETRIS",
            style="Titre.TLabel"
        ).pack(pady=(85, 10))
        ttk.Label(
            self.frame_tetris_choix,
            text="Choisis la difficulté",
            style="SousTitre.TLabel"
        ).pack(pady=5)

        for difficulte, texte in (
            ("facile", "🟢 Facile"),
            ("moyen", "🟡 Moyen"),
            ("difficile", "🔴 Difficile")
        ):
            ttk.Button(
                self.frame_tetris_choix,
                text=texte,
                command=lambda niveau=difficulte:
                self.preparer_tetris(niveau),
                style="Principal.TButton",
                width=30
            ).pack(pady=7)

        self.bouton_menu(self.frame_tetris_choix)

        ttk.Label(
            self.frame_tetris,
            text="🧱 TETRIS",
            style="Titre.TLabel"
        ).pack(pady=(15, 3))
        self.tetris_info = ttk.Label(
            self.frame_tetris,
            text="Flèches : déplacer | Haut : tourner | Espace : tourner",
            style="SousTitre.TLabel"
        )
        self.tetris_info.pack()
        self.tetris_score_label = ttk.Label(
            self.frame_tetris,
            text="Score : 0",
            style="Stats.TLabel"
        )
        self.tetris_score_label.pack(pady=4)

        self.tetris_canvas = tk.Canvas(
            self.frame_tetris,
            width=300,
            height=600,
            bg="#172033",
            highlightthickness=0,
            relief="ridge",
            borderwidth=5,
            highlightbackground="#818cf8"
        )
        self.tetris_canvas.pack(pady=8)

        ttk.Button(
            self.frame_tetris,
            text="🔄 Nouvelle partie",
            command=self.lancer_tetris,
            style="Principal.TButton"
        ).pack(pady=4)
        self.bouton_menu(self.frame_tetris)

    def afficher_tetris(self):
        self.masquer_frames()
        self.frame_tetris_choix.pack(fill="both", expand=True)

    def preparer_tetris(self, difficulte):
        self.tetris_difficulte = difficulte
        self.frame_tetris_choix.pack_forget()
        self.frame_tetris.pack(fill="both", expand=True)
        self.lancer_tetris()
        self.fenetre.focus_set()

    def lancer_tetris(self):
        if self.tetris_timer is not None:
            self.fenetre.after_cancel(self.tetris_timer)

        self.tetris_plateau = [[0] * 10 for _ in range(20)]
        self.tetris_score = 0
        self.tetris_en_cours = True
        self.tetris_piece = None
        self.tetris_piece_x = 0
        self.tetris_piece_y = 0
        self.tetris_forme = None
        self.tetris_nouvelle_piece()

    def tetris_formes(self):
        return [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (1, 1), (2, 1)]
        ]

    def tetris_vitesse(self):
        return {
            "facile": 650,
            "moyen": 400,
            "difficile": 220
        }[self.tetris_difficulte]

    def tetris_positions(self, forme=None, x=None, y=None):
        forme = self.tetris_forme if forme is None else forme
        x = self.tetris_piece_x if x is None else x
        y = self.tetris_piece_y if y is None else y
        return [(x + colonne, y + ligne) for colonne, ligne in forme]

    def tetris_collision(self, forme, x, y):
        for colonne, ligne in self.tetris_positions(forme, x, y):
            if colonne < 0 or colonne >= 10 or ligne >= 20:
                return True
            if ligne >= 0 and self.tetris_plateau[ligne][colonne]:
                return True
        return False

    def tetris_nouvelle_piece(self):
        self.tetris_piece = random.randint(1, 7)
        self.tetris_forme = self.tetris_formes()[self.tetris_piece - 1]
        self.tetris_piece_x = 3
        self.tetris_piece_y = 0
        if self.tetris_collision(
            self.tetris_forme,
            self.tetris_piece_x,
            self.tetris_piece_y
        ):
            self.terminer_tetris()
            return
        self.actualiser_tetris()
        self.tetris_timer = self.fenetre.after(
            self.tetris_vitesse(), self.avancer_tetris
        )

    def actualiser_tetris(self):
        self.tetris_canvas.delete("all")
        couleurs = {
            1: "#38bdf8", 2: "#facc15", 3: "#c084fc",
            4: "#fb923c", 5: "#60a5fa", 6: "#4ade80", 7: "#f87171"
        }

        for ligne in range(20):
            for colonne in range(10):
                valeur = self.tetris_plateau[ligne][colonne]
                self.tetris_dessiner_case(
                    colonne, ligne, couleurs.get(valeur, "#243047")
                )

        if self.tetris_forme is not None:
            for colonne, ligne in self.tetris_positions():
                if ligne >= 0:
                    self.tetris_dessiner_case(
                        colonne,
                        ligne,
                        couleurs.get(self.tetris_piece, "#ffffff")
                    )
        self.tetris_score_label.config(text=f"Score : {self.tetris_score}")

    def tetris_dessiner_case(self, colonne, ligne, couleur):
        taille = 30
        self.tetris_canvas.create_rectangle(
            colonne * taille + 1,
            ligne * taille + 1,
            (colonne + 1) * taille - 1,
            (ligne + 1) * taille - 1,
            fill=couleur,
            outline="#111827"
        )

    def deplacer_tetris(self, delta_colonne, delta_ligne):
        nouvelle_colonne = self.tetris_piece_x + delta_colonne
        nouvelle_ligne = self.tetris_piece_y + delta_ligne
        if not self.tetris_collision(
            self.tetris_forme, nouvelle_colonne, nouvelle_ligne
        ):
            self.tetris_piece_x = nouvelle_colonne
            self.tetris_piece_y = nouvelle_ligne
            self.actualiser_tetris()
            return True
        return False

    def tourner_tetris(self):
        forme = [(-ligne, colonne) for colonne, ligne in self.tetris_forme]
        minimum_colonne = min(colonne for colonne, ligne in forme)
        minimum_ligne = min(ligne for colonne, ligne in forme)
        forme = [
            (colonne - minimum_colonne, ligne - minimum_ligne)
            for colonne, ligne in forme
        ]
        if not self.tetris_collision(
            forme, self.tetris_piece_x, self.tetris_piece_y
        ):
            self.tetris_forme = forme
            self.actualiser_tetris()

    def avancer_tetris(self):
        if not self.tetris_en_cours:
            return
        if not self.deplacer_tetris(0, 1):
            self.bloquer_tetris()
        else:
            self.tetris_timer = self.fenetre.after(
                self.tetris_vitesse(), self.avancer_tetris
            )

    def bloquer_tetris(self):
        for colonne, ligne in self.tetris_positions():
            if ligne >= 0:
                self.tetris_plateau[ligne][colonne] = self.tetris_piece

        lignes_completes = [
            ligne for ligne in self.tetris_plateau if all(ligne)
        ]
        self.tetris_plateau = [
            ligne for ligne in self.tetris_plateau if not all(ligne)
        ]
        self.tetris_plateau = (
            [[0] * 10 for _ in lignes_completes]
            + self.tetris_plateau
        )
        self.tetris_score += len(lignes_completes) ** 2 * 100
        self.tetris_nouvelle_piece()

    def touche_tetris(self, evenement):
        if not self.tetris_en_cours:
            return
        if evenement.keysym == "Left":
            self.deplacer_tetris(-1, 0)
        elif evenement.keysym == "Right":
            self.deplacer_tetris(1, 0)
        elif evenement.keysym == "Down":
            self.avancer_tetris()
        elif evenement.keysym in ("Up", "space"):
            self.tourner_tetris()

    def terminer_tetris(self):
        self.tetris_en_cours = False
        self.tetris_timer = None
        joueur = simpledialog.askstring(
            "Classement Tetris",
            "Ton nom :",
            parent=self.fenetre
        ) or "Anonyme"
        ajouter_top(
            f"Tetris {self.tetris_difficulte.capitalize()}",
            joueur,
            self.tetris_score
        )
        messagebox.showinfo(
            "Tetris",
            f"Défaite !\nScore : {self.tetris_score}",
            parent=self.fenetre
        )

    # =====================================================
    # AVENTURE PLATEFORME
    # =====================================================

    def creer_plateforme(self):
        self.frame_plateforme_choix = ttk.Frame(self.fenetre)
        self.frame_plateforme = ttk.Frame(self.fenetre)
        self.plateforme_timer = None
        self.plateforme_en_cours = False
        self.plateforme_niveau = 1

        ttk.Label(
            self.frame_plateforme_choix,
            text="🌟 AVENTURE PLATEFORME",
            style="Titre.TLabel"
        ).pack(pady=(80, 10))
        ttk.Label(
            self.frame_plateforme_choix,
            text="Choisis ton niveau",
            style="SousTitre.TLabel"
        ).pack(pady=5)
        choix_niveaux = ttk.Frame(self.frame_plateforme_choix)
        choix_niveaux.pack(pady=8)
        for niveau in range(1, 21):
            ttk.Button(
                choix_niveaux,
                text=f"Niveau {niveau}",
                command=lambda choix=niveau:
                self.preparer_plateforme(choix),
                style="Principal.TButton",
                width=16
            ).grid(
                row=(niveau - 1) // 4,
                column=(niveau - 1) % 4,
                padx=5,
                pady=5
            )
        self.bouton_menu(self.frame_plateforme_choix)

        ttk.Label(
            self.frame_plateforme,
            text="🌟 AVENTURE PLATEFORME",
            style="Titre.TLabel"
        ).pack(pady=(12, 3))
        self.plateforme_score_label = ttk.Label(
            self.frame_plateforme,
            text="Cristaux : 0",
            style="Stats.TLabel"
        )
        self.plateforme_score_label.pack()
        self.plateforme_niveau_label = ttk.Label(
            self.frame_plateforme,
            text="Niveau 1",
            style="SousTitre.TLabel"
        )
        self.plateforme_niveau_label.pack()
        self.plateforme_temps_label = ttk.Label(
            self.frame_plateforme,
            text="Chronomètre : 0 min 0 s",
            style="Stats.TLabel"
        )
        self.plateforme_temps_label.pack()
        self.plateforme_bonus_label = ttk.Label(
            self.frame_plateforme,
            text="",
            style="Stats.TLabel"
        )
        self.plateforme_bonus_label.pack()
        ttk.Label(
            self.frame_plateforme,
            text="Flèches : courir | Espace ou Haut : sauter",
            style="SousTitre.TLabel"
        ).pack(pady=3)

        self.plateforme_canvas = tk.Canvas(
            self.frame_plateforme,
            width=800,
            height=450,
            bg="#8bd5ff",
            highlightthickness=0
        )
        self.plateforme_canvas.pack(pady=8)

        ttk.Button(
            self.frame_plateforme,
            text="🔄 Recommencer",
            command=self.lancer_plateforme,
            style="Principal.TButton"
        ).pack(pady=3)
        self.bouton_menu(self.frame_plateforme)

    def afficher_plateforme(self):
        self.masquer_frames()
        self.frame_plateforme_choix.pack(fill="both", expand=True)

    def preparer_plateforme(self, niveau):
        self.plateforme_niveau = niveau
        self.plateforme_score = 0
        self.plateforme_temps_debut = time.perf_counter()
        self.frame_plateforme_choix.pack_forget()
        self.frame_plateforme.pack(fill="both", expand=True)
        self.lancer_plateforme()
        self.fenetre.focus_set()

    def lancer_plateforme(self, nouvelle_partie=True):
        if self.plateforme_timer is not None:
            self.fenetre.after_cancel(self.plateforme_timer)

        self.plateforme_en_cours = True
        self.plateforme_touches = set()
        if nouvelle_partie:
            self.plateforme_score = 0
            self.plateforme_temps_debut = time.perf_counter()
        self.plateforme_bonus_fin = 0.0
        self.plateforme_camera = 0
        self.plateforme_joueur = {
            "x": 70.0, "y": 320.0, "largeur": 28, "hauteur": 40,
            "vx": 0.0, "vy": 0.0, "sol": False
        }
        niveaux_definis = {
            1: {
                "arrivee": 1940,
                "plateformes": [
                    (0, 410, 520, 40), (600, 410, 420, 40),
                    (1100, 410, 430, 40), (1600, 410, 500, 40),
                    (230, 330, 150, 18), (700, 300, 145, 18),
                    (940, 350, 130, 18), (1230, 300, 160, 18),
                    (1450, 345, 130, 18), (1730, 290, 150, 18)
                ],
                "cristaux": [[280, 290], [735, 260], [970, 310], [1270, 260], [1490, 305], [1770, 250]],
                "bonus": [[430, 370], [1380, 360]],
                "ennemis": [{"x": 760.0, "y": 370.0, "vx": 1.2}, {"x": 1320.0, "y": 260.0, "vx": -1.0}]
            },
            2: {
                "arrivee": 1940,
                "plateformes": [
                    (0, 410, 350, 40), (470, 410, 270, 40),
                    (850, 410, 260, 40), (1240, 410, 230, 40),
                    (1600, 410, 500, 40), (170, 315, 120, 18),
                    (520, 270, 130, 18), (910, 320, 120, 18),
                    (1290, 275, 125, 18), (1510, 330, 120, 18),
                    (1770, 260, 125, 18)
                ],
                "cristaux": [[205, 275], [555, 230], [940, 280], [1325, 235], [1550, 290], [1810, 220]],
                "bonus": [[680, 370], [1430, 370], [1860, 220]],
                "ennemis": [{"x": 540.0, "y": 370.0, "vx": 1.4}, {"x": 1280.0, "y": 370.0, "vx": -1.2}, {"x": 1660.0, "y": 370.0, "vx": 1.5}]
            },
            3: {
                "arrivee": 1940,
                "plateformes": [
                    (0, 410, 250, 40), (390, 410, 180, 40),
                    (700, 410, 180, 40), (1020, 410, 170, 40),
                    (1340, 410, 160, 40), (1650, 410, 450, 40),
                    (85, 290, 100, 18), (450, 250, 100, 18),
                    (760, 300, 100, 18), (1080, 240, 100, 18),
                    (1390, 285, 100, 18), (1710, 220, 110, 18)
                ],
                "cristaux": [[115, 250], [480, 210], [790, 260], [1110, 200], [1420, 245], [1740, 180]],
                "bonus": [[500, 370], [1120, 370], [1780, 370]],
                "ennemis": [{"x": 430.0, "y": 370.0, "vx": 1.7}, {"x": 735.0, "y": 370.0, "vx": -1.6}, {"x": 1370.0, "y": 370.0, "vx": 1.8}]
            }
        }
        niveaux = niveaux_definis.get(self.plateforme_niveau)
        if niveaux is None:
            niveaux = self.generer_niveau_plateforme(self.plateforme_niveau)
        self.plateforme_arrivee = niveaux["arrivee"]
        self.plateforme_plateformes = niveaux["plateformes"]
        self.plateforme_cristaux = niveaux["cristaux"]
        self.plateforme_bonus = niveaux["bonus"]
        self.plateforme_ennemis = niveaux["ennemis"]
        self.plateforme_niveau_label.config(
            text=f"Niveau {self.plateforme_niveau}"
        )
        self.actualiser_plateforme()
        self.avancer_plateforme()

    def generer_niveau_plateforme(self, niveau):
        hasard = random.Random(niveau)
        arrivee = 1940 + (niveau - 3) * 25
        hauteur_plateformes = [290, 330, 260, 350]
        plateformes = [(0, 410, arrivee + 150, 40)]
        cristaux = []
        bonus = []
        ennemis = []

        for index in range(6):
            x = 180 + index * 285
            y = hauteur_plateformes[(index + niveau) % len(hauteur_plateformes)]
            largeur = 105 + hasard.randint(0, 45)
            plateformes.append((x, y, largeur, 18))
            cristaux.append([x + largeur // 2, y - 25])

            if index % 2 == niveau % 2:
                bonus.append([x + largeur - 25, y - 25])
            if index % 3 != 1:
                ennemis.append({
                    "x": float(x + 20),
                    "y": 382.0,
                    "vx": 1.0 + (niveau % 3) * 0.3
                })

        for index in range(3):
            bonus.append([700 + index * 560, 370])

        return {
            "arrivee": arrivee,
            "plateformes": plateformes,
            "cristaux": cristaux,
            "bonus": bonus,
            "ennemis": ennemis
        }

    def touche_plateforme(self, evenement):
        if not self.plateforme_en_cours:
            return
        touche = evenement.keysym
        self.plateforme_touches.add(touche)
        if touche in ("space", "Up") and self.plateforme_joueur["sol"]:
            self.plateforme_joueur["vy"] = -12
            self.plateforme_joueur["sol"] = False

    def touche_plateforme_relache(self, evenement):
        if self.plateforme_en_cours:
            self.plateforme_touches.discard(evenement.keysym)

    def plateforme_sur_plateforme(self, x, ancien_bas, nouveau_bas):
        for plateforme_x, plateforme_y, largeur, hauteur in self.plateforme_plateformes:
            dans_x = x + self.plateforme_joueur["largeur"] > plateforme_x and x < plateforme_x + largeur
            traverse = ancien_bas <= plateforme_y <= nouveau_bas
            if dans_x and traverse:
                return plateforme_y
        return None

    def avancer_plateforme(self):
        if not self.plateforme_en_cours:
            return

        joueur = self.plateforme_joueur
        vitesse = 8 if time.perf_counter() < self.plateforme_bonus_fin else 5
        if "Left" in self.plateforme_touches:
            joueur["vx"] = -vitesse
        elif "Right" in self.plateforme_touches:
            joueur["vx"] = vitesse
        else:
            joueur["vx"] *= 0.75

        limite = self.plateforme_arrivee + 100 - joueur["largeur"]
        joueur["x"] = max(0, min(limite, joueur["x"] + joueur["vx"]))
        ancien_bas = joueur["y"] + joueur["hauteur"]
        joueur["vy"] += 0.6
        joueur["y"] += joueur["vy"]
        nouveau_bas = joueur["y"] + joueur["hauteur"]
        joueur["sol"] = False

        plateforme_y = self.plateforme_sur_plateforme(
            joueur["x"], ancien_bas, nouveau_bas
        )
        if plateforme_y is not None:
            joueur["y"] = plateforme_y - joueur["hauteur"]
            joueur["vy"] = 0
            joueur["sol"] = True

        for ennemi in self.plateforme_ennemis:
            ennemi["x"] += ennemi["vx"]
            if ennemi["x"] < 0 or ennemi["x"] > 1980:
                ennemi["vx"] *= -1
            touche_ennemi = (
                joueur["x"] < ennemi["x"] + 28
                and joueur["x"] + joueur["largeur"] > ennemi["x"]
                and joueur["y"] < ennemi["y"] + 28
                and joueur["y"] + joueur["hauteur"] > ennemi["y"]
            )
            if touche_ennemi:
                self.terminer_plateforme("Un adversaire t'a touché !")
                return

        cristaux_restants = []
        for cristal_x, cristal_y in self.plateforme_cristaux:
            attrape = (
                joueur["x"] < cristal_x + 18
                and joueur["x"] + joueur["largeur"] > cristal_x
                and joueur["y"] < cristal_y + 18
                and joueur["y"] + joueur["hauteur"] > cristal_y
            )
            if attrape:
                self.plateforme_score += 1
            else:
                cristaux_restants.append([cristal_x, cristal_y])
        self.plateforme_cristaux = cristaux_restants

        bonus_restants = []
        for bonus_x, bonus_y in self.plateforme_bonus:
            attrape = (
                joueur["x"] < bonus_x + 20
                and joueur["x"] + joueur["largeur"] > bonus_x
                and joueur["y"] < bonus_y + 20
                and joueur["y"] + joueur["hauteur"] > bonus_y
            )
            if attrape:
                self.plateforme_bonus_fin = time.perf_counter() + 5
            else:
                bonus_restants.append([bonus_x, bonus_y])
        self.plateforme_bonus = bonus_restants

        if joueur["y"] > 470:
            self.terminer_plateforme("Tu es tombé !")
            return
        if joueur["x"] >= self.plateforme_arrivee:
            self.terminer_plateforme("Arrivée atteinte !")
            return

        self.actualiser_plateforme()
        self.plateforme_timer = self.fenetre.after(
            30, self.avancer_plateforme
        )

    def actualiser_plateforme(self):
        canvas = self.plateforme_canvas
        canvas.delete("all")
        joueur = self.plateforme_joueur
        self.plateforme_camera = max(
            0, min(self.plateforme_arrivee - 700, joueur["x"] - 300)
        )
        camera = self.plateforme_camera

        canvas.create_rectangle(0, 0, 800, 450, fill="#8bd5ff", outline="")
        canvas.create_oval(80, 55, 175, 105, fill="#fff3bf", outline="")
        canvas.create_oval(650, 85, 770, 135, fill="#fff3bf", outline="")

        for plateforme_x, plateforme_y, largeur, hauteur in self.plateforme_plateformes:
            x = plateforme_x - camera
            canvas.create_rectangle(
                x, plateforme_y, x + largeur, plateforme_y + hauteur,
                fill="#4b7f52", outline="#28513a", width=2
            )
            canvas.create_rectangle(
                x, plateforme_y, x + largeur, plateforme_y + 6,
                fill="#8dd35f", outline=""
            )

        for cristal_x, cristal_y in self.plateforme_cristaux:
            x = cristal_x - camera
            canvas.create_polygon(
                x + 9, cristal_y, x + 18, cristal_y + 9,
                x + 9, cristal_y + 18, x, cristal_y + 9,
                fill="#ffe066", outline="#d69e2e"
            )

        for bonus_x, bonus_y in self.plateforme_bonus:
            x = bonus_x - camera
            canvas.create_polygon(
                x + 10, bonus_y, x + 3, bonus_y + 12,
                x + 10, bonus_y + 9, x + 17, bonus_y + 9,
                x + 10, bonus_y + 20, x + 18, bonus_y + 7,
                x + 11, bonus_y + 10,
                fill="#f6e05e", outline="#b7791f"
            )

        for ennemi in self.plateforme_ennemis:
            x = ennemi["x"] - camera
            canvas.create_oval(
                x, ennemi["y"], x + 28, ennemi["y"] + 28,
                fill="#e85d75", outline="#9b2c4a", width=2
            )

        canvas.create_rectangle(
            self.plateforme_arrivee - camera, 300,
            self.plateforme_arrivee - camera + 7, 410,
            fill="#f6ad55", outline="#975a16", width=2
        )
        canvas.create_polygon(
            self.plateforme_arrivee - camera + 7, 300,
            self.plateforme_arrivee - camera + 65, 320,
            self.plateforme_arrivee - camera + 7, 340,
            fill="#805ad5", outline=""
        )

        x = joueur["x"] - camera
        canvas.create_rectangle(
            x, joueur["y"], x + joueur["largeur"],
            joueur["y"] + joueur["hauteur"],
            fill="#f56565", outline="#9b2c2c", width=2
        )
        canvas.create_oval(
            x + 5, joueur["y"] + 7, x + 10, joueur["y"] + 12,
            fill="#1a202c", outline=""
        )
        self.plateforme_score_label.config(
            text=f"Cristaux : {self.plateforme_score}"
        )
        temps = int(time.perf_counter() - self.plateforme_temps_debut)
        minutes, secondes = divmod(temps, 60)
        self.plateforme_temps_label.config(
            text=f"Chronomètre : {minutes} min {secondes} s"
        )
        if time.perf_counter() < self.plateforme_bonus_fin:
            restant = self.plateforme_bonus_fin - time.perf_counter()
            self.plateforme_bonus_label.config(
                text=f"⚡ Vitesse + : {restant:.1f} s"
            )
        else:
            self.plateforme_bonus_label.config(text="")

    def terminer_plateforme(self, message):
        self.plateforme_en_cours = False
        self.plateforme_timer = None

        if message == "Arrivée atteinte !" and self.plateforme_niveau < 20:
            score = self.plateforme_score
            niveau_termine = self.plateforme_niveau
            self.plateforme_niveau += 1
            messagebox.showinfo(
                "Niveau terminé",
                f"Bravo ! Le niveau {niveau_termine} est terminé.\n"
                f"Passage au niveau {self.plateforme_niveau}.",
                parent=self.fenetre
            )
            self.lancer_plateforme(nouvelle_partie=False)
            self.plateforme_score = score
            self.actualiser_plateforme()
            return

        joueur = simpledialog.askstring(
            "Classement Aventure plateforme",
            "Ton nom :",
            parent=self.fenetre
        ) or "Anonyme"
        temps = int(time.perf_counter() - self.plateforme_temps_debut)
        ajouter_top(
            "Aventure plateforme",
            joueur,
            self.plateforme_score,
            temps
        )
        minutes, secondes = divmod(temps, 60)
        messagebox.showinfo(
            "Aventure plateforme",
            f"{message}\nCristaux : {self.plateforme_score}\n"
            f"Temps : {minutes} min {secondes} s",
            parent=self.fenetre
        )

    # =====================================================
    # 2048
    # =====================================================

    def creer_2048(self):
        self.frame_2048 = ttk.Frame(self.fenetre)

        ttk.Label(
            self.frame_2048,
            text="🔢 2048",
            style="Titre.TLabel"
        ).pack(pady=15)

        self.jeu2048_score_label = ttk.Label(
            self.frame_2048,
            text="Score : 0",
            style="Stats.TLabel"
        )
        self.jeu2048_score_label.pack()

        self.jeu2048_info = ttk.Label(
            self.frame_2048,
            text="Utilise les flèches du clavier.",
            style="SousTitre.TLabel"
        )
        self.jeu2048_info.pack(pady=5)

        grille = ttk.Frame(
            self.frame_2048,
            style="Carte.TFrame",
            padding=10
        )
        grille.pack(pady=10)

        self.jeu2048_cases = []

        for ligne in range(4):
            ligne_cases = []

            for colonne in range(4):
                case = tk.Label(
                    grille,
                    text="",
                    width=5,
                    height=2,
                    font=("Arial", 22, "bold"),
                    relief="ridge",
                    borderwidth=2,
                    bg="#cdc1b4"
                )
                case.grid(
                    row=ligne,
                    column=colonne,
                    padx=4,
                    pady=4
                )
                ligne_cases.append(case)

            self.jeu2048_cases.append(ligne_cases)

        ttk.Button(
            self.frame_2048,
            text="🔄 Nouvelle partie",
            command=self.lancer_2048,
            style="Principal.TButton"
        ).pack(pady=8)

        self.bouton_menu(self.frame_2048)
        self.jeu2048_en_cours = False

    def afficher_2048(self):
        self.masquer_frames()
        self.frame_2048.pack(fill="both", expand=True)
        self.lancer_2048()

    def lancer_2048(self):
        self.jeu2048_grille = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.jeu2048_score = 0
        self.jeu2048_en_cours = True
        self.jeu2048_score_enregistre = False

        self.ajouter_case_2048()
        self.ajouter_case_2048()
        self.actualiser_2048()

    def ajouter_case_2048(self):
        cases_vides = [
            (ligne, colonne)
            for ligne in range(4)
            for colonne in range(4)
            if self.jeu2048_grille[ligne][colonne] == 0
        ]

        if cases_vides:
            ligne, colonne = random.choice(cases_vides)
            self.jeu2048_grille[ligne][colonne] = (
                4 if random.random() < 0.1 else 2
            )

    def touche_2048(self, evenement):
        if self.plateforme_en_cours:
            self.touche_plateforme(evenement)
            return

        if self.tetris_en_cours:
            self.touche_tetris(evenement)
            return

        if self.snake_en_cours:
            self.touche_snake(evenement)
            return

        if not self.jeu2048_en_cours:
            return

        directions = {
            "Left": "gauche",
            "Right": "droite",
            "Up": "haut",
            "Down": "bas"
        }

        if evenement.keysym in directions:
            self.deplacer_2048(directions[evenement.keysym])

    def fusionner_ligne_2048(self, ligne):
        valeurs = [valeur for valeur in ligne if valeur != 0]
        resultat = []
        index = 0

        while index < len(valeurs):
            if (
                index + 1 < len(valeurs)
                and valeurs[index] == valeurs[index + 1]
            ):
                valeur = valeurs[index] * 2
                resultat.append(valeur)
                self.jeu2048_score += valeur
                index += 2
            else:
                resultat.append(valeurs[index])
                index += 1

        resultat.extend([0] * (4 - len(resultat)))
        return resultat

    def transposer_2048(self, grille):
        return [
            [grille[ligne][colonne] for ligne in range(4)]
            for colonne in range(4)
        ]

    def deplacer_2048(self, direction):
        ancienne_grille = [
            ligne[:] for ligne in self.jeu2048_grille
        ]

        if direction == "gauche":
            self.jeu2048_grille = [
                self.fusionner_ligne_2048(ligne)
                for ligne in self.jeu2048_grille
            ]

        elif direction == "droite":
            self.jeu2048_grille = [
                list(reversed(
                    self.fusionner_ligne_2048(
                        list(reversed(ligne))
                    )
                ))
                for ligne in self.jeu2048_grille
            ]

        elif direction == "haut":
            grille = self.transposer_2048(self.jeu2048_grille)
            grille = [
                self.fusionner_ligne_2048(ligne)
                for ligne in grille
            ]
            self.jeu2048_grille = self.transposer_2048(grille)

        elif direction == "bas":
            grille = self.transposer_2048(self.jeu2048_grille)
            grille = [
                list(reversed(
                    self.fusionner_ligne_2048(
                        list(reversed(ligne))
                    )
                ))
                for ligne in grille
            ]
            self.jeu2048_grille = self.transposer_2048(grille)

        if self.jeu2048_grille == ancienne_grille:
            return

        self.ajouter_case_2048()
        self.actualiser_2048()

        if self.a_gagne_2048():
            self.jeu2048_en_cours = False
            self.enregistrer_score_2048()
            messagebox.showinfo(
                "2048",
                "Bravo, tu as atteint 2048 !"
            )
        elif not self.peut_jouer_2048():
            self.jeu2048_en_cours = False
            self.enregistrer_score_2048()
            messagebox.showinfo(
                "2048",
                "Partie terminée !"
            )

    def a_gagne_2048(self):
        return any(
            2048 in ligne
            for ligne in self.jeu2048_grille
        )

    def peut_jouer_2048(self):
        for ligne in range(4):
            for colonne in range(4):
                valeur = self.jeu2048_grille[ligne][colonne]

                if valeur == 0:
                    return True

                if (
                    colonne < 3
                    and valeur == self.jeu2048_grille[ligne][colonne + 1]
                ):
                    return True

                if (
                    ligne < 3
                    and valeur == self.jeu2048_grille[ligne + 1][colonne]
                ):
                    return True

        return False

    def actualiser_2048(self):
        couleurs = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e"
        }

        for ligne in range(4):
            for colonne in range(4):
                valeur = self.jeu2048_grille[ligne][colonne]
                case = self.jeu2048_cases[ligne][colonne]

                case.config(
                    text="" if valeur == 0 else str(valeur),
                    bg=couleurs.get(valeur, "#3c3a32"),
                    fg="#776e65" if valeur <= 4 else "white"
                )

        self.jeu2048_score_label.config(
            text=f"Score : {self.jeu2048_score}"
        )

    def enregistrer_score_2048(self):
        if self.jeu2048_score_enregistre:
            return

        self.jeu2048_score_enregistre = True
        joueur = simpledialog.askstring(
            "Classement 2048",
            "Ton nom :",
            parent=self.fenetre
        ) or "Anonyme"

        ajouter_top(
            "2048",
            joueur,
            self.jeu2048_score
        )

    # =====================================================
    # TOPS
    # =====================================================

    def afficher_tops(self):
        tops = charger_tops()

        fenetre = tk.Toplevel(self.fenetre)
        fenetre.title("🏆 Mes classements")
        fenetre.geometry("700x650")
        fenetre.resizable(False, False)
        fenetre.configure(bg="#111827")

        choix = {
            "🎯 Top du Bingo": "Bingo",
            "✊ Top Pierre-Feuille-Ciseau-Lézard-Spock":
                "Pierre-Feuille-Ciseau-Lézard-Spock",
            "⭕ Top du Morpion": "Morpion",
            "🔴 Top du Puissance 4": "Puissance 4",
            "⚓ Top de la Bataille navale": "Bataille navale",
            "♟ Top des Échecs": "Échecs",
            "🔤 Top du Pendu": "Pendu",
            "🔢 Top du 2048": "2048",
            "🐍 Top du Snake": "Snake",
            "🧱 Top du Tetris - Facile": "Tetris Facile",
            "🧱 Top du Tetris - Moyen": "Tetris Moyen",
            "🧱 Top du Tetris - Difficile": "Tetris Difficile",
            "🌟 Top Aventure plateforme": "Aventure plateforme",
            "🧠 Quiz - Tables de multiplication":
                "Quiz - Tables de multiplication",
            "🧠 Quiz - Culture générale":
                "Quiz - Culture générale",
            "🧠 Quiz - Sciences": "Quiz - Sciences",
            "🧠 Quiz - Géographie": "Quiz - Géographie"
        }

        ttk.Label(
            fenetre,
            text="🏆 MES CLASSEMENTS",
            style="Titre.TLabel"
        ).pack(pady=15)

        ttk.Label(
            fenetre,
            text="Choisis un jeu pour consulter les meilleurs scores",
            style="SousTitre.TLabel"
        ).pack(pady=(0, 10))

        selection = tk.StringVar(value=list(choix)[0])

        menu = ttk.Combobox(
            fenetre,
            textvariable=selection,
            values=list(choix),
            state="readonly",
            width=48
        )
        menu.pack(pady=5)

        zone = tk.Text(
            fenetre,
            font=("DejaVu Sans", 12),
            wrap="word",
            bg="#f8fafc",
            fg="#1e293b",
            padx=18,
            pady=14,
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        zone.pack(
            padx=25,
            pady=15,
            fill="both",
            expand=True
        )

        def afficher_classement():
            nom = selection.get()
            type_top = choix[nom]

            if type_top == "Bingo":
                classement = []

                for jeu, resultats in tops.items():
                    if jeu.startswith("Bingo"):
                        classement.extend(resultats)

                classement.sort(
                    key=lambda resultat: (
                        resultat.get("score", 999999),
                        resultat.get("temps", 999999)
                    )
                )
            else:
                if type_top == "Aventure plateforme":
                    classement = sorted(
                        tops.get(type_top, []),
                        key=lambda resultat: (
                            resultat.get("temps", 999999),
                            -resultat.get("score", 0)
                        )
                    )
                else:
                    classement = sorted(
                        tops.get(type_top, []),
                        key=lambda resultat: -resultat.get("score", 0)
                    )

            zone.config(state="normal")
            zone.delete("1.0", tk.END)
            zone.insert(tk.END, f"{nom}\n\n")

            if not classement:
                zone.insert(
                    tk.END,
                    "Aucun résultat enregistré."
                )
            else:
                for rang, resultat in enumerate(classement[:10], 1):
                    joueur = resultat.get("joueur", "Anonyme")
                    score = resultat.get("score", 0)

                    if type_top == "Bingo":
                        temps = resultat.get("temps")

                        if temps is not None:
                            texte = (
                                f"{rang}. {joueur} - "
                                f"{score} essai(s) - "
                                f"{formater_temps(temps)}\n"
                            )
                        else:
                            texte = (
                                f"{rang}. {joueur} - "
                                f"{score} essai(s)\n"
                            )
                    else:
                        temps = resultat.get("temps")
                        if type_top == "Aventure plateforme" and temps is not None:
                            texte = (
                                f"{rang}. {joueur} - "
                                f"{score} cristal(aux) - "
                                f"{formater_temps(temps)}\n"
                            )
                        else:
                            texte = (
                                f"{rang}. {joueur} - "
                                f"{score} point(s)\n"
                            )

                    zone.insert(tk.END, texte)

            zone.config(state="disabled")

        menu.bind(
            "<<ComboboxSelected>>",
            lambda event: afficher_classement()
        )

        afficher_classement()

    def effacer_tops(self):
        tops = charger_tops()
        fenetre = tk.Toplevel(self.fenetre)
        fenetre.title("🏆 Gestion des classements")
        fenetre.geometry("720x620")
        fenetre.resizable(False, False)
        fenetre.configure(bg="#111827")

        ttk.Label(
            fenetre,
            text="🏆 GESTION DES CLASSEMENTS",
            style="Titre.TLabel"
        ).pack(pady=(24, 5))

        ttk.Label(
            fenetre,
            text="Sélectionne un ou plusieurs classements à supprimer",
            style="SousTitre.TLabel"
        ).pack(pady=(0, 16))

        carte = ttk.Frame(
            fenetre,
            style="Carte.TFrame",
            padding=12
        )
        carte.pack(padx=28, fill="both", expand=True)

        ttk.Label(
            carte,
            text="Classements enregistrés",
            style="CarteTitre.TLabel"
        ).pack(anchor="w", pady=(0, 3))

        ttk.Label(
            carte,
            text="Maintiens Ctrl pour sélectionner plusieurs lignes.",
            style="Info.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        zone_liste = ttk.Frame(carte)
        zone_liste.pack(fill="both", expand=True)

        liste = tk.Listbox(
            zone_liste,
            selectmode=tk.MULTIPLE,
            width=64,
            height=17,
            font=("DejaVu Sans", 11),
            activestyle="none",
            bg="#f8fafc",
            fg="#1e293b",
            selectbackground="#6366f1",
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#c7d2fe"
        )
        liste.pack(side="left", fill="both", expand=True)

        barre = ttk.Scrollbar(
            zone_liste,
            orient="vertical",
            command=liste.yview
        )
        barre.pack(side="right", fill="y")
        liste.config(yscrollcommand=barre.set)

        noms_tops = list(tops)
        for nom_top in noms_tops:
            nombre_resultats = len(tops[nom_top])
            liste.insert(
                tk.END,
                f"{nom_top} ({nombre_resultats} résultat(s))"
            )

        if not noms_tops:
            liste.insert(tk.END, "Aucun top enregistré.")
            liste.config(state="disabled")

        boutons = ttk.Frame(fenetre)
        boutons.pack(pady=18)

        def supprimer_selection():
            selections = liste.curselection()
            if not selections:
                messagebox.showwarning(
                    "Classements",
                    "Sélectionne au moins un top.",
                    parent=fenetre
                )
                return

            noms_selectionnes = [noms_tops[index] for index in selections]
            confirmation = messagebox.askyesno(
                "Confirmation",
                "Supprimer les tops sélectionnés ?",
                parent=fenetre
            )
            if not confirmation:
                return

            tops_actuels = charger_tops()
            for nom_top in noms_selectionnes:
                tops_actuels.pop(nom_top, None)

            if tops_actuels:
                sauvegarder_tops(tops_actuels)
            elif FICHIER_TOP.exists():
                FICHIER_TOP.unlink()

            messagebox.showinfo(
                "Classements",
                "Les tops sélectionnés ont été supprimés.",
                parent=fenetre
            )
            fenetre.destroy()

        def supprimer_tout():
            if not tops:
                fenetre.destroy()
                return

            if not messagebox.askyesno(
                "Confirmation",
                "Supprimer tous les tops ?",
                parent=fenetre
            ):
                return

            if FICHIER_TOP.exists():
                FICHIER_TOP.unlink()

            messagebox.showinfo(
                "Classements",
                "Tous les tops ont été supprimés.",
                parent=fenetre
            )
            fenetre.destroy()

        ttk.Button(
            boutons,
            text="✕ Supprimer la sélection",
            command=supprimer_selection,
            style="Danger.TButton"
        ).pack(side="left", padx=5)
        ttk.Button(
            boutons,
            text="🗑 Tout supprimer",
            command=supprimer_tout,
            style="Danger.TButton"
        ).pack(side="left", padx=5)

    def ouvrir_parametres(self):
        fenetre = tk.Toplevel(self.fenetre)
        fenetre.title("⚙ Paramètres")
        fenetre.geometry("620x650")
        fenetre.resizable(False, False)
        fenetre.configure(bg="#111827")

        ttk.Label(
            fenetre,
            text="⚙ PARAMÈTRES",
            style="Titre.TLabel"
        ).pack(pady=(20, 5))
        ttk.Label(
            fenetre,
            text="Personnalise ton arcade",
            style="SousTitre.TLabel"
        ).pack(pady=(0, 15))

        configuration = charger_configuration()
        couleurs = {
            "Bleu nuit": "#111827",
            "Vert forêt": "#12352f",
            "Bordeaux": "#3b1725",
            "Gris ardoise": "#263238",
            "Brun chaleureux": "#3b2a20"
        }
        couleur_actuelle = configuration.get(
            "couleur_menu",
            COULEUR_MENU_DEFAUT
        )
        nom_couleur = next(
            (
                nom for nom, valeur in couleurs.items()
                if valeur == couleur_actuelle
            ),
            "Bleu nuit"
        )

        carte_couleur = ttk.Frame(
            fenetre,
            style="Carte.TFrame",
            padding=14
        )
        carte_couleur.pack(padx=30, fill="x")
        ttk.Label(
            carte_couleur,
            text="Couleur du menu",
            style="CarteTitre.TLabel"
        ).pack(anchor="w")
        choix_couleur = ttk.Combobox(
            carte_couleur,
            values=list(couleurs),
            state="readonly",
            width=35
        )
        choix_couleur.set(nom_couleur)
        choix_couleur.pack(anchor="w", pady=(8, 0))

        carte_ordre = ttk.Frame(
            fenetre,
            style="Carte.TFrame",
            padding=14
        )
        carte_ordre.pack(padx=30, pady=12, fill="both", expand=True)
        ttk.Label(
            carte_ordre,
            text="Ordre des jeux",
            style="CarteTitre.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            carte_ordre,
            text="Sélectionne un jeu puis utilise Monter ou Descendre.",
            style="Info.TLabel"
        ).pack(anchor="w", pady=(3, 8))

        definitions = {
            identifiant: texte
            for identifiant, texte, _ in self.jeux_menu
        }
        ordre = configuration.get("ordre_jeux", [])
        ordre = [identifiant for identifiant in ordre if identifiant in definitions]
        ordre.extend(
            identifiant for identifiant, _, _ in self.jeux_menu
            if identifiant not in ordre
        )

        zone_ordre = ttk.Frame(carte_ordre)
        zone_ordre.pack(fill="both", expand=True)
        liste = tk.Listbox(
            zone_ordre,
            width=45,
            height=12,
            font=("DejaVu Sans", 11),
            selectmode=tk.SINGLE,
            activestyle="none",
            bg="#f8fafc",
            fg="#1e293b",
            selectbackground="#6366f1",
            selectforeground="#ffffff",
            relief="flat"
        )
        liste.pack(side="left", fill="both", expand=True)
        for identifiant in ordre:
            liste.insert(tk.END, definitions[identifiant])

        boutons_ordre = ttk.Frame(zone_ordre)
        boutons_ordre.pack(side="right", padx=(10, 0), anchor="n")

        def deplacer(delta):
            selection = liste.curselection()
            if not selection:
                return
            index = selection[0]
            nouvel_index = index + delta
            if not 0 <= nouvel_index < liste.size():
                return
            valeur = liste.get(index)
            liste.delete(index)
            liste.insert(nouvel_index, valeur)
            liste.selection_set(nouvel_index)
            liste.activate(nouvel_index)

        ttk.Button(
            boutons_ordre,
            text="▲ Monter",
            command=lambda: deplacer(-1),
            style="Secondaire.TButton"
        ).pack(pady=3)
        ttk.Button(
            boutons_ordre,
            text="▼ Descendre",
            command=lambda: deplacer(1),
            style="Secondaire.TButton"
        ).pack(pady=3)

        def enregistrer():
            textes_choisis = list(liste.get(0, tk.END))
            identifiants = [
                identifiant for texte in textes_choisis
                for identifiant, nom in definitions.items()
                if nom == texte
            ]
            configuration["couleur_menu"] = couleurs[choix_couleur.get()]
            configuration["ordre_jeux"] = identifiants
            sauvegarder_configuration(configuration)
            self.appliquer_couleur_menu(configuration["couleur_menu"])
            self.construire_menu_jeux()
            fenetre.destroy()

        boutons = ttk.Frame(fenetre)
        boutons.pack(pady=15)
        ttk.Button(
            boutons,
            text="🔑 Modifier le mot de passe",
            command=self.modifier_mot_de_passe,
            style="Secondaire.TButton"
        ).pack(side="left", padx=5)
        ttk.Button(
            boutons,
            text="✓ Enregistrer",
            command=enregistrer,
            style="Principal.TButton"
        ).pack(side="left", padx=5)

    def modifier_mot_de_passe(self):
        ancien = simpledialog.askstring(
            "Paramètres",
            "Mot de passe actuel :",
            show="*",
            parent=self.fenetre
        )
        if ancien is None:
            return

        if ancien != charger_mot_de_passe():
            messagebox.showerror(
                "Paramètres",
                "Le mot de passe actuel est incorrect.",
                parent=self.fenetre
            )
            return

        nouveau = simpledialog.askstring(
            "Paramètres",
            "Nouveau mot de passe :",
            show="*",
            parent=self.fenetre
        )
        if nouveau is None:
            return
        if not nouveau.strip():
            messagebox.showwarning(
                "Paramètres",
                "Le nouveau mot de passe ne peut pas être vide.",
                parent=self.fenetre
            )
            return

        confirmation = simpledialog.askstring(
            "Paramètres",
            "Confirme le nouveau mot de passe :",
            show="*",
            parent=self.fenetre
        )
        if confirmation != nouveau:
            messagebox.showerror(
                "Paramètres",
                "Les deux mots de passe sont différents.",
                parent=self.fenetre
            )
            return

        sauvegarder_mot_de_passe(nouveau)
        messagebox.showinfo(
            "Paramètres",
            "Le mot de passe a été modifié.",
            parent=self.fenetre
        )

    def quitter(self, event=None):
        self.arreter_bingo()
        self.fenetre.destroy()


def demander_connexion(fenetre):
    while True:
        nom_utilisateur = simpledialog.askstring(
            "Connexion",
            "Nom d'utilisateur :",
            parent=fenetre
        )
        if nom_utilisateur is None:
            return False

        mot_de_passe = simpledialog.askstring(
            "Connexion",
            "Mot de passe :",
            show="*",
            parent=fenetre
        )
        if mot_de_passe is None:
            return False

        if (
            nom_utilisateur == "admin"
            and mot_de_passe == charger_mot_de_passe()
        ):
            return True

        messagebox.showerror(
            "Connexion refusée",
            "Nom d'utilisateur ou mot de passe incorrect.",
            parent=fenetre
        )


fenetre = tk.Tk()
fenetre.withdraw()

if demander_connexion(fenetre):
    fenetre.deiconify()
    application = JeuxApp(fenetre)
    fenetre.mainloop()
else:
    fenetre.destroy()
