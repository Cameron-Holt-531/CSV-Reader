"""
CSV Data Staging Tool (V2.0)

Description:
    A Streamlit application designed to assist with data preparation and cleansing.
    This tool allows users to upload raw CSV files, filter data by specific columns,
    perform manual inline edits, and export the cleaned data for downstream 
    system ingestion (e.g., ERP, CRM imports).

Key Features:
    - Data Integrity: Forces string encoding to preserve leading zeros in IDs/Zip Codes.
    - Interactive Editing: Allows users to modify cell values directly in the browser.
    - Filter Logic: Dynamic sidebar filtering based on column values.

Author: Cameron Holt
Version: 2.0 (Stable)
Dependencies: streamlit, pandas
"""


# --- IMPORT LIBRARIES ---
import streamlit as st
import pandas as pd

# -- CONFIGURE PAGE ---
st.set_page_config(page_title='CSV File Reader', layout='wide')
st.title("CSV Reader")
st.markdown("Upload your CSV, filter by the desired column, and export the output.")

#1. File Upload Section

uploaded_file = st.file_uploader('Upload your CSV File', type =['csv'], label_visibility='collapsed')

# --- ENHANCEMENT: Only run this code if a file is uploaded ---
if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file, dtype=str)
    df.index = df.index+1
    st.subheader(f"Results ({len(df)} rows)")

#2. Show the raw daat (Expandable to save space)
    with st.expander("View Raw Data"):
        st.write(df)

    #3. Sidebar Filtering Logic
    st.sidebar.header("Filter Options")
       
        # User Selects a column to filter by:
    column_to_filter = st.sidebar.selectbox("Select a column to filter:", df.columns)

        # User select a value from that column (unique values only)
    unique_values = df[column_to_filter].unique()
    selected_value = st.sidebar.selectbox("Select value:", unique_values)

        # Apply the Filter
    filtered_df = df[df[column_to_filter] == selected_value]

    # 4. Display Filtered Data (Editable)
    st.subheader(f"Filtered Results ({len(filtered_df)} rows)")
    
        # [V2 Change] Switch to Editable grid
    edited_df = st.data_editor(filtered_df, use_container_width = True, num_rows="dynamic")

    #5. Download Button
    csv_export = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label = "Download Filtered Data as CSV",
        data = csv_export,
        file_name ='filtered_data.csv',
        mime='text/csv',
    )
else:
    st.info("Awaiting CSV file upload")