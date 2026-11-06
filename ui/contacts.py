from utils.imports import *

def show_contact() -> None:


    with st.container(border=True):
        col4, col5 = st.columns(2)

        with col4:
            st.markdown("**GitHub :** \n <br><a href='https://github.com/Yoann-Rabahi1?tab=repositories' target='_blank'>Voir GitHub ici</a>", unsafe_allow_html=True)
        with col5:
            st.markdown("**LinkedIn :** \n <br><a href='https://www.linkedin.com/in/yoann-rabahi-95a26a289/' target='_blank'>Voir LinkedIn ici</a>", unsafe_allow_html=True)