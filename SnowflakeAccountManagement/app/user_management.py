import pandas as pd
import streamlit as st
from app.snowflake_connection import get_connection

def list_users():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SHOW USERS")
        users = cur.fetchall()
        conn.close()

        # Add column names
        column_names = [
            "name",
            "created_on",
            "login_name",
            "display_name",
            "first_name",
            "last_name",
            "email",
            "mins_to_unlock",
            "days_to_expiry",
            "comment",
            "disabled",
            "must_change_password",
            "snowflake_lock",
            "default_warehouse",
            "default_namespace",
            "default_role",
            "default_secondary_roles",
            "ext_authn_duo",
            "ext_authn_uid",
            "mins_to_bypass_mfa",
            "owner",
            "last_success_login",
            "expires_at_time",
            "locked_until_time",
            "has_password",
            "has_rsa_public_key"
        ]

        # Convert the users data to a DataFrame
        df = pd.DataFrame(users, columns=column_names)

        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def show():
    st.header("User Management")

    # Adding some color to the header
    st.markdown("""
        <style>
            .stHeader {
                color: #FFFFFF;
                background-color: #6A1B9A; /* Purple */
                padding: 10px;
                border-radius: 12px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Function to create a new user
    def create_user(username, password):
        try:
            conn = get_connection()
            cur = conn.cursor()
            query = f"CREATE USER {username} PASSWORD = '{password}'"
            cur.execute(query)
            conn.close()
            st.success(f"User {username} created successfully!", icon="✅")
        except Exception as e:
            st.error(f"Error: {e}", icon="❌")

    # UI for creating a user
    st.subheader("Create User")
    new_username = st.text_input("New Username", key="new_username_input_unique")
    new_password = st.text_input("New Password", type="password", key="new_password_input_unique")
    if st.button("Create User", key="create_user_btn_unique"):
        if new_username and new_password:
            create_user(new_username, new_password)
        else:
            st.error("Please provide both username and password.")

    # Display the existing users
    st.subheader("Existing Users")
    users_df = list_users()
    if users_df is not None:
        st.table(users_df)
    else:
        st.write("No users found or error in fetching users.")

    # Adding some color to the UI
    st.markdown("""
        <style>
            .stButton>button {
                background-color: #4CAF50; /* Green */
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                transition-duration: 0.4s;
            }

            .stButton>button:hover {
                background-color: #388E3C;
                color: white;
                border: 2px solid #388E3C;
            }

            .stHeader, .stSubheader {
                color: #FFFFFF;
                background-color: #6A1B9A; /* Purple */
            }

            .stApp {
                background-color: #282C34; /* Dark Background */
                padding: 20px;
                color: #ABB2BF; /* Light Text */
            }

            .stTextInput>div>input {
                border: 2px solid #007FFF;
                border-radius: 8px;
                padding: 10px;
                background-color: #3C3F41; /* Darker Background for Input */
                color: #FFFFFF; /* White Text */
            }
        </style>
    """, unsafe_allow_html=True)

# Call the show function to display the UI
show()
