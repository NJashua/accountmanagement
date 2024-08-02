import streamlit as st
from app import snowflake_connection, user_management, role_management, database_management, warehouse_management, data_sharing, credits_usage, custom_table_creation, data_insertion

# Initialize session state variables
if 'connected' not in st.session_state:
    st.session_state.connected = False

# Define pages
PAGES = {
    "Snowflake Connection": snowflake_connection,
    "User Management": user_management,
    "Role Management": role_management,
    "Database Management": database_management,
    "Warehouse Management": warehouse_management,
    "Data Sharing": data_sharing,
    "Credits Usage": credits_usage,
    "Custom Table": custom_table_creation,
    "Data Insertion": data_insertion
}

st.sidebar.title("Dev Stage")
selection = st.sidebar.radio("Go To", list(PAGES.keys()))

def show_page(page_name):
    """Render the selected page."""
    if page_name in PAGES:
        PAGES[page_name].show()
    else:
        st.error("Page not found")

if selection == "Snowflake Connection":
    st.subheader("Connect to Snowflake")
    
    if st.button("Connect"):
        conn = snowflake_connection.get_connection()
        if conn:
            st.session_state.connected = True
            st.success("Connection successful")
        else:
            st.session_state.connected = False
            st.error("Failed to connect")

if st.session_state.connected or selection == "Snowflake Connection":
    show_page(selection)
else:
    st.info("Please connect to Snowflake before accessing other pages.")
