# CSV Data Staging Tool (v2.2.0)

## Overview
The **CSV Data Staging Tool** is a lightweight, defensive application designed to solve the "Garbage In, Garbage Out" problem in data integration. 

As an Integration Engineer, I frequently encounter raw data that is unfit for downstream ingestion (ERP/CRM imports). This tool provides a staging environment to sanitize, filter, and validate CSV data before it enters a production system.

## Features
* **Defensive Importing:** Validates file integrity before processing to prevent crash-loops.
* **Automated Sanitization:** * Removes "Ghost Rows" (empty rows often left by Excel).
    * Trims whitespace from headers and cells.
    * Deduplicates records automatically.
* **Audit Logging:** Generates a downloadable log of rows that were removed/cleaned.
* **Privacy-First:** Processes data entirely in-memory using Streamlit; no data is stored on disk.

## Tech Stack
* **Language:** Python 3.12+
* **Interface:** Streamlit
* **Data Processing:** Pandas

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/csv-staging-tool.git](https://github.com/YOUR_USERNAME/csv-staging-tool.git)

2. Install depedencies:
   ```bash
   pip install -r requirements.txt

3. Run the application
   ```bash
   streamlit run CSV_Reader.py
