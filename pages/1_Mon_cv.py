from utils.imports import *
from utils.constants import *

from ui.components import *
from ui.header import show_header
from ui.contacts import show_contact


st.set_page_config(
    page_title="Yoann Rabahi - CV",
    layout="centered"
)

css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
    .badge {
        background-color: #f0f2f6;
        color: #1f2937;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
        display: inline-block;
    }
    .date-text {
        text-align: right;
        color: #6b7280;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


show_header()

show_contact()

st.write("")

show_experiences()