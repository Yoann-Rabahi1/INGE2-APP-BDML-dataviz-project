from utils.imports import pd, st, np, px, pdk
from data.loaders import df_process

# --- Constantes de style ---
COLOR_MAP = {"1": "#FF4B4B", "2": "#1C83E1"}
GREEN_DARK = "#004d25"
GREEN = "#05a357"
GREEN_BG = "#f0fdf4"
DIST_UNIT = "miles"  # trip_distance est en miles dans les données NYC TLC ; adapter si converti en km


def section_title(text: str, first: bool = False) -> None:
    """Bandeau de titre de section."""
    margin_top = "0" if first else "2rem"
    st.markdown(
        f"""
        <div style="
            background-color: {GREEN_BG};
            border-left: 4px solid {GREEN};
            padding: 0.5rem 1rem;
            border-radius: 4px;
            margin-top: {margin_top};
            margin-bottom: 1.5rem;
        ">
            <h2 style="color: {GREEN_DARK}; font-weight: 600; margin: 0;">{text}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(text: str) -> None:
    """Encadré d'interprétation placé sous une figure."""
    st.markdown(
        f"""
        <div style="
            background-color: #f8fafc;
            border-left: 3px solid #1C83E1;
            padding: 0.6rem 1rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        ">
            💡 <b>Lecture :</b> {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_fig(fig):
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def exploratory_analysis(df: pd.DataFrame) -> None:

    df = df_process(df)
    df["VendorID"] = df["VendorID"].astype(str)

    # =====================================================================
    # INTRODUCTION
    # =====================================================================
    st.markdown(
        f"""
        <div style="
            background-color: {GREEN_BG};
            border: 1px solid {GREEN};
            padding: 1rem 1.25rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
        ">
            <h3 style="color: {GREEN_DARK}; margin-top: 0;">Introduction</h3>
            <p style="margin-bottom: 0.5rem;">
                Cette section prolonge le travail réalisé lors de la <b>phase de traitement des données</b>.
                Les deux premières figures (<i>distribution des distances</i> et <i>répartition des courses par heure</i>)
                y avaient déjà été visualisées pour contrôler la qualité des données. Nous les reprenons ici,
                cette fois pour <b>en tirer des enseignements métier</b>.
            </p>
            <p style="margin-bottom: 0;">
                Nous passerons ensuite à des visualisations dynamiques (carte de chaleur, nuage de points durée / distance)
                accompagnées d'indicateurs clés, avant de conclure par une synthèse narrative de la demande de taxis à New York.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================================
    # I) STATISTICS VISUALIZATIONS
    # =====================================================================
    section_title("I) Statistics Visualizations", first=True)

    # --- 1.1) Distribution des distances ---
    st.subheader(f"1.1) Distribution des distances de trajet ({DIST_UNIT})")

    with st.container(border=True):
        fig_dist = px.histogram(
            df,
            x="trip_distance",
            color="VendorID",
            range_x=[0, 20],
            color_discrete_map=COLOR_MAP,
            labels={"trip_distance": f"Distance ({DIST_UNIT})", "count": "Nombre de courses"},
        )
        st.plotly_chart(style_fig(fig_dist), use_container_width=True)

    short_share = (df["trip_distance"] < 3).mean() * 100
    insight(
        f"la distribution est fortement asymétrique à droite : environ <b>{short_share:.0f} %</b> des courses "
        f"font moins de 3 {DIST_UNIT}. Le taxi sert surtout à des <b>déplacements courts, intra-urbains</b>, "
        f"les longs trajets (aéroports, banlieue) restant minoritaires. Les deux opérateurs ont un profil très similaire."
    )

    # --- 1.2) Répartition par heure ---
    st.subheader("1.2) Répartition des courses par heure de la journée")

    with st.container(border=True):
        if "hour" in df.columns:
            fig_hour = px.histogram(
                df,
                x="hour",
                color="VendorID",
                barmode="group",
                range_x=[0, 24],
                color_discrete_map=COLOR_MAP,
                labels={"hour": "Heure de la journée", "count": "Nombre de courses"},
            )
            st.plotly_chart(style_fig(fig_hour), use_container_width=True)

            peak_hour = int(df["hour"].value_counts().idxmax())
            insight(
                f"l'activité est au plus bas en pleine nuit, monte dès le matin (pic des <b>trajets domicile-travail</b>), "
                f"puis atteint son maximum en fin de journée, autour de <b>{peak_hour} h</b>, "
                f"quand les sorties de bureau se mêlent aux loisirs."
            )
        else:
            st.warning("La colonne 'hour' est absente du DataFrame.")

    # =====================================================================
    # II) DYNAMIC VISUALIZATIONS + KPI
    # =====================================================================
    section_title("II) Dynamic Visualizations + KPI")

    # --- 2.1) Carte ---
    st.subheader("2.1) Carte interactive des localisations (points de dépose)")

    df_map = df[["dropoff_latitude", "dropoff_longitude", "passenger_count", "VendorID"]].copy()
    df_map = df_map.rename(columns={"dropoff_latitude": "latitude", "dropoff_longitude": "longitude"})
    df_map = df_map.dropna(subset=["latitude", "longitude"])

    with st.container(border=True):
        view_state = pdk.ViewState(
            latitude=df_map["latitude"].mean(),
            longitude=df_map["longitude"].mean(),
            zoom=11,
            pitch=0,
        )
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=df_map,
            get_position=["longitude", "latitude"],
            get_weight="passenger_count",  # intensité pondérée par le nombre de passagers
            radius_pixels=30,
        )
        st.pydeck_chart(
            pdk.Deck(layers=[heatmap_layer], initial_view_state=view_state, tooltip=False)
        )

    insight(
        "les zones les plus intenses se concentrent sur <b>Manhattan</b>, cœur économique et touristique. "
        "Des points chauds plus isolés apparaissent autour des <b>aéroports</b> (JFK, LaGuardia), "
        "tandis que les autres arrondissements restent beaucoup moins denses."
    )

    # --- 2.2) Scatter durée vs distance ---
    st.subheader(f"2.2) Durée du trajet vs Distance (taille = montant total)")

    df_filtered = df.query("1 < duree_trajet <= 120 and total_amount > 0 and trip_distance > 0")
    correlation = df_filtered["duree_trajet"].corr(df_filtered["trip_distance"])

    with st.container(border=True):
        fig_scatter = px.scatter(
            df_filtered,
            x="duree_trajet",
            y="trip_distance",
            color="VendorID",
            size="total_amount",
            range_y=[0, 50],
            color_discrete_map=COLOR_MAP,
            hover_data=["passenger_count", "tip_amount"],
            title="Durée du trajet vs distance",
            labels={
                "duree_trajet": "Durée du trajet (min)",
                "trip_distance": f"Distance ({DIST_UNIT})",
            },
        )
        st.plotly_chart(style_fig(fig_scatter), use_container_width=True)
        st.caption(f"Coefficient de corrélation (durée / distance) : **{correlation:.2f}**")

        col1, col2 = st.columns(2)
        median_duration = df["duree_trajet"].median()
        median_distance = df["trip_distance"].median()

        with col1:
            st.metric(label="Durée médiane d'une course (min)", value=f"{median_duration:.1f} min")
        with col2:
            st.metric(
                label=f"Distance médiane par course ({DIST_UNIT})",
                value=f"{median_distance:.2f} {DIST_UNIT}",
            )

    insight(
        f"durée et distance sont globalement liées (corrélation de <b>{correlation:.2f}</b>), "
        f"mais le nuage reste dispersé : à distance égale, la durée varie beaucoup. "
        f"C'est la signature de la <b>congestion</b> : un même trajet peut prendre deux fois plus de temps "
        f"aux heures de pointe. Les gros points (montants élevés) correspondent surtout aux longues distances."
    )

    # =====================================================================
    # III) EXPLAIN FIGURES
    # =====================================================================
    section_title("III) Explain Figures")

    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True):
            st.markdown("**📊 Distances & horaires**")
            st.markdown(
                "- **Trajets courts dominants** : la majorité des courses reste en centre-ville.\n"
                "- **Pics de pendulaires** : montée matinale puis pic de fin de journée.\n"
                "- **Nuit calme** : creux d'activité en milieu de nuit."
            )
    with col_b:
        with st.container(border=True):
            st.markdown("**🗺️ Espace & temps de trajet**")
            st.markdown(
                "- **Manhattan** concentre l'essentiel des déposes.\n"
                "- **Aéroports** : points chauds secondaires, avec des trajets plus longs et plus chers.\n"
                "- **Congestion** : forte variabilité de la durée à distance comparable."
            )

    # =====================================================================
    # IV) STORYTELLING (BI)
    # =====================================================================
    section_title("IV) Storytelling")

    total_trips = len(df)
    avg_amount = df_filtered["total_amount"].mean()
    peak_hour_story = int(df["hour"].value_counts().idxmax()) if "hour" in df.columns else None

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Courses analysées", f"{total_trips:,}".replace(",", " "))
    k2.metric("Courses < 3 " + DIST_UNIT, f"{short_share:.0f} %")
    k3.metric("Montant moyen", f"{avg_amount:.2f} $")
    if peak_hour_story is not None:
        k4.metric("Heure de pointe", f"{peak_hour_story} h")

    with st.container(border=True):
        st.markdown(
            f"""
**Ce que racontent les données**

La demande de taxis à New York est avant tout **une demande urbaine de proximité** : près de {short_share:.0f} % des courses
sont courtes et se déroulent dans Manhattan. Cette demande suit le **rythme de la ville** : elle s'éveille avec les pendulaires,
culmine en fin de journée, puis retombe la nuit.

Dans l'espace, l'activité est très concentrée : Manhattan en est le cœur, les aéroports forment des pôles secondaires
qui génèrent moins de courses mais des trajets plus longs et plus rémunérateurs.

Enfin, la durée d'une course dépend autant de **l'état du trafic** que de la distance : c'est un levier d'amélioration
(allocation des véhicules aux heures de pointe, anticipation de la congestion) pour un opérateur.

*Les deux opérateurs (VendorID 1 et 2) présentent des comportements proches, ce qui suggère un marché homogène.*
            """
        )