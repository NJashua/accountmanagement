import streamlit as st
from app.snowflake_connection import get_connection

def show():
    st.markdown("""
        <style>
            .stApp {
                background-color: black; /* Light gray background */
                padding: 20px;
                font-family: 'Arial', sans-serif;
            }
            .stHeader, .stSubheader, .stMarkdown, .stCaption, .stText, .stMetric, .stCodeBlock, .stJson {
                color: black; /* Black text */
            }
            .stButton>button {
                background-color: green; /* Blue background */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
                margin: 10px 0;
                cursor: pointer;
                transition-duration: 0.4s;
            }
            .stButton>button:hover {
                background-color: darkblue; /* Darker blue on hover */
                color: white;
            }
            .stSelectbox, .stTextInput, .stTextArea {
                margin-bottom: 20px;
            }
            .stTextInput>input, .stNumberInput>input, .stSelectbox>select {
                border: 1px solid #ddd; /* Light border */
                border-radius: 4px;
                padding: 10px;
                background-color: #fff; /* White background */
                color: #333; /* Dark text */
            }
            .stCheckbox>label {
                color: black; /* Black text */
            }
        </style>
    """, unsafe_allow_html=True)

    st.header("Data Sharing Management")

    def create_data_share(share_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"CREATE SHARE {share_name}")
            conn.close()
            st.success(f"Data share {share_name} created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def add_table_to_share(share_name, database_name, schema_name, table_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"GRANT USAGE ON DATABASE {database_name} TO SHARE {share_name}")
            cur.execute(f"GRANT USAGE ON SCHEMA {database_name}.{schema_name} TO SHARE {share_name}")
            cur.execute(f"GRANT SELECT ON TABLE {database_name}.{schema_name}.{table_name} TO SHARE {share_name}")
            conn.close()
            st.success(f"Table {table_name} added to share {share_name} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def remove_table_from_share(share_name, database_name, schema_name, table_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"REVOKE SELECT ON TABLE {database_name}.{schema_name}.{table_name} FROM SHARE {share_name}")
            conn.close()
            st.success(f"Table {table_name} removed from share {share_name} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def drop_data_share(share_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"DROP SHARE {share_name}")
            conn.close()
            st.success(f"Data share {share_name} dropped successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create Data Share")
    share_name_create = st.text_input("Data Share Name to Create")
    if st.button("Create Data Share"):
        create_data_share(share_name_create)

    st.subheader("Add Table to Data Share")
    share_name_add = st.text_input("Data Share Name to Add Table")
    database_name_add = st.text_input("Database Name")
    schema_name_add = st.text_input("Schema Name")
    table_name_add = st.text_input("Table Name")
    if st.button("Add Table to Data Share"):
        add_table_to_share(share_name_add, database_name_add, schema_name_add, table_name_add)

    st.subheader("Remove Table from Data Share")
    share_name_remove = st.text_input("Data Share Name to Remove Table")
    database_name_remove = st.text_input("Database Name", key="db_remove")
    schema_name_remove = st.text_input("Schema Name", key="schema_remove")
    table_name_remove = st.text_input("Table Name", key="table_remove")
    if st.button("Remove Table from Data Share"):
        remove_table_from_share(share_name_remove, database_name_remove, schema_name_remove, table_name_remove)

    st.subheader("Drop Data Share")
    share_name_drop = st.text_input("Data Share Name to Drop")
    if st.button("Drop Data Share"):
        drop_data_share(share_name_drop)
