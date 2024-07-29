import streamlit as st
from app.snowflake_connection import get_connection

def show():
    st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                padding: 20px;
                font-family: 'Arial', sans-serif;
            }
            .stHeader, .stSubheader {
                color: #333333;
                text-align: center;
                margin-bottom: 20px;
            }
            .stButton>button {
                background-color: #4CAF50; /* Green */
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
                background-color: #45a049; /* Darker Green */
                color: white;
            }
            .stSelectbox, .stTextInput, .stTextArea {
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.header("Database Management")

    # Function to create a database
    def create_database(database_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {database_name}")
            conn.close()
            st.success(f"Database {database_name} created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    # Function to clone a database
    def clone_database(source_db, target_db):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {target_db} CLONE {source_db}")
            conn.close()
            st.success(f"Database {source_db} cloned to {target_db} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    # Function to drop a database
    def drop_database(database_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"DROP DATABASE {database_name}")
            conn.close()
            st.success(f"Database {database_name} dropped successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    # Function to list all databases
    def list_databases():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SHOW DATABASES")
            databases = cur.fetchall()
            conn.close()
            return [db[1] for db in databases]  # Extracting database names
        except Exception as e:
            st.error(f"Error: {e}")
            return []
    def transefer_ownership(database_name, new_role):
        try:
            conn = get_connection()
            curr = conn.cursor()
            # curr.execute(f"REVOKE USAGE ON DATABASE {database_name} FROM SHARE myshare")
            curr.execute(f"GRANT OWNERSHIP ON DATABASE {database_name} TO ROLE {new_role}")
            curr.execute(f"GRANT USAGE ON DATABASE {database_name} TO ROLE {new_role}")
            conn.close()
            st.success(f"Ownership of database {database_name} transferred to role {new_role} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")


    # UI for database management
    st.subheader("Create Database")
    database_name_create = st.text_input("Database Name to Create")
    if st.button("Create Database"):
        create_database(database_name_create)

    st.subheader("Clone Database")
    databases = list_databases()
    source_db = st.selectbox("Select Source Database", databases)
    target_db = st.text_input("Target Database Name")
    if st.button("Clone Database"):
        clone_database(source_db, target_db)

    st.subheader("Drop Database")
    selected_db_drop = st.selectbox("Select Database to Drop", databases)
    if st.button("Drop Database"):
        drop_database(selected_db_drop)

    st.subheader("Transfer Ownership")
    selected_db_ownership = st.selectbox("Select database to grant", databases)
    new_role = st.text_input("New Role")
    if st.button("Transfer Ownership"):
        transefer_ownership(selected_db_ownership, new_role)

show()
