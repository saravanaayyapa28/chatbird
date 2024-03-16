import os
import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

# Function to search database
def search_database(conn, search_term, columns):
    cursor = conn.cursor()
    # Construct the WHERE clause dynamically to search across multiple columns
    where_clause = " OR ".join([f"{column} LIKE '%{search_term}%'" for column in columns])
    cursor.execute(f"SELECT * FROM student WHERE {where_clause}")

    results = cursor.fetchall()
    return results

# Set Streamlit page configuration
st.set_page_config(page_title="AI APP TO CHAT WITH SQL DB")

# Streamlit UI
st.header("ASK ANYTHING ABOUT YOUR DB")

# Text input for user query
search_term = st.text_input('Ask a question here:')
submit_button = st.button('Search')

st.image("robot.jpg", use_column_width=True)

# Additional options in sidebar
st.sidebar.subheader("Additional Options")

option1 = st.sidebar.selectbox('Choose The Format ', ['Excel', 'CSV', 'PDF'])
option2 = st.sidebar.selectbox('Select The Downloaded Option ', ['View', 'Download'])

# Database connection and insertion
def insert_into_database(prediction_input, pp, accuracy):
    conn = sqlite3.connect("streamlit/Streamlit_programs/chatbird/customer.db")
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO userinputresponse VALUES (?, ?, ?)", (prediction_input, pp, str(accuracy)))
    conn.commit()
    conn.close()

# Inserting data into database
if submit_button:
    # Assuming prediction_input, pp, and accuracy are defined elsewhere in your code
    prediction_input = "Sample Prediction Input"
    pp = "Sample PP"
    accuracy = 0.85
    insert_into_database(prediction_input, pp, accuracy)

# SQLite database connection
db_file_path = 'E:/customer.db'
if os.path.exists(db_file_path):
    conn = sqlite3.connect(db_file_path)
    st.write("Database connected successfully.")

    if search_term:
        # Specify the columns to search in
        search_columns = ["LastName", "FirstName", "ID","Age"]  # Add more columns as needed
        # Perform search and display results
        results = search_database(conn, search_term, search_columns)
        if not results:
            st.write('No results found.')
        else:
            st.write(f'Results for search term "{search_term}":')
            # Display results in table format
            df = pd.DataFrame(results, columns=["ID", "FirstName", "LastName", "Age", "Mobile", "AdditionalColumn"])  # Include all columns returned from the SQL query
            st.dataframe(df)
            
            # Download option
            if option2 == 'Download':
                if option1 == 'Excel':
                    excel_file = BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label="Download Excel", data=excel_file, file_name='search_results.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                elif option1 == 'CSV':
                    csv_file = df.to_csv(index=False).encode()
                    st.download_button(label="Download CSV", data=csv_file, file_name='search_results.csv', mime='text/csv')
                elif option1 == 'PDF':
                    # Code to convert DataFrame to PDF
                    # Placeholder for PDF conversion code
                    st.write("PDF download option will be implemented soon.")
            else:
                st.write('Viewing the data without download')
                
    else:
        st.write('Please enter a search term.')
else:
    st.write("Error: Database file not found. Please ensure that the database file exists at the specified path.")
    st.write(f"Specified path: {db_file_path}")

# Close database connection
if 'conn' in locals():
    conn.close()
