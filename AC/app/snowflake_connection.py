import snowflake.connector
import pandas as pd
import streamlit as st

# Snowflake credentials
user = "NITHIN"
password = "Nithin@2024"
account = "ngqvwsw-vc68866"

def get_connection():
    """Establish and return a Snowflake connection."""
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        )
        return conn
    except snowflake.connector.errors.Error as e:
        st.error(f"Snowflake Error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return None

def fetch_warehouses():
    """Fetch list of warehouses."""
    conn = get_connection()
    if conn:
        try:
            query = "SHOW WAREHOUSES"
            df = pd.read_sql(query, conn)
            conn.close()
            return df['name'].tolist()
        except Exception as e:
            st.error(f"Error fetching warehouses: {e}")
            return []
    return []

def fetch_databases():
    """Fetch list of databases."""
    conn = get_connection()
    if conn:
        try:
            query = "SHOW DATABASES"
            df = pd.read_sql(query, conn)
            conn.close()
            return df['name'].tolist()
        except Exception as e:
            st.error(f"Error fetching databases: {e}")
            return []
    return []

def fetch_schemas(database):
    """Fetch list of schemas for a given database."""
    conn = get_connection()
    if conn:
        try:
            query = f"SHOW SCHEMAS IN DATABASE {database}"
            df = pd.read_sql(query, conn)
            conn.close()
            return df['name'].tolist()
        except Exception as e:
            st.error(f"Error fetching schemas: {e}")
            return []
    return []

def fetch_tables(database, schema):
    """Fetch list of tables for a given database and schema."""
    conn = get_connection()
    if conn:
        try:
            query = f"SHOW TABLES IN SCHEMA {database}.{schema}"
            df = pd.read_sql(query, conn)
            conn.close()
            return df['name'].tolist()
        except Exception as e:
            st.error(f"Error fetching tables: {e}")
            return []
    return []
