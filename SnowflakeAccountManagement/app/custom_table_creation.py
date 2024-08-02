import streamlit as st
from app.snowflake_connection import get_connection, fetch_warehouses, fetch_databases, fetch_schemas, fetch_tables

def create_table(database, schema, table_name, columns):
    conn = get_connection()
    if conn:
        try:
            conn.cursor().execute(f"USE DATABASE {database}")
            conn.cursor().execute(f"USE SCHEMA {schema}")
            create_table_query = f"CREATE TABLE {table_name} ({columns})"
            conn.cursor().execute(create_table_query)
            conn.commit()
            st.success(f"Table '{table_name}' created successfully in {database}.{schema}.")
        except Exception as e:
            st.error(f"Error creating table: {e}")
        finally:
            conn.close()

def show():
    st.title("Custom Table Creation in Snowflake")

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
                selected_table = st.selectbox("Select Table (or create new)", [""] + tables)
                
                if selected_table:
                    st.subheader(f"Selected Table: {selected_table}")

                # Provide dummy data for table creation
                table_name = st.text_input("Enter New Table Name (Leave empty to select existing table)", value="")
                columns = st.text_area("Enter Columns (e.g., id INT, name STRING, created_at TIMESTAMP)", 
                                       value="id INT, name STRING, created_at TIMESTAMP")
                
                if st.button("Create Table") and table_name:
                    if selected_database and selected_schema and table_name and columns:
                        create_table(selected_database, selected_schema, table_name, columns)
                    else:
                        st.error("Please fill out all fields to create a table.")

if __name__ == "__main__":
    show()
