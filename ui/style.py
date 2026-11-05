CUSTOM_CSS = """
    <style>
        /* Style global des conteneurs (effet Card) */
        div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
            margin-bottom: 20px;
        }
        
        /* Titres principaux */
        h1 {
            color: #1E293B;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        h2 {
            color: blue;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 2px solid #316896;
            padding-bottom: 5px;
            display: inline-block;
        }
        
        h3 {
            color: green;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 20px;
        }
        
        /* Style des métriques */
        div[data-testid="stMetric"] {
            background-color: lightgreen;
            border: 1px solid #E2E8F0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.01);
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #64748B;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.4rem;
            color: #0F172A;
            font-weight: 700;
        }
    </style>
"""