import streamlit as st
import pandas as pd
from .snowflake_connection import get_connection, fetch_warehouses, fetch_databases, fetch_schemas, fetch_tables

def insert_data(database, schema, table_name, data):
    conn = get_connection()
    if conn:
        try:
            conn.cursor().execute(f"USE DATABASE {database}")
            conn.cursor().execute(f"USE SCHEMA {schema}")

            for index, row in data.iterrows():
                columns = ', '.join(row.index)
                values = ', '.join([f"'{str(val)}'" for val in row.values])
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                conn.cursor().execute(insert_query)

            conn.commit()
            st.success(f"Data inserted successfully into {table_name}.")
        except Exception as e:
            st.error(f"Error inserting data: {e}")
        finally:
            conn.close()

def show():
    st.title("Data Insertion into Snowflake Table")

    # Fetch available warehouses
    warehouses = fetch_warehouses()
    selected_warehouse = st.selectbox("Select Warehouse", warehouses)

    if selected_warehouse:
        # Fetch available databases
        databases = fetch_databases()
        selected_database = st.selectbox("Select Database", databases)
        
        if selected_database:
            schemas = fetch_schemas(selected_database)
            selected_schema = st.selectbox("Select Schema", schemas)
            
            if selected_schema:
                tables = fetch_tables(selected_database, selected_schema)
                selected_table = st.selectbox("Select Table", tables)
                
                if selected_table:
                    st.subheader(f"Selected Table: {selected_table}")

                    # File uploader to insert data
                    uploaded_file = st.file_uploader("Choose a file (CSV, JSON, TXT)", type=["csv", "json", "txt"])

                    if uploaded_file:
                        file_type = uploaded_file.type
                        if file_type == "application/json":
                            data = pd.read_json(uploaded_file)
                        elif file_type == "text/csv":
                            data = pd.read_csv(uploaded_file)
                        elif file_type == "text/plain":
                            data = pd.read_csv(uploaded_file, delimiter='\t')
                        else:
                            st.error("Unsupported file type")
                        
                        st.write(data)
                        
                        # Button to insert data
                        if st.button("Insert Data"):
                            insert_data(selected_database, selected_schema, selected_table, data)
                    
                    # Text area for manual data entry
                    st.subheader("Or Enter Data Manually")
                    manual_data = st.text_area("Enter data (comma-separated values for each row)", height=200)
                    
                    if manual_data:
                        try:
                            # Assuming user inputs data in CSV format (one row per line)
                            from io import StringIO
                            manual_data_df = pd.read_csv(StringIO(manual_data), header=None)
                            
                            # Ensure columns match table structure
                            if not manual_data_df.empty:
                                columns = manual_data_df.iloc[0].tolist()
                                values = manual_data_df[1:].values.tolist()
                                data = pd.DataFrame(values, columns=columns)
                                
                                st.write(data)
                                
                                # Button to insert data
                                if st.button("Insert Manual Data"):
                                    insert_data(selected_database, selected_schema, selected_table, data)
                        except Exception as e:
                            st.error(f"Error processing manual data: {e}")

if __name__ == "__main__":
    show()
