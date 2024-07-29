import streamlit as st
from app.snowflake_connection import get_connection

def show():
    # Apply custom CSS styles
    st.markdown("""
        <style>
            /* Global styles */
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
            }
            .stApp {
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .stHeader {
                color: #FFFFFF;
                background-color: #6A1B9A; /* Purple */
                padding: 10px;
                border-radius: 12px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }
            .stSubheader {
                color: #4CAF50; /* Green */
            }
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
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
            }
            .user-management-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            .user-management-card {
                margin: 20px;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 300px;
            }
            .user-management-card:hover {
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("Role Management")

    def list_users():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SHOW USERS")
            users = cur.fetchall()
            conn.close()
            return [user[0] for user in users]
        except Exception as e:
            st.error(f"Error: {e}")
            return []

    def list_roles():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SHOW ROLES")
            roles = cur.fetchall()
            conn.close()
            return [role[1] for role in roles]
        except Exception as e:
            st.error(f"Error: {e}")
            return []

    def reset_password(username, new_password):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"ALTER USER {username} SET PASSWORD = '{new_password}'")
            conn.close()
            st.success(f"Password for user {username} reset successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def disable_user(username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"ALTER USER {username} DISABLE")
            conn.close()
            st.success(f"User {username} disabled successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def drop_user(username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"DROP USER {username}")
            conn.close()
            st.success(f"User {username} dropped successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def grant_role_to_user(role_name, username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"GRANT ROLE {role_name} TO USER {username}")
            conn.close()
            st.success(f"Role {role_name} granted to user {username} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def revoke_role_from_user(role_name, username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"REVOKE ROLE {role_name} FROM USER {username}")
            conn.close()
            st.success(f"Role {role_name} revoked from user {username} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Select User")
    users = list_users()
    selected_user = st.selectbox("Select User", users)

    if selected_user:
        st.subheader("Reset Password")
        new_password = st.text_input("New Password", type="password", key="reset_password")
        if st.button("Reset Password"):
            reset_password(selected_user, new_password)
        
        st.subheader("Disable User")
        if st.button("Disable User"):
            disable_user(selected_user)
        
        st.subheader("Drop User")
        if st.button("Drop User"):
            drop_user(selected_user)
        
        st.subheader("Grant a Role")
        roles = list_roles()
        role_name_grant = st.selectbox("Role Name to Grant", roles, key="grant_role_name")
        if st.button("Grant Role"):
            grant_role_to_user(role_name_grant, selected_user)
        
        st.subheader("Revoke a Role")
        role_name_revoke = st.selectbox("Role Name to Revoke", roles, key="revoke_role_name")
        if st.button("Revoke Role"):
            revoke_role_from_user(role_name_revoke, selected_user)

if __name__ == "__main__":
    show()
