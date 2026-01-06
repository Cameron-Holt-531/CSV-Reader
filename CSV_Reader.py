"""
CSV Data Staging Tool (V2.0.1)

Description:
    A Streamlit application designed to assist with data preparation and cleansing.
    This tool allows users to upload raw CSV files, filter data by specific columns,
    perform manual inline edits, and export the cleaned data for downstream 
    system ingestion (e.g., ERP, CRM imports).

Key Features:
    - [NEW] Main Stage Filtering: Filter controls moved from sidebar to main view.
    - [NEW] Sample Data Generator: Instantly creates dummy data for testing.
    - Data Integrity: Forces string encoding to preserve leading zeros in IDs/Zip Codes.
    - Interactive Editing: Allows users to modify cell values directly in the browser.
    - Filter Logic: Dynamic sidebar filtering based on column values.

Author: Cameron Holt
Version: 2.1.0 (Stable)
Dependencies: streamlit, pandas
"""


# --- IMPORT LIBRARIES ---
import streamlit as st
import pandas as pd

# --- GENERATE SAMPLE DATA ---
def generate_sample_data():
    """Creates a dummy DataFrame to demonstrate app functionality."""
    data = {
        'EmployeeID': ['001024', '002055', '003109', '004552', '005110'],
        'FirstName': ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan'],
        'LastName': ['Smith', 'Jones', 'Brown', 'Prince', 'Wright'],
        'Department': ['Accounting', 'IT', 'Sales', 'IT', 'Accounting'],
        'Status': ['Active', 'Active', 'On Leave', 'Active', 'Terminated'],
        'Salary': ['55000', '85000', '62000', '90000', '58000']
    }
    return pd.DataFrame(data)



# -- CONFIGURE PAGE ---
st.set_page_config(page_title='CSV File Reader', layout='wide')
st.title("CSV Reader")

st.markdown("Upload your CSV to begin.")

#1. Data Source Section (Side-by-Side)
    # Configuring a 4:1 ratio so that the button stays compact to the right.
col1, col2 = st.columns([4,1])

with col1:
    uploaded_file = st.file_uploader('Upload your CSV File', type =['csv'], label_visibility='collapsed')
with col2:
    # Adding vertical whitespace so the button aligns with the input box
    st.write("")
    if st.button("Load Sample Data"):
        st.session_state['sample_data']= generate_sample_data()

# --- Logic: Determine which data to use
df = None

if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file, dtype=str)
    df.index = df.index+1
    # If a file is uploaded, clear any sample data from the session
    if 'sample_data' in st.session_state:
        del st.session_state['sample_data']
    st.subheader(f"Results ({len(df)} rows)")

elif 'sample_data' in st.session_state:
    df = st.session_state['sample_data']
    st.info("Using generated sample data.")

if df is not None:

#2. Show the raw data (Expandable to save space)
    with st.expander("View Raw Data"):
        st.write(df)

    st.markdown("### Data Editor")


#3. Main Stage Filtering
    f_col1, f_col2 = st.columns(2)

    with f_col1:
    # Placeholder option prevents auto-filtering
        columns_list =["-- All Columns --"] + list(df.columns)
        column_to_filter = st.selectbox("Filter by Column:", columns_list)

    # Only show value Selector if a specific column is chosen
    if column_to_filter != "-- All Columns --":
        with f_col2:
            unique_values = df[column_to_filter].unique()
            selected_value = st.selectbox("Select value:", unique_values)

        # Apply the Filter
        filtered_df = df[df[column_to_filter] == selected_value]
    
    else:
    # No Filter Selected
        filtered_df = df

    # Dynamic Header Update
    st.caption(f"Showing ({len(filtered_df)} rows)")
    
# 4. Display Data (Editable)
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

    st.markdown("---") # Visual separator for the footer

# --- FOOTER SECTION ---
with st.container():
    with st.expander("Legal Disclaimer & Data Privacy Policy"):
        st.markdown("""
        **1. Architecture & Privacy:** This application is hosted on the **Streamlit Community Cloud**. Processing occurs entirely in-memory on a public cloud server; no data is saved to disk or databases. Your data is permanently discarded automatically when you close this tab or refresh the page.
        
        **2. No Warranty & Liability:** This software is provided "as is," without warranty of any kind. The author (Cameron Holt) is not liable for data transmitted via this public cloud environment. **Do not upload sensitive PII (Personally Identifiable Information) or regulated financial data.**
        
        **3. User Responsibility:** By using this tool, you acknowledge that you are responsible for the data you upload and that you have the necessary permissions to process it in a public cloud environment.
        """)