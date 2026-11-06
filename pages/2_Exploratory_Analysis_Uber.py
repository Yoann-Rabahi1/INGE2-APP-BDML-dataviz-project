from utils.imports import *
from utils.constants import DATA_URL

from onglet.data_analysis.data_loading_processing import data_processing
from onglet.data_analysis.exploratory_analysis import exploratory_analysis
from data.loaders import get_dataframe

df = get_dataframe(DATA_URL, sep=",")




tab_1, tab_2= st.tabs(["Data loading & Processing", "Exploratory Data Analysis"])

with tab_1:
    data_processing(df)



with tab_2:
    exploratory_analysis(df)






