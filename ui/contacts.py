from utils.imports import *

def show_contact() -> None:

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col1.markdown("📧 **Email :**  \nrabahiyoann@gmail.com")
        col2.markdown("📞 **Téléphone :**  \n07 63 93 10 97")
        col3.markdown("📍 **Localisation :**  \nParis, France")