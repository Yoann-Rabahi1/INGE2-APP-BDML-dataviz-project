from utils.imports import pd

def get_dataframe(url: str, sep: str) -> pd.DataFrame:

    df = pd.read_csv(url, sep=sep)
    
    return df