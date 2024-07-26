import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import snowflake.connector
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide", initial_sidebar_state="collapsed")

# plt.style.use('seaborn-whitegrid')
# sns.set_theme(style="whitegrid")

def get_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            user='NITHIN',
            password='Nj@9390779404',
            account='ctkbbdn-xc60080',
            warehouse='COMPUTE_WH',
            database='customer_analysis_db',
            schema='customer_analysis_schema'
        )
        st.write("Connected to Snowflake successfully..:)!")
        return conn
    except snowflake.connector.errors.OperationalError as e:
        st.error(f"Operational error: {e}")
    except snowflake.connector.errors.ProgrammingError as e:
        st.error(f"Programming error: {e}")

def fetch_data_from_snowflake():
    conn = get_snowflake_connection()
    if conn:
        query = """
        SELECT 
            CATEGORY, 
            PAYMENT_METHOD, 
            TRANSACTION_DATE, 
            AMOUNT, 
            QUANTITY, 
            STORE,
            GENDER
        FROM 
            CUSTOMER_DATA
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()

df = fetch_data_from_snowflake()

if not df.empty:
    st.title("Customerz Sales Dashboard")

    df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'])
    df['YEAR'] = df['TRANSACTION_DATE'].dt.year

    year = st.selectbox("Select Year", df['YEAR'].unique())

    df_year = df[df['YEAR'] == year]

    total_sales = df_year['AMOUNT'].sum()
    total_profit = (df_year['AMOUNT'] * 0.2).sum()
    total_orders = len(df_year)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric("Orders", total_orders)

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Top 10 Selling Products")
        top_selling_products = df_year.groupby('CATEGORY')['QUANTITY'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(x=top_selling_products.values, y=top_selling_products.index, palette="viridis", ax=ax)
        ax.set_xlabel("Sum of Sales")
        st.pyplot(fig)

    with col5:
        st.subheader("Top 10 Most Profitable Products")
        top_profitable_products = df_year.groupby('CATEGORY')['AMOUNT'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(x=top_profitable_products.values, y=top_profitable_products.index, palette="viridis", ax=ax)
        ax.set_xlabel("Sum of Profit")
        st.pyplot(fig)

    col6, col7 = st.columns(2)

    # with col6:
    #     st.subheader("Average Time Between Orders (Days)")
    #     df_year = df_year.sort_values('TRANSACTION_DATE')
    #     df_year['PREV_DATE'] = df_year['TRANSACTION_DATE'].shift(1)
    #     df_year['DAYS_BETWEEN'] = (df_year['TRANSACTION_DATE'] - df_year['PREV_DATE']).dt.days
    #     average_days_between_orders = df_year['DAYS_BETWEEN'].mean()
    #     st.metric("Average Days Between Orders", f"{average_days_between_orders:.2f} days")

    with col7:
        st.subheader("Sales Trends for Product Categories over the Years")
        category_sales = df.groupby(['YEAR', 'CATEGORY'])['AMOUNT'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x='YEAR', y='AMOUNT', hue='CATEGORY', data=category_sales, palette="viridis", ax=ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Sum of Sales")
        st.pyplot(fig)

    st.subheader("Future Sales and Revenue Prediction")

    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    prediction_pipeline = pipeline('text-classification', model=model, tokenizer=tokenizer)

    future_sales_predictions = {}
    future_revenue_predictions = {}

    for category in df['CATEGORY'].unique():
        category_data = df[df['CATEGORY'] == category]['AMOUNT'].sum()
        future_sales = prediction_pipeline(f"Future sales prediction for category {category}")
        future_revenue = future_sales[0]['score'] * category_data
        
        future_sales_predictions[category] = future_sales[0]['score'] * category_data
        future_revenue_predictions[category] = future_revenue

    st.write("Future Sales Predictions:")
    st.write(future_sales_predictions)

    st.write("Future Revenue Predictions:")
    st.write(future_revenue_predictions)

    future_sales_df = pd.DataFrame(list(future_sales_predictions.items()), columns=['Category', 'Predicted Sales'])
    future_revenue_df = pd.DataFrame(list(future_revenue_predictions.items()), columns=['Category', 'Predicted Revenue'])

    col8, col9 = st.columns(2)

    with col8:
        st.subheader("Predicted Sales by Category")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(x='Predicted Sales', y='Category', data=future_sales_df, palette="viridis", ax=ax)
        ax.set_xlabel("Predicted Sales")
        st.pyplot(fig)

    with col9:
        st.subheader("Predicted Revenue by Category")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(x='Predicted Revenue', y='Category', data=future_revenue_df, palette="viridis", ax=ax)
        ax.set_xlabel("Predicted Revenue")
        st.pyplot(fig)

else:
    st.error("Failed to load data from Snowflake.")
