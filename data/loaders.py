from utils.imports import pd, np

def get_dataframe(url: str, sep: str) -> pd.DataFrame:

    df = pd.read_csv(url, sep=sep)
    
    return df

def df_process(df : pd.DataFrame) -> pd.DataFrame:

    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    df["VendorID"] = df["VendorID"].astype(str)
    df['duree_trajet'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() // 60
    df["vitesse_moyenne"] = (df["trip_distance"] / df["duree_trajet"]) * 60
    df["vitesse_moyenne"] = df["vitesse_moyenne"].replace([np.inf, -np.inf], np.nan)
    df["hour"] = df["tpep_pickup_datetime"].dt.hour

    return df
