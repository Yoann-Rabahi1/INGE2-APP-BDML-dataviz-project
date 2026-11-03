from utils.imports import pd, st
from utils.constants import PAGE_SIZE

def df_all(df : pd.DataFrame):

    total_pages = (len(df) + PAGE_SIZE - 1) // PAGE_SIZE

    dataframe_slot = st.empty()
    with st.container(horizontal_alignment="right"):
        page = st.pagination(num_pages=total_pages)

    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE

    df_page = df.iloc[start_idx:end_idx]

    dataframe_slot.dataframe(df_page, hide_index=True)