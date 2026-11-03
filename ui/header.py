from utils.imports import *

def cv_header() -> None:

    st.markdown("<h1 style='text-align: center;'>Yoann Rabahi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'> Data Science & Machine Learning Student / Engineer</p>", unsafe_allow_html=True)


def analysis_header() -> None:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #05a357 0%, #004d25 100%);
            padding: 1.25rem 1rem;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        ">
            <h1 style="
                color: #FFFFFF;
                text-align: center;
                font-weight: 700;
                font-family: 'Inter', sans-serif;
                margin: 0;
                letter-spacing: -0.3px;
            ">
                Uber Dataset Analysis
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )