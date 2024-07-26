import snowflake.connector

def test_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            user='NITHIN',
            password='Nj@9390779404',
            account='ctkbbdn-xc60080',
            warehouse='COMPUTE_WH',
            database='customer_analysis_db',
            schema='customer_analysis_schema'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP")
        result = cursor.fetchone()
        print("Connected to Snowflake successfully!")
        print("Current Timestamp:", result[0])
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")

if __name__ == "__main__":
    test_snowflake_connection()
