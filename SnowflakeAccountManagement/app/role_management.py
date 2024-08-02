import streamlit as st

from app.snowflake_connection import get_connection

def show():
    st.markdown("""
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: black;
            }
            # .stApp {
            #     max-width: 800px;
            #     margin: 40px auto;
            #     padding: 20px;
            #     background-color: #fff;
            #     border: 1px solid #ddd;
            #     border-radius: 10px;
            #     box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            # }
            .stHeader {
                color: #FFFFFF;
                background-color: #6A1B9A;
                padding: 10px;
                border-radius: 12px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }
            .stSubheader {
                color: #4CAF50;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 24px;
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

    def execute_query(query, success_message):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query)
            conn.close()
            st.success(success_message)
        except Exception as e:
            st.error(f"Error: {e}")

    users = list_users()
    selected_user = st.selectbox("Select User", users)

    if selected_user:
        st.subheader("Actions for User")
        new_password = st.text_input("New Password", type="password")
        if st.button("Reset Password"):
            execute_query(f"ALTER USER {selected_user} SET PASSWORD = '{new_password}'", f"Password for user {selected_user} reset successfully!")

        if st.button("Disable User"):
            execute_query(f"ALTER USER {selected_user} DISABLE", f"User {selected_user} disabled successfully!")

        if st.button("Drop User"):
            execute_query(f"DROP USER {selected_user}", f"User {selected_user} dropped successfully!")

        roles = list_roles()
        role_name_grant = st.selectbox("Role Name to Grant", roles, key="grant_role_name")
        if st.button("Grant Role"):
            execute_query(f"GRANT ROLE {role_name_grant} TO USER {selected_user}", f"Role {role_name_grant} granted to user {selected_user} successfully!")

        role_name_revoke = st.selectbox("Role Name to Revoke", roles, key="revoke_role_name")
        if st.button("Revoke Role"):
            execute_query(f"REVOKE ROLE {role_name_revoke} FROM USER {selected_user}", f"Role {role_name_revoke} revoked from user {selected_user} successfully!")

if __name__ == "__main__":
    show()