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
with st.expander("ℹ️ Data Privacy & Security Disclaimer"):
    st.markdown("""
    **1. No Data Storage:** This application processes your data entirely in-memory. 
    It does not connect to any database, and no data is saved to disk. 
    Once you close this tab or refresh the page, your data is permanently lost.
    
    **2. Hosting Environment:** This app is hosted on the **Streamlit Community Cloud**. 
    While data is encrypted in transit (HTTPS), it is processed on a public cloud server.
    
   **3. User Responsibility:** By using this tool, you acknowledge that you are responsible 
    for the data you upload and that you have the necessary permissions to process it 
    in a public cloud environment.
    """)
st.markdown("Upload your CSV, filter by the desired column, and export the output.")

#1. File Upload Section

uploaded_file = st.file_uploader('Upload your CSV File', type =['csv'], label_visibility='collapsed')

# --- ENHANCEMENT: Only run this code if a file is uploaded ---
if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file, dtype=str)
    df.index = df.index+1
    st.subheader(f"Results ({len(df)} rows)")

#2. Show the raw data (Expandable to save space)
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

# --- FOOTER / LEGAL DISCLAIMER ---
st.markdown("---") # Horizontal Rule
with st.container():
    st.markdown("### Privacy & Terms")
    st.caption(f"""
    **Architecture Notice:** This application is hosted on the **Streamlit Community Cloud**. 
    The application logic processes data entirely in-memory and does not save your uploads to any database or disk. 
    Your data is discarded automatically when you close this tab.
    
    **No Warranty:** This software is provided "as is," without warranty of any kind. 
    The author (Cameron Holt) is not liable for data transmitted via this public cloud environment.
    **Please do not upload sensitive PII (Personally Identifiable Information) or regulated financial data.**
    """)