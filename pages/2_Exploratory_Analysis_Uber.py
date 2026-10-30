from utils.imports import *
from data.loaders import get_dataframe

url = r"https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"

df = get_dataframe(url, ",")

st.dataframe(df)