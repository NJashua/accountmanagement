import streamlit as st
from app import snowflake_connection, user_management, role_management, database_management, data_sharing, warehouse_management

PAGES={
    "Snowflake Connection": snowflake_connection,
    "User Management": user_management,
    "Role Management" : role_management,
    "Database Management": database_management,
    "Warehouse Management": warehouse_management,
    "Data Sharing": data_sharing
    }
# st.title("Navigation")
selection=st.sidebar.radio("Go to", list(PAGES.keys()))
page=PAGES[selection]
page.show()
