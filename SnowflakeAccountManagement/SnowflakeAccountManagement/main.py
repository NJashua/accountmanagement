import streamlit as st
from app.snowflake_connection import get_connection
from app import user_management, role_management, database_management, warehouse_management, data_sharing, credits_usage, custom_table_creation, data_insertion
from snowflake.connector import ProgrammingError

# Initialize session state variables
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Define pages
PAGES = {
    "User Management": user_management,
    "Role Management": role_management,
    "Database Management": database_management,
    "Warehouse Management": warehouse_management,
    "Data Sharing": data_sharing,
    "Credits Usage": credits_usage,
    "Custom Table": custom_table_creation,
    "Data Insertion": data_insertion
}

def check_user_exists(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE user_db;")
        cursor.execute("USE SCHEMA user_schema;")
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}';")
        user = cursor.fetchone()
        return user is not None
    finally:
        cursor.close()
        conn.close()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("USE DATABASE user_db;")
        cursor.execute("USE SCHEMA user_schema;")
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');")
        conn.commit()
        st.success("Registration successful! Please log in.")
    except ProgrammingError as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def show_page(page_name):
    """Render the selected page."""
    if page_name in PAGES:
        PAGES[page_name].show()
    else:
        st.error("Page not found")

def main():
    st.markdown("""
        <style>
            .css-1d391kg .css-1d391kg {
                background-color: #003366; /* Dark blue background */
                color: white;
            }
            .css-1d391kg .css-1d391kg .stSelectbox label {
                color: white;
            }
            .css-1d391kg .css-1d391kg .stButton>button {
                background-color: #004080; /* Blue background */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
                margin: 10px 0;
                cursor: pointer;
                transition-duration: 0.4s;
            }
            .css-1d391kg .css-1d391kg .stButton>button:hover {
                background-color: #0059b3; /* Darker blue on hover */
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.subheader("Login/Register")
        username = st.text_input("Username", key="login_reg_user")
        password = st.text_input("Password", type='password', key="login_reg_pass")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                if check_user_exists(username, password):
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                else:
                    st.error("Invalid credentials. Please try again or register.")
        
        with col2:
            if st.button("Register"):
                register_user(username, password)

    else:
        # Sidebar for page selection
        st.sidebar.title("Dev Stage")
        selection = st.sidebar.selectbox("Select a Page", ["Snowflake Connection"] + list(PAGES.keys()))

        # Connection handling
        if selection == "Snowflake Connection":
            st.subheader("Connect to Snowflake")

            if st.button("Connect"):
                conn = get_connection()
                if conn:
                    st.session_state.connected = True
                    st.success("Connection successful")
                else:
                    st.session_state.connected = False
                    st.error("Failed to connect")

        # Render the selected page if connected or if it's the connection page
        if st.session_state.connected or selection == "Snowflake Connection":
            show_page(selection)

if __name__ == '__main__':
    main()
