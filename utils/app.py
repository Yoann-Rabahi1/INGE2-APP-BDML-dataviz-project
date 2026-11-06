from pathlib import Path

from utils.imports import *

GREEN_DARK = "#004d25"
GREEN = "#05a357"
GREEN_BG = "#f0fdf4"

# Racine du projet (le dossier qui contient backend.py et pages/) : utils/app.py -> utils -> racine
ROOT = Path(__file__).resolve().parent.parent

# (titre, icône, chemin relatif à la racine)
PAGE_FILES = [
    ("CV", "📄", "pages/1_Mon_cv.py"),
    ("Analysis", "📊", "pages/2_Exploratory_Analysis_Uber.py"),
]


def apply_sidebar() -> None:
    """Style + contenu de la sidebar. Exécuté à chaque rerun, donc identique sur toutes les pages."""
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                background-color: {GREEN_BG};
                border-right: 1px solid #d1fae5;
            }}
            /* Liens de navigation (anciens et nouveaux sélecteurs Streamlit) */
            [data-testid="stSidebarNav"] a,
            [data-testid="stSidebarNavLink"] {{
                border-radius: 6px;
                margin: 2px 0;
            }}
            [data-testid="stSidebarNav"] a:hover,
            [data-testid="stSidebarNavLink"]:hover {{
                background-color: #dcfce7;
            }}
            /* Page active */
            [data-testid="stSidebarNav"] a[aria-current="page"],
            [data-testid="stSidebarNavLink"][aria-current="page"] {{
                background-color: {GREEN};
                font-weight: 600;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] *,
            [data-testid="stSidebarNavLink"][aria-current="page"] * {{
                color: white !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
                <div style="font-size: 2.2rem;">🚕</div>
                <div style="color: {GREEN_DARK}; font-weight: 700; font-size: 1.1rem;">
                    NYC Taxi Explorer
                </div>
                <div style="color: #6b7280; font-size: 0.8rem;">
                    Explorer · Comprendre · Raconter
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        st.caption("Projet de data visualisation · Streamlit")


def home() -> None:
    """Page d'accueil : à quoi sert l'interface et comment elle est organisée."""

    # --- En-tête ---
    st.markdown(
        f"""
        <div style="
            background-color: {GREEN_BG};
            border-left: 5px solid {GREEN};
            padding: 1.2rem 1.5rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
        ">
            <h1 style="color: {GREEN_DARK}; font-weight: 700; margin: 0;">
                🚕 NYC Taxi Explorer
            </h1>
            <p style="color: #374151; margin: 0.4rem 0 0 0; font-size: 1.05rem;">
                Une interface interactive pour explorer, comprendre et raconter la demande de taxis à New York.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- À quoi sert l'interface ---
    st.header("À quoi sert cette interface ?")
    st.markdown(
        """
        Cette application permet d'analyser un jeu de données de **courses de taxis new-yorkais** :
        distances, durées, horaires, localisations, montants, opérateurs.
        Elle accompagne la démarche d'analyse **de bout en bout**, depuis les données brutes jusqu'aux
        enseignements métier, sans écrire de code.
        """
    )

    # --- Parcours en 3 étapes ---
    st.header("Comment est-elle organisée ?")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("1. 🧹 Traitement")
            st.markdown(
                "Chargement et nettoyage des données : contrôle de la qualité, "
                "valeurs aberrantes, création de variables (heure, durée du trajet)."
            )

    with col2:
        with st.container(border=True):
            st.subheader("2. 📊 Exploration")
            st.markdown(
                "Visualisations statistiques et dynamiques : distribution des distances, "
                "rythme horaire, carte de chaleur, relation durée / distance."
            )

    with col3:
        with st.container(border=True):
            st.subheader("3. 📖 Storytelling")
            st.markdown(
                "Synthèse des résultats sous forme d'indicateurs clés et de récit "
                "pour comprendre les usages du taxi dans le temps et l'espace."
            )

    # --- Ce qu'on peut y trouver ---
    st.header("Ce que vous allez y découvrir")
    st.markdown(
        """
        - **Quand** les New-Yorkais prennent-ils le taxi ? (pics de pendulaires, creux nocturnes)
        - **Où** la demande se concentre-t-elle ? (Manhattan, aéroports)
        - **Quelle distance** et **quelle durée** pour une course typique ?
        - **Quel impact** de la congestion sur le temps de trajet ?
        - Les **deux opérateurs** (VendorID 1 et 2) se comportent-ils de la même façon ?
        """
    )

    # --- Mode d'emploi ---
    st.header("Mode d'emploi")
    with st.container(border=True):
        st.markdown(
            """
            1. Utilisez le **menu latéral** pour naviguer entre les sections.
            2. Les graphiques sont **interactifs** : survolez pour voir les détails, zoomez, filtrez via la légende.
            3. La carte se **déplace et se zoome** à la souris.
            4. Chaque figure est suivie d'une courte **lecture** qui en résume l'enseignement principal.
            """
        )

    # --- Pied de page ---
    st.divider()
    st.caption(
        "Projet de data visualisation · Données : courses de taxis de New York (NYC TLC) · "
        "Réalisé avec Streamlit, Plotly et PyDeck."
    )


def main() -> None:
    """Lance toute l'application : configuration, navigation, sidebar, page courante."""

    # Doit être le premier appel Streamlit
    st.set_page_config(
        page_title="NYC Taxi Explorer",
        page_icon="🚕",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    pages = [st.Page(home, title="Accueil", icon="🏠", url_path="accueil", default=True)]
    missing = []

    for title, icon, relative_path in PAGE_FILES:
        full_path = ROOT / relative_path
        if full_path.exists():
            # Chemin absolu : accepté par st.Page, et indépendant du dossier de ce fichier
            pages.append(st.Page(full_path, title=title, icon=icon))
        else:
            missing.append(str(full_path))

    if missing:
        st.error("Fichier(s) de page introuvable(s) :\n\n" + "\n".join(f"- {m}" for m in missing))

    navigation = st.navigation(pages, position="sidebar")

    # Sidebar appliquée sur TOUTES les pages, juste avant l'exécution de la page choisie.
    apply_sidebar()

    navigation.run()