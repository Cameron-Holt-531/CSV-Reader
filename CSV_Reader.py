# --- IMPORT LIBRARIES ---
import streamlit as st
import pandas as pd
# -- CONFIGURE PAGE ---
st.set_page_config(page_title='CSV File Reader', layout='wide')
st.title("CSV Reader")
upload_file = st.file_uploader('Upload your CSV File')
# --- ENHANCEMENT: Only run this code if a file is uploaded ---
if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.dataframe(df, width=1800, height=1200)
