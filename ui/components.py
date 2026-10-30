from utils.imports import *
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