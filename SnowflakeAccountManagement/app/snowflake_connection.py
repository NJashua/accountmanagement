import streamlit as st

import snowflake.connector

def show():
    st.header("Snowflake Connection")

    user="NITHIN"
    password="Nj@9390779404"
    account="ngqvwsw-vc68866"
    if st.button("Connect"):
        try:
            conn=snowflake.connector.connect(
                user=user,
                password=password,
                account=account
            )
            st.success("Connected successfully:)")
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

def get_connection():
    user="NITHIN"
    password="Nj@9390779404"
    account="ngqvwsw-vc68866"

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account
    )
    return conn