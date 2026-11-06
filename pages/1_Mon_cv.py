from utils.imports import st
from onglet.CV.cv import show_cv
from onglet.CV.courses import show_courses


tab1, tab2 = st.tabs(["Mon CV", "Mes cours"])


with tab1 : 

    show_cv()


with tab2:

    show_courses()
    