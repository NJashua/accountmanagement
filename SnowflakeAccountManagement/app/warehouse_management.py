import streamlit as st
from app.snowflake_connection import get_connection

def show():
    st.markdown("""
        <style>
            .stApp {
                padding: 20px;
                font-family: 'Arial', sans-serif;
            }
            .stHeader, .stSubheader {
                color: #000000; /* Black color for text */
                text-align: center;
                margin-bottom: 20px;
            }
            .stButton>button {
                background-color: #2ecc71; /* Green background */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
                margin: 10px 0;
                cursor: pointer;
                transition-duration: 0.4s;
            }
            .stButton>button:hover {
                background-color: #27ae60; /* Darker green on hover */
                color: white;
            }
            .stSelectbox, .stTextInput, .stTextArea {
                margin-bottom: 20px;
            }
            .stTextInput>input {
                border: 1px solid #ddd; /* Light border */
                border-radius: 4px;
                padding: 10px;
                background-color: yellow; /* Light gray background */
                color: #000; /* Black text */
            }
            .stNumberInput>input {
                border: 1px solid #ddd; /* Light border */
                border-radius: 4px;
                padding: 10px;
                background-color: #f9f9f9; /* Light gray background */
                color: #000; /* Black text */
            }
            .stCheckbox>label {
                color: #000000; /* Black color for labels */
            }
            .stSelectbox>select {
                border: 1px solid #ddd; /* Light border */
                border-radius: 4px;
                padding: 10px;
                background-color: #f9f9f9; /* Light gray background */
                color: #000; /* Black text */
            }
        </style>
    """, unsafe_allow_html=True)

    st.header("Warehouse Management")

    def create_warehouse(warehouse_name, auto_resume, auto_suspend, multi_cluster, query_acceleration):
        try:
            conn = get_connection()
            cur = conn.cursor()
            options = []
            if auto_resume:
                options.append("AUTO_RESUME = TRUE")
            else:
                options.append("AUTO_RESUME = FALSE")
            if auto_suspend:
                options.append(f"AUTO_SUSPEND = {auto_suspend}")
            if multi_cluster:
                options.append("MAX_CLUSTER_COUNT = 1")
            else:
                options.append("MAX_CLUSTER_COUNT = 1")
            if query_acceleration:
                options.append("QUERY_ACCELERATION = TRUE")
            else:
                options.append("QUERY_ACCELERATION = FALSE")
            options_str = ", ".join(options)
            cur.execute(f"CREATE WAREHOUSE {warehouse_name} WITH {options_str}")
            conn.close()
            st.success(f"Warehouse {warehouse_name} created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def edit_warehouse(warehouse_name, auto_resume, auto_suspend, multi_cluster, query_acceleration):
        try:
            conn = get_connection()
            cur = conn.cursor()
            options = []
            if auto_resume is not None:
                options.append(f"AUTO_RESUME = {auto_resume}")
            if auto_suspend is not None:
                options.append(f"AUTO_SUSPEND = {auto_suspend}")
            if multi_cluster is not None:
                options.append(f"MAX_CLUSTER_COUNT = {multi_cluster}")
            if query_acceleration is not None:
                options.append(f"QUERY_ACCELERATION = {query_acceleration}")
            options_str = ", ".join(options)
            cur.execute(f"ALTER WAREHOUSE {warehouse_name} SET {options_str}")
            conn.close()
            st.success(f"Warehouse {warehouse_name} edited successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def resume_warehouse(warehouse_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"ALTER WAREHOUSE {warehouse_name} RESUME")
            conn.close()
            st.success(f"Warehouse {warehouse_name} resumed successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def drop_warehouse(warehouse_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"DROP WAREHOUSE {warehouse_name}")
            conn.close()
            st.success(f"Warehouse {warehouse_name} dropped successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def transfer_ownership(warehouse_name, new_owner_role):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(f"REVOKE USAGE ON WAREHOUSE {warehouse_name} FROM ROLE {new_owner_role}")
            cur.execute(f"GRANT OWNERSHIP ON WAREHOUSE {warehouse_name} TO ROLE {new_owner_role}")
            cur.execute(f"GRANT USAGE ON WAREHOUSE {warehouse_name} TO ROLE {new_owner_role}")
            conn.close()
            st.success(f"Ownership of warehouse {warehouse_name} transferred to {new_owner_role} successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

    def list_warehouses():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SHOW WAREHOUSES")
            warehouses = cur.fetchall()
            conn.close()
            return [wh[0] for wh in warehouses]  # Extracting warehouse names
        except Exception as e:
            st.error(f"Error: {e}")
            return []

    st.subheader("Create Warehouse")
    warehouse_name_create = st.text_input("Warehouse Name to Create")
    auto_resume_create = st.checkbox("Auto Resume", value=True)
    auto_suspend_create = st.number_input("Auto Suspend (minutes)", min_value=1, value=5, key="auto_suspend_create")
    multi_cluster_create = st.checkbox("Multi Cluster", value=False)
    query_acceleration_create = st.checkbox("Query Acceleration", value=False)
    if st.button("Create Warehouse", key="create_warehouse_button"):
        create_warehouse(warehouse_name_create, auto_resume_create, auto_suspend_create, multi_cluster_create, query_acceleration_create)

    st.subheader("Edit Warehouse")
    warehouses = list_warehouses()
    warehouse_name_edit = st.selectbox("Select Warehouse to Edit", warehouses)
    auto_resume_edit = st.checkbox("Auto Resume (check for ON)", value=True, key="auto_resume_edit")
    auto_suspend_edit = st.number_input("Auto Suspend (minutes)", min_value=1, value=5, key="auto_suspend_edit")
    multi_cluster_edit = st.checkbox("Multi Cluster (check for ON)", value=False, key="multi_cluster_edit")
    query_acceleration_edit = st.checkbox("Query Acceleration (check for ON)", value=False, key="query_acceleration_edit")
    if st.button("Edit Warehouse", key="edit_warehouse_button"):
        edit_warehouse(warehouse_name_edit, auto_resume_edit, auto_suspend_edit, multi_cluster_edit, query_acceleration_edit)

    st.subheader("Resume Warehouse")
    warehouse_name_resume = st.selectbox("Select Warehouse to Resume", warehouses, key="resume_warehouse_selectbox")
    if st.button("Resume Warehouse", key="resume_warehouse_button"):
        resume_warehouse(warehouse_name_resume)

    st.subheader("Drop Warehouse")
    warehouse_name_drop = st.selectbox("Select Warehouse to Drop", warehouses, key="drop_warehouse_selectbox")
    if st.button("Drop Warehouse", key="drop_warehouse_button"):
        drop_warehouse(warehouse_name_drop)

    st.subheader("Transfer Ownership")
    warehouse_name_ownership = st.selectbox("Select Warehouse to Transfer Ownership", warehouses, key="ownership_warehouse_selectbox")
    new_owner_role = st.text_input("New Owner Role", key="new_owner_role")
    if st.button("Transfer Ownership", key="transfer_ownership_button"):
        transfer_ownership(warehouse_name_ownership, new_owner_role)
