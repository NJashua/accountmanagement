import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from app.snowflake_connection import get_connection, fetch_warehouses, fetch_databases, fetch_schemas

def fetch_credits_data(warehouse, database, schema):
    """Fetch credits data for the selected warehouse, database, and schema."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"USE DATABASE {database}")
        cur.execute(f"USE SCHEMA {schema}")

        # Fetch total credits used in the last month
        cur.execute(f"""
            SELECT 
                SUM(credits_used) AS total_credits_used 
            FROM 
                WAREHOUSE_METERING_HISTORY
            WHERE 
                start_time >= DATEADD('month', -1, CURRENT_DATE())
                AND warehouse_name = '{warehouse}'
        """)
        total_credits_used = cur.fetchone()[0]

        # Fetch daily usage credits in a month
        cur.execute(f"""
            SELECT 
                start_time::date AS usage_date, 
                SUM(credits_used) AS daily_credits_used
            FROM 
                WAREHOUSE_METERING_HISTORY
            WHERE 
                start_time >= DATEADD('month', -1, CURRENT_DATE())
                AND warehouse_name = '{warehouse}'
            GROUP BY 
                start_time::date
            ORDER BY 
                usage_date
        """)
        daily_credits = cur.fetchall()
        
        # Convert to DataFrame
        daily_credits_df = pd.DataFrame(daily_credits, columns=['usage_date', 'daily_credits_used'])
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        total_credits_used = None
        daily_credits_df = pd.DataFrame(columns=['usage_date', 'daily_credits_used'])
        
    finally:
        cur.close()
        conn.close()

    return total_credits_used, daily_credits_df

def plot_credits_usage(daily_credits_df):
    """Plot credits usage data."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(daily_credits_df['usage_date'], daily_credits_df['daily_credits_used'], color='skyblue')
    ax.set_xlabel("Date")
    ax.set_ylabel("Credits Used")
    ax.set_title("Daily Credits Usage")

    # Format x-axis labels to display month name
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    return fig

def show():
    """Display Snowflake credits usage overview with dropdown selections."""
    st.header("Snowflake Credits Usage Overview")

    # Dropdowns for selecting warehouse, database, and schema
    warehouses = fetch_warehouses()
    databases = fetch_databases()
    
    selected_warehouse = st.selectbox("Select Warehouse", warehouses)
    selected_database = st.selectbox("Select Database", databases)
    
    # Fetch schemas based on selected database
    schemas = fetch_schemas(selected_database)
    selected_schema = st.selectbox("Select Schema", schemas)
    
    # Fetch and display total credits used and daily credits usage
    total_credits_used, daily_credits_df = fetch_credits_data(selected_warehouse, selected_database, selected_schema)
    if total_credits_used is not None:
        st.subheader(f"Total Credits Used in the Last Month: {total_credits_used:.2f}")
        
        if not daily_credits_df.empty:
            st.subheader("Daily Credits Usage")
            st.pyplot(plot_credits_usage(daily_credits_df))
        else:
            st.write("No daily credits usage data available.")
    else:
        st.write("No credits data available.")
