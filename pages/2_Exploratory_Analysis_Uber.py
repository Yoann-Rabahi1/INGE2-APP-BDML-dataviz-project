from utils.imports import *
from ui.header import analysis_header
from ui.sidebar import uber_sidebar
from ui.pagination import df_all

df = pd.read_csv("data/df_output.csv")


df_map = df[["dropoff_latitude", "dropoff_longitude", "passenger_count", "VendorID"]].copy()
df_map = df_map.rename(columns={"dropoff_latitude": "latitude", "dropoff_longitude": "longitude"})

def get_color(vendor_id):
    
    return "#FF4B4B" if vendor_id == 1 else "#1C83E1"

df_map["color_hex"] = df_map["VendorID"].apply(get_color)

df_map["VendorID"] = df_map["VendorID"].astype(str)



mask_columns = df.filter(regex=r"longitude|latitude|tpep|trip", axis=1).columns.tolist()

mask_columns = mask_columns + ["distance_km", "vitesse_en_kmh"]

df_keep = df.drop(columns=mask_columns, errors="ignore")

analysis_header()

# uber_sidebar()

df_all(df_keep)

st.markdown(
    """
    <div style="
        background-color: #f0fdf4;
        border-left: 4px solid #05a357;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    ">
        <h2 style="
            color: #004d25; 
            font-weight: 600; 
            margin: 0;
        ">
            <strong>I) Statistics Visualizations</strong>
        </h2>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="color: #334155; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;">
        1.1) Distribution des distances de trajet (km)
    </h3>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    density_distance = px.histogram(
        df, 
        x="distance_km", 
        color="VendorID",
        range_x=[0, 20],
        # Dictionnaire pour associer chaque VendorID à une couleur explicite
        color_discrete_map={
            1: "#FF4B4B",  
            2: "#1C83E1"   
        }
    )
    
    st.plotly_chart(density_distance, use_container_width=True)


st.markdown(
    """
    <h3 style="color: #334155; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">
        1.2) Répartition des courses par heure de la journée
    </h3>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Tracer le KDE avec Seaborn
    sns.kdeplot(data=df, x="hour", fill=True, hue="VendorID", ax=ax, palette={1 : "red", 2 : "blue"})
    
    ax.set_xlim(0, 24)
    ax.set_xlabel("Heure de la journée")
    ax.set_ylabel("Densité")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Affichage dans Streamlit
    st.pyplot(fig)
    plt.close(fig) # Libère l


st.markdown(
    """
    <div style="
        background-color: #f0fdf4;
        border-left: 4px solid #05a357;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    ">
        <h2 style="
            color: #004d25; 
            font-weight: 600; 
            margin: 0;
        ">
            <strong>II) Dynamic Visualizations + KPI</strong>
        </h2>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="color: #334155; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">
        2.1) Interactive scatter/map of pickup locations.
    </h3>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):

    st.map(
        df_map, 
        latitude="latitude", 
        longitude="longitude", 
        color="color_hex",       
        size="passenger_count"
    )


st.markdown(
    """
    <h3 style="color: #334155; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">
        2.2) Interactive scatter/map of pickup locations.
    </h3>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):

    pass