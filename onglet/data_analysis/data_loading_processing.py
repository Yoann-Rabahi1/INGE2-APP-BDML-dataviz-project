from utils.imports import pd, st, np, px
from ui.pagination import df_all
from ui.style import CUSTOM_CSS

def data_processing(df: pd.DataFrame):

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    # --- Titre Principal ---
    st.title("Data Loading & Transformation")
    st.divider()

    # --- 1) Chargement des données ---
    st.header("1) Chargement des données")
    df_all(df)

    # --- 2) Dimensions du Dataset ---
    st.header("2) Dimensions du Dataset")

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Nombre de lignes",
                value=f"{df.shape[0]:,}".replace(",", " ")
            )
        with col2:
            st.metric(
                label="Nombre de colonnes",
                value=df.shape[1]
            )
        with col3:
            st.metric(
                label="Pourcentage de doublons",
                value=f"{(df.duplicated().sum() / df.shape[0]) * 100:.2f} %"
            )
        with col4:
            st.metric(
                label="Pourcentage de NaN",
                value=f"{(df.isna().sum().sum() / df.shape[0]) * 100:.2f} %"
            )

    # --- 3) Description du Dataset ---
    st.header("3) Description du Dataset")
    st.dataframe(df.describe(), use_container_width=True)

    # --- 4) Informations sur le Dataset ---
    st.header("4) Informations sur le Dataset")

    info_df = pd.DataFrame({
        "Colonne": df.columns,
        "Type": df.dtypes.astype(str),
        "Null Count": df.isnull().sum().values
    })

    with st.container(border=True):
        st.subheader("📊 Structure du DataFrame (info)")
        st.dataframe(info_df, use_container_width=True, hide_index=True)
        
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        st.caption(f"Mémoire totale : {memory_mb:.2f} MB")

    # --- 5) Transformation des Données ---
    st.header("5) Transformation des Données")

    # 5.1
    st.subheader("5.1) Conversion des heures de réceptions, dépôts et VendorID")

    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    df["VendorID"] = df["VendorID"].astype(str)

    st.dataframe(pd.DataFrame(
        data={
            "tpep_pickup_datetime": str(df["tpep_pickup_datetime"].dtype),
            "tpep_dropoff_datetime": str(df["tpep_dropoff_datetime"].dtype),
            "VendorID": str(df["VendorID"].dtype)
        },
        index=[0]
    ), use_container_width=True)

    # 5.2
    st.subheader("5.2) Ajout de la colonne `duree_trajet`")

    df['duree_trajet'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() // 60

    st.latex(r'''
        temps\_trajet = \frac{(datetime_{dropoff} - datetime_{pickup})_{total\_seconds}}{60} 
    ''')

    with st.container(border=True):
        fig_duree = px.histogram(
            df.query("duree_trajet < 120"),
            x="duree_trajet",
            color="VendorID",
            color_discrete_map={"1": "#FF4B4B", "2": "#1C83E1"},
            title="Répartition de la durée moyenne des trajets par course",
            template="plotly_white"
        )
        st.plotly_chart(fig_duree, use_container_width=True)

    # 5.3
    st.subheader("5.3) Ajout de la colonne `vitesse_moyenne`")

    df["vitesse_moyenne"] = (df["trip_distance"] / df["duree_trajet"]) * 60
    df["vitesse_moyenne"] = df["vitesse_moyenne"].replace([np.inf, -np.inf], np.nan)

    st.latex(r'''
        vitesse_{moy} = \left(\frac{distance}{temps}\right) \cdot 60
    ''')

    with st.container(border=True):
        fig_vitesse = px.histogram(
            df.query("vitesse_moyenne < 50"),
            x="vitesse_moyenne",
            color="VendorID",
            color_discrete_map={"1": "#FF4B4B", "2": "#1C83E1"},
            title="Répartition de la vitesse moyenne des ubers",
            template="plotly_white"
        )
        st.plotly_chart(fig_vitesse, use_container_width=True)

    # 5.4
    st.subheader("5.4) Ajout de la colonne `hour`")

    df["hour"] = df["tpep_pickup_datetime"].dt.hour

    with st.container(border=True):
        df_hourly_count = df["hour"].value_counts().sort_index().reset_index()
        df_hourly_count.columns = ["hour", "count"]

        fig_hour = px.area(
            df_hourly_count,
            x="hour",
            y="count",
            range_x=[0, 24],
            title="Volume global des courses au fil de la journée",
            labels={"hour": "Heure de la journée", "count": "Nombre de courses"},
            template="plotly_white"
        )
        
        fig_hour.update_traces(
            line_color="#316896", 
            fillcolor="rgba(49, 104, 150, 0.3)"
        )
        fig_hour.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        
        st.plotly_chart(fig_hour, use_container_width=True)

    # 5.5
    st.subheader("5.5) Analyse des outliers")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            fig_box1 = px.box(
                df, y="duree_trajet",
                title="Boîte à moustaches : Durée du trajet",
                labels={"duree_trajet": "Durée (minutes)"},
                template="plotly_white"
            )
            st.plotly_chart(fig_box1, use_container_width=True)

        with col2:
            fig_box2 = px.box(
                df, y="trip_distance",
                title="Boîte à moustaches : Distance Parcourue",
                labels={"trip_distance": "Distance (miles)"},
                template="plotly_white"
            )
            st.plotly_chart(fig_box2, use_container_width=True)

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            fig_box3 = px.box(
                df, y="vitesse_moyenne",
                title="Boîte à moustaches : Vitesse moyenne",
                labels={"vitesse_moyenne": "Vitesse (km/h)"},
                template="plotly_white"
            )
            st.plotly_chart(fig_box3, use_container_width=True)

        with col2:
            fig_box4 = px.box(
                df, y="total_amount",
                title="Boîte à moustaches : Montant Total",
                labels={"total_amount": "Montant dollars ($)"},
                template="plotly_white"
            )
            st.plotly_chart(fig_box4, use_container_width=True)