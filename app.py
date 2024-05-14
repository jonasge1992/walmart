import streamlit as st
import pandas as pd
import plotly.express as px
import math
# Configuración de la página para usar todo el ancho disponible
st.set_page_config(layout="wide")

# Menú en la barra lateral para selección de la página
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Forecasting", "Sales Analysis", "Product Analysis", "Interpretation"])

# Cargar el DataFrame principal para las demás páginas
merge_scaled_df = pd.read_csv("raw_data/merge_df_scaled.csv")

# Función auxiliar para extraer categorías y sumar ventas
def get_category_sales(df):
    df['category'] = df['id'].apply(lambda x: x.split('_')[0])
    return df.groupby('category')['sales'].sum().reset_index()

# Página Principal
if page == "Home":
    st.title("Welcome to the M5 Forecasting System")
    st.markdown("### Our objective is to predict sales for the next 28 days using sales records from 2011-01-29 to 2016-06-19.")
    data = pd.read_csv("raw_data/merge_df_scaled.csv")
    st.write(data.head())  # Muestra las primeras filas del DataFrame

    st.markdown("### Now, we will use the ARIMA model to predict sales 28 days ahead.")
    if st.button("Make Prediction", help="Make prediction using ARIMA model"):
        # Aquí irá el código para realizar la predicción con ARIMA
        st.write("Prediction made successfully!")
# Visión General de los Datos
elif page == "Forecasting":
    st.title("Forecasting")
    st.markdown("### Behold the sales forecast for the next 28 days ")
    st.write(merge_scaled_df.head())
    st.write("The WRMSSE has a value of: ")
    st.write("The RMSE has a value of: ")


# Análisis de Ventas por Categoría
elif page == "Sales Analysis":
    st.title("Sales Analysis")

    # Gráfico de ventas totales por categoría
    st.markdown("### Total Sales by Category")
    category_sales = get_category_sales(merge_scaled_df)
    fig_bar = px.bar(category_sales, x='category', y='sales', title='Sales by Category', labels={'sales': 'Total Sales', 'category': 'Category'})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de ventas de los últimos 28 días
    st.markdown("### Sales for the Last 28 Days")
    # Filtrar los datos para obtener solo los últimos 28 días
    last_28_days_sales = merge_scaled_df.groupby('date')['sales'].sum().reset_index().tail(28)
    fig_last_28_days = px.line(last_28_days_sales, x='date', y='sales', title='Sales for the Last 28 Days', labels={'sales': 'Total Sales', 'date': 'Date'})
    st.plotly_chart(fig_last_28_days, use_container_width=True)

    # Histograma de ventas diarias durante los últimos 28 días
    fig_daily_sales_histogram = px.histogram(last_28_days_sales, x='date', y='sales', title='Daily Sales Histogram for the Last 28 Days', labels={'sales': 'Total Sales', 'date': 'Date'})
    st.plotly_chart(fig_daily_sales_histogram, use_container_width=True)

    # Gráfico de ventas por categoría
    st.markdown("### Sales by Category")
    fig_pie = px.pie(category_sales, values='sales', names='category', title='Percentage of Sales by Category')
    st.plotly_chart(fig_pie, use_container_width=True)

# Análisis de Productos
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


elif page == "Interpretation":
    st.title("Interpretation")
    st.write("HERE WE WILL PUT A MERGED DATASET WITH THE 28 DAYS")

    # Convertir la columna 'date' a tipo datetime
    merge_scaled_df['date'] = pd.to_datetime(merge_scaled_df['date'])

    # Obtener la fecha más reciente en los datos
    current_date = merge_scaled_df['date'].max()
    # Calcular la fecha hace 12 meses
    one_year_ago_date = current_date - pd.DateOffset(days=28 * 12)

    # Filtrar los datos para los últimos 12 periodos de 28 días
    last_12_intervals_data = merge_scaled_df[(merge_scaled_df['date'] >= one_year_ago_date) & (merge_scaled_df['date'] <= current_date)]

    # Crear un nuevo DataFrame para almacenar las fechas y las ventas en intervalos de 28 días
    sales_28_days = pd.DataFrame(columns=['Date', 'Sales'])

    # Iterar sobre los periodos de 28 días y calcular las ventas
    for i in range(12):
        start_date = current_date - pd.DateOffset(days=28 * (i + 1))
        end_date = current_date - pd.DateOffset(days=28 * i)
        sales_in_interval = merge_scaled_df[(merge_scaled_df['date'] >= start_date) & (merge_scaled_df['date'] <= end_date)]['sales'].sum()
        sales_28_days = pd.concat([sales_28_days, pd.DataFrame({'Date': [f'{start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")}'], 'Sales': [sales_in_interval]})], ignore_index=True)

    # Calcular las variaciones entre intervalos
    variation_last_interval = sales_28_days['Sales'].iloc[-1] - sales_28_days['Sales'].iloc[-2]
    variation_3_intervals = sales_28_days['Sales'].iloc[-1] - sales_28_days['Sales'].iloc[-4]
    variation_6_intervals = sales_28_days['Sales'].iloc[-1] - sales_28_days['Sales'].iloc[-7]

    # Calcular las variaciones porcentuales
    percentage_variation_last_interval = (variation_last_interval / sales_28_days['Sales'].iloc[-2]) * 100
    percentage_variation_3_intervals = (variation_3_intervals / sales_28_days['Sales'].iloc[-4]) * 100
    percentage_variation_6_intervals = (variation_6_intervals / sales_28_days['Sales'].iloc[-7]) * 100

    # Mostrar las variaciones
    st.write(f"Variation with respect to the last interval (Absolute): {variation_last_interval}")
    st.write(f"Variation with respect to the last interval (Percentage): {percentage_variation_last_interval}%")
    st.write(f"Variation with respect to every 3 intervals (Absolute): {variation_3_intervals}")
    st.write(f"Variation with respect to every 3 intervals (Percentage): {percentage_variation_3_intervals}%")
    st.write(f"Variation with respect to every 6 intervals (Absolute): {variation_6_intervals}")
    st.write(f"Variation with respect to every 6 intervals (Percentage): {percentage_variation_6_intervals}%")

    # Crear un gráfico de barras para representar las ventas acumuladas cada 28 días
    fig_histogram = px.bar(sales_28_days, x='Date', y='Sales', title='Total Sales in 28-Day Intervals',
                           labels={'Sales': 'Total Sales', 'Date': 'Date Interval'})

    # Personalizar el diseño del histograma
    fig_histogram.update_layout(xaxis_title='Date Interval', yaxis_title='Total Sales')

    # Mostrar el gráfico de barras
    st.plotly_chart(fig_histogram, use_container_width=True)
