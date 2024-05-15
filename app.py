import streamlit as st
import pandas as pd
import plotly.express as px
import math
# Setting page configuration to use the full available width
st.set_page_config(layout="wide")

# Sidebar menu for page selection
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Forecasting", "Sales Analysis", "Product Analysis", "Interpretation"])

# Load the main DataFrame for other pages
merge_scaled_df = pd.read_csv("raw_data/merge_df_scaled.csv")

# Helper function to extract categories and sum sales
def get_category_sales(df):
    df['category'] = df['id'].apply(lambda x: x.split('_')[0])
    return df.groupby('category')['sales'].sum().reset_index()

# Home Page
if page == "Home":
    st.title("Welcome to the M5 Forecasting System")
    st.markdown("### Our objective is to predict sales for the next 28 days using sales records from 2011-01-29 to 2016-06-19.")
    data = pd.read_csv("raw_data/merge_df_scaled.csv")
    st.write(data.head())   # Display the first few rows of the DataFrame

    st.markdown("### Now, we will use the ARIMA model to predict sales 28 days ahead.")
    if st.button("Make Prediction", help="Make prediction using ARIMA model"):
        # Here goes the code to perform prediction with ARIMA
        st.write("Prediction made successfully!")
# Forecasting Page
elif page == "Forecasting":
    st.title("Forecasting")
    st.markdown("### Behold the sales forecast for the next 28 days ")
    st.write(merge_scaled_df.head())
    st.write("The WRMSSE has a value of: ")
    st.write("The RMSE has a value of: ")


# Sales Analysis Page
elif page == "Sales Analysis":
    st.title("Sales Analysis")

    # Total Sales by Category Bar Chart
    st.markdown("### Total Sales by Category")
    category_sales = get_category_sales(merge_scaled_df)
    fig_bar = px.bar(category_sales, x='category', y='sales', title='Sales by Category', labels={'sales': 'Total Sales', 'category': 'Category'})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Sales for the Last 28 Days Line Chart
    st.markdown("### Sales for the Last 28 Days")
    last_28_days_sales = merge_scaled_df.groupby('date')['sales'].sum().reset_index().tail(28)
    fig_last_28_days = px.line(last_28_days_sales, x='date', y='sales', title='Sales for the Last 28 Days', labels={'sales': 'Total Sales', 'date': 'Date'})
    st.plotly_chart(fig_last_28_days, use_container_width=True)

    # Daily Sales Histogram for the Last 28 Days
    fig_daily_sales_histogram = px.histogram(last_28_days_sales, x='date', y='sales', title='Daily Sales Histogram for the Last 28 Days', labels={'sales': 'Total Sales', 'date': 'Date'})
    st.plotly_chart(fig_daily_sales_histogram, use_container_width=True)

    # Sales by Category Pie Chart
    st.markdown("### Sales by Category")
    fig_pie = px.pie(category_sales, values='sales', names='category', title='Percentage of Sales by Category')
    st.plotly_chart(fig_pie, use_container_width=True)

# Product Analysis Page
elif page == "Product Analysis":
    st.title("Product Analysis")

    product_ids = merge_scaled_df['id'].unique()
    selected_product_ids = st.multiselect("Select Product IDs", product_ids)

    if selected_product_ids:
        filtered_df = merge_scaled_df[
            merge_scaled_df['id'].isin(selected_product_ids)
        ]

        if not filtered_df.empty:
            product_sales = filtered_df.groupby('id')['sales'].sum().reset_index()
            fig = px.bar(product_sales, x='id', y='sales', title='Total Sales by Selected Products', labels={'sales': 'Total Sales', 'id': 'Product ID'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No rows matching the selected filters.")
    else:
        st.write("Select product filters to view data.")

# Interpretation Page
elif page == "Interpretation":
    st.title("Interpretation")
    st.write("HERE WE WILL PUT A MERGED DATASET WITH THE 28 DAYS")

    # Convert the 'date' column to datetime type
    merge_scaled_df['date'] = pd.to_datetime(merge_scaled_df['date'])

    # Get the most recent date in the data
    current_date = merge_scaled_df['date'].max()
    # Calculate the date 12 months ago
    one_year_ago_date = current_date - pd.DateOffset(days=28 * 12)

    # Filter the data for the last 12 periods of 28 days
    last_12_intervals_data = merge_scaled_df[(merge_scaled_df['date'] >= one_year_ago_date) & (merge_scaled_df['date'] <= current_date)]

    # Create a new DataFrame to store dates and sales in 28-day intervals
    sales_28_days = pd.DataFrame(columns=['Date', 'Sales'])

    for i in range(12):
        start_date = current_date - pd.DateOffset(days=28 * (i + 1))
        end_date = current_date - pd.DateOffset(days=28 * i)
        sales_in_interval = merge_scaled_df[(merge_scaled_df['date'] >= start_date) & (merge_scaled_df['date'] <= end_date)]['sales'].sum()
        sales_28_days = pd.concat([sales_28_days, pd.DataFrame({'Date': [f'{start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")}'], 'Sales': [sales_in_interval]})], ignore_index=True)

    # Reverse the order of the DataFrame
    sales_28_days = sales_28_days.iloc[::-1]

    # Calculate variations between intervals
    variation_last_interval = sales_28_days['Sales'].iloc[-1] - sales_28_days['Sales'].iloc[-2]
    variation_3_intervals = sales_28_days['Sales'].iloc[-1] - sales_28_days['Sales'].iloc[-4]
    variation_6_intervals = sales_28_days['Sales'].iloc[-1] - sales_28_days['Sales'].iloc[-7]

    # Calculate percentage variations
    percentage_variation_last_interval = (variation_last_interval / sales_28_days['Sales'].iloc[-2]) * 100
    percentage_variation_3_intervals = (variation_3_intervals / sales_28_days['Sales'].iloc[-4]) * 100
    percentage_variation_6_intervals = (variation_6_intervals / sales_28_days['Sales'].iloc[-7]) * 100

    # Display variations
    st.write(f"Variation with respect to the last interval (Absolute): {variation_last_interval}")
    st.write(f"Variation with respect to the last interval (Percentage): {percentage_variation_last_interval}%")
    st.write(f"Variation with respect to every 3 intervals (Absolute): {variation_3_intervals}")
    st.write(f"Variation with respect to every 3 intervals (Percentage): {percentage_variation_3_intervals}%")
    st.write(f"Variation with respect to every 6 intervals (Absolute): {variation_6_intervals}")
    st.write(f"Variation with respect to every 6 intervals (Percentage): {percentage_variation_6_intervals}%")

    # Create a bar chart to represent total sales in 28-day intervals
    fig_histogram = px.bar(sales_28_days, x='Date', y='Sales', title='Total Sales in 28-Day Intervals',
                           labels={'Sales': 'Total Sales', 'Date': 'Date Interval'})

    # Customize the histogram layout
    fig_histogram.update_layout(xaxis_title='Date Interval', yaxis_title='Total Sales')

    # Display the bar chart
    st.plotly_chart(fig_histogram, use_container_width=True)
