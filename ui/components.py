from utils.imports import st
from utils.constants import *

def afficher_experiences(liste_exp: list):
    for exp in liste_exp:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<h3 style='font-weight:bolder;'>{exp['poste']}</h3>", unsafe_allow_html=True)
                st.markdown(f"**{exp['entreprise']}** — *{exp['ville']}*")
            with col2:
                st.markdown(f"<p class='date-text'>{exp['date_de_debut']} — {exp['date_de_fin']}</p>", unsafe_allow_html=True)
            
            if exp.get("competences"):
                badges_html = "".join([f"<span class='badge'>{comp}</span>" for comp in exp["competences"]])
                st.markdown(badges_html, unsafe_allow_html=True)
            
            if exp.get("missions"):
                for mission in exp["missions"]:
                    st.markdown(f"- {mission}")
                    
            st.divider()


def afficher_education(liste_edu: list):
    for edu in liste_edu:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<h3 style='font-weight:bolder;'>{edu['diplome']}</h3>", unsafe_allow_html=True)
                st.markdown(f"**{edu['ecole']}** ({edu['ville']}) — *{edu['specialite']}*")
            with col2:
                st.markdown(f"<p class='date-text'>{edu['moyenne']}</p>", unsafe_allow_html=True)
            
            st.markdown(
                f"<span class='badge'>Niveau: {edu['niveau']}</span>", 
                unsafe_allow_html=True
            )
            
            if edu.get("matieres"):
                st.markdown("**Matières clés :** " + " • ".join(edu["matieres"]))
            
            st.divider()


def afficher_echanges(liste_echanges: list):
    for ech in liste_echanges:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<h3 style='font-weight:bolder;'>{ech['nom_projet']}</h3>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p class='date-text'>🌍 {ech['pays']}</p>", unsafe_allow_html=True)
            
            if ech.get("competences"):
                badges_html = "".join([f"<span class='badge'>{comp}</span>" for comp in ech["competences"]])
                st.markdown(badges_html, unsafe_allow_html=True)
                
            if ech.get("missions"):
                for mission in ech["missions"]:
                    st.markdown(f"- {mission}")
                    
            st.divider()


def afficher_langues_competences(liste_data: list):
    for data in liste_data:

        with st.container():

            st.markdown("#### 🗣️ Langues")
            cols = st.columns(2)
            langues_items = list(data["Langues"].items())
            mid = (len(langues_items) + 1) // 2
            
            with cols[0]:
                for lang, niveau in langues_items[:mid]:
                    st.markdown(f"- **{lang}** : {niveau}")
            with cols[1]:
                for lang, niveau in langues_items[mid:]:
                    st.markdown(f"- **{lang}** : {niveau}")
            
            st.write("")
            st.markdown("#### Compétences Transversales")
            badges_comp = "".join([f"<span class='badge'>{comp}</span>" for comp in data["Competences"]])
            st.markdown(badges_comp, unsafe_allow_html=True)
            
            st.write("")
            st.markdown("#### Compétences Techniques")
            badges_tech = "".join([f"<span class='badge'>{tech}</span>" for tech in data["Technique"]])
            st.markdown(badges_tech, unsafe_allow_html=True)


def show_experiences():

    with st.container(border=True):
        st.header(":blue[Expériences Professionnelles]")
        afficher_experiences(EXPERIENCES)

        st.header(":blue[Échange Universitaire]")
        afficher_echanges(ECHANGE_UNIVERSITAIRE)

        st.header(":blue[Formation]")
        afficher_education(EDUCATION)

        st.header(":blue[Langues & Compétences]")
        afficher_langues_competences(LANGUES_ET_COMPETENCES)



def afficher_carte_cours(cours):
    """Affiche un cours unique sous forme de carte stylisée"""
    with st.container():
        st.markdown(
            f"""
            <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; background-color: white; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #1e293b;">{cours['nom_cours']}</h4>
                <p style="color: #64748b; font-size: 0.9em; margin-bottom: 8px;"><b>{cours['annee_scolaire']}</b></p>
            """, 
            unsafe_allow_html=True
        )
        
        if cours.get("liste_chapitre"):
            badges = "".join([f"<span class='badge'>{chap}</span>" for chap in cours["liste_chapitre"]])
            st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: gray; font-style: italic; font-size: 0.85em;'>Aucun chapitre renseigné</p>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

def afficher_cours_par_matrice(liste_cours):
    st.markdown("<h1 style='text-align: center;'>Mes Cours</h1>", unsafe_allow_html=True)
    
    # Regroupement par année / semestre
    semestres = [5, 6, 7]
    
    for sem in semestres:
        cours_sem = [c for c in liste_cours if c["semestre"] == sem]
        if not cours_sem:
            continue
            
        annee_label = "1ère Année" if sem in [5, 6] else "2ème Année"
        st.markdown(f"## {annee_label} — Semestre {sem} <span style='font-size:0.6em; color:gray;'>({len(cours_sem)} cours)</span>", unsafe_allow_html=True)
        
        # Affichage en matrice de 2 colonnes
        for i in range(0, len(cours_sem), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                afficher_carte_cours(cours_sem[i])
                
            with col2:
                if i + 1 < len(cours_sem):
                    afficher_carte_cours(cours_sem[i + 1])
                    
        st.markdown("<br>", unsafe_allow_html=True)

# CSS pour les badges et l'alignement
st.markdown("""
    <style>
    .badge {
        display: inline-block;
        background-color: #f1f5f9;
        color: #334155;
        padding: 3px 8px;
        margin: 2px;
        border-radius: 4px;
        font-size: 0.75em;
        font-weight: 500;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)