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
        df = pd.DataFrame(users, columns=column_names)

        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def show():
    st.header("User Management")

    def create_user(username, password):
        try:
            conn = get_connection()
            cur = conn.cursor()
            query = f"CREATE USER {username} PASSWORD = '{password}'"
            cur.execute(query)
            conn.close()
            st.success(f"User {username} created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create User")
    new_username = st.text_input("New Username", key="new_username_input_unique")
    new_password = st.text_input("New Password", type="password", key="new_password_input_unique")
    if st.button("Create User", key="create_user_btn_unique"):
        if new_username and new_password:
            create_user(new_username, new_password)
        else:
            st.error("Please provide both username and password.")

    st.subheader("Existing Users")
    users_df = list_users()
    if users_df is not None:
        st.table(users_df)
    else:
        st.write("No users found or error in fetching users.")

show()
