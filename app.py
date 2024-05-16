import streamlit as st
import pandas as pd
import plotly.express as px
import math
import requests


# Lista específica de IDs
id_options_list = [
    'FOODS_3_090_CA_3_validation', 'FOODS_3_586_TX_2_validation', 'FOODS_3_586_TX_3_validation',
    'FOODS_3_586_CA_3_validation', 'FOODS_3_090_CA_1_validation', 'FOODS_3_090_WI_3_validation',
    'FOODS_3_090_TX_2_validation', 'FOODS_3_090_TX_3_validation', 'FOODS_3_252_TX_2_validation',
    'FOODS_3_586_TX_1_validation', 'FOODS_3_555_TX_2_validation', 'FOODS_3_090_TX_1_validation',
    'FOODS_3_120_CA_3_validation', 'FOODS_3_586_CA_1_validation', 'FOODS_3_252_TX_3_validation',
    'FOODS_3_586_WI_3_validation', 'FOODS_3_694_WI_3_validation', 'FOODS_3_252_CA_3_validation',
    'FOODS_3_541_CA_3_validation', 'FOODS_3_635_CA_3_validation', 'FOODS_3_226_WI_1_validation',
    'FOODS_3_555_TX_3_validation', 'FOODS_3_252_CA_1_validation', 'FOODS_3_377_TX_3_validation',
    'FOODS_3_808_CA_3_validation', 'FOODS_3_587_CA_3_validation', 'FOODS_3_226_WI_2_validation',
    'FOODS_3_555_TX_1_validation', 'FOODS_3_586_CA_2_validation', 'FOODS_3_377_TX_2_validation',
    'FOODS_3_120_CA_1_validation', 'FOODS_3_694_WI_2_validation', 'FOODS_3_555_CA_3_validation',
    'FOODS_3_555_WI_3_validation', 'FOODS_3_252_CA_2_validation', 'FOODS_3_252_TX_1_validation',
    'FOODS_3_090_CA_2_validation', 'FOODS_3_681_CA_3_validation', 'FOODS_3_318_WI_3_validation',
    'FOODS_3_714_WI_3_validation', 'FOODS_3_714_CA_1_validation', 'FOODS_3_090_CA_4_validation',
    'FOODS_3_007_WI_2_validation', 'FOODS_3_714_CA_3_validation', 'FOODS_3_587_CA_1_validation',
    'FOODS_3_202_CA_3_validation', 'FOODS_3_587_TX_2_validation', 'FOODS_3_234_WI_2_validation',
    'FOODS_3_607_CA_3_validation'
]

# Setting page configuration to use the full available width
st.set_page_config(layout="wide")

# Sidebar menu for page selection
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home"])

# File uploader for the main DataFrame
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Initialize merge_scaled_df as None
merge_scaled_df = None

# DataFrame acumulativo para almacenar las predicciones
if 'cumulative_predictions' not in st.session_state:
    st.session_state['cumulative_predictions'] = pd.DataFrame()

if uploaded_file is not None:
    # Load the DataFrame from the uploaded file
    merge_scaled_df = pd.read_csv(uploaded_file)



# Check if the DataFrame is loaded before proceeding
if merge_scaled_df is not None:

    # Helper function to extract categories and sum sales
    def get_category_sales(df):
        df['category'] = df['id'].apply(lambda x: x.split('_')[0])
        return df.groupby('category')['sales'].sum().reset_index()



    # Página principal
    if page == "Home":
        if merge_scaled_df is not None:
            st.title("Welcome to the M5 Forecasting System")
            st.markdown("### Our objective is to predict sales for the next 28 days using sales records from 2011-01-29 to 2016-06-19.")
            st.write(merge_scaled_df.head())   # Display the first few rows of the DataFrame

            st.markdown("### Now, we will use models to predict sales 28 days ahead.")

            # Dropdown box to select ID
            selected_id = st.selectbox("Select an ID for prediction", id_options_list)

            if st.button("Make Prediction", help="Make prediction using the API"):
                try:
                    # Hacer una solicitud GET a la API
                    api_url = f"https://walmart-lvvu2engva-ew.a.run.app/predict?id={selected_id}"
                    response = requests.get(api_url)
                    response.raise_for_status()  # Levanta una excepción para códigos de estado HTTP 4xx/5xx

                    # Parsear la respuesta JSON
                    simulated_response = response.json()

                    st.markdown(
                        f"""
                        <div style="text-align: center; font-size: 24px;">
                            <p><strong>Prediction made successfully!</strong></p>
                            <p>The best model was <strong>{simulated_response['model']}</strong>!</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Convertir las predicciones en un DataFrame
                    prediction_df = pd.DataFrame(list(simulated_response["prediction"].items()), columns=["date", "sales"])
                    prediction_df["date"] = pd.to_datetime(prediction_df["date"])
                    prediction_df["id"] = simulated_response["id"]
                    prediction_df["type"] = "Prediction"

                    # Convertir los datos reales en un DataFrame
                    actual_dates = list(simulated_response["prediction"].keys())  # Usar las mismas fechas que en predicciones
                    actual_sales = list(simulated_response["actual"].values())
                    actual_df = pd.DataFrame({"date": actual_dates, "sales": actual_sales})
                    actual_df["date"] = pd.to_datetime(actual_df["date"])
                    actual_df["id"] = simulated_response["id"]
                    actual_df["type"] = "Actual"

                    # Convertir los datos históricos en un DataFrame
                    history_df = pd.DataFrame(list(simulated_response["history"].items()), columns=["date", "sales"])
                    history_df["date"] = pd.to_datetime(history_df["date"])
                    history_df["id"] = simulated_response["id"]
                    history_df["type"] = "History"

                    # Combinar todos los DataFrames
                    combined_df = pd.concat([prediction_df, actual_df, history_df])

                    # Mostrar el DataFrame de predicciones sin la columna 'type' y con las columnas en el orden especificado
                    st.write("Predictions DataFrame:")
                    st.write(prediction_df[["date", "id", "sales"]])

                    # Graficar la evolución de las ventas con color específico para las predicciones
                    fig = px.line(combined_df, x="date", y="sales", color="type", title=f"Sales Forecast for {selected_id} Over 28 Days",
                                labels={"sales": "Sales", "date": "Date"},
                                color_discrete_map={
                                    "Prediction": "green",
                                    "Actual": "red",
                                    "History": "skyblue"
                                })
                    fig.update_layout(
                        autosize=False,
                        width=1800,
                        height=600,
                        margin=dict(l=50, r=50, b=100, t=100, pad=4)
                    )
                    st.plotly_chart(fig)

                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred while making the API request: {e}")
                except KeyError as e:
                    st.error(f"An error occurred while processing the API response: {e}")

        else:
            st.title("Welcome to the M5 Forecasting System")
            st.markdown("### To get started, please upload a .csv file with your historical sales data.")

    # Prediction Analysis Page
    elif page == "Prediction Analysis":
        st.title("Prediction Analysis")

        # Check if there are any predictions made
        if not st.session_state['cumulative_predictions'].empty:
            st.write("Cumulative Predictions Dataset:")
            st.write(st.session_state['cumulative_predictions'])

            # Total Sales by ID Bar Chart
            st.markdown("### Total Sales by ID")
            cumulative_predictions_melted = st.session_state['cumulative_predictions'].melt(id_vars=["ID"], var_name="Day", value_name="Sales")
            total_sales_by_id = cumulative_predictions_melted.groupby("ID")["Sales"].sum().reset_index()
            fig_bar_total_sales = px.bar(total_sales_by_id, x="ID", y="Sales", title="Total Sales by ID", labels={"Sales": "Total Sales", "ID": "ID"})
            st.plotly_chart(fig_bar_total_sales, use_container_width=True)

            # Sales Evolution Line Chart
            st.markdown("### Sales Evolution Over 28 Days")
            fig_line_sales_evolution = px.line(cumulative_predictions_melted, x="Day", y="Sales", color="ID", title="Sales Evolution Over 28 Days", labels={"Sales": "Sales", "Day": "Day"})
            st.plotly_chart(fig_line_sales_evolution, use_container_width=True)
        else:
            st.write("No predictions made yet.")

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


    # Página de interpretación
    elif page == "Interpretation":
        st.title("Interpretation")

        if merge_scaled_df is not None and 'cumulative_predictions' in st.session_state:
            st.write("Dataset loaded successfully.")

            # Convertir la columna 'date' a tipo datetime en el DataFrame original
            st.write("Converting 'date' column in the original dataset to datetime type.")
            try:
                merge_scaled_df['date'] = pd.to_datetime(merge_scaled_df['date'])
                st.write("Conversion complete.")
            except Exception as e:
                st.write(f"Error converting 'date' column in the original dataset: {e}")

            # Mostrar las primeras filas del dataset para confirmar que está cargado
            st.write("Displaying the first few rows of the dataset:")
            st.write(merge_scaled_df.head())

            # Dropdown para seleccionar el ID del producto
            st.write("Creating dropdown for Product ID selection.")
            id_options = st.session_state['cumulative_predictions']['id'].unique().tolist()
            selected_id = st.selectbox("Select a Product ID for Interpretation", id_options)
            st.write(f"Selected Product ID: {selected_id}")

            # Filtrar el DataFrame original por el ID seleccionado
            original_filtered_df = merge_scaled_df[merge_scaled_df['id'] == selected_id]

            # Obtener el DataFrame de predicciones desde session_state y filtrar por el ID seleccionado
            predictions_df = st.session_state['cumulative_predictions'][st.session_state['cumulative_predictions']['id'] == selected_id].reset_index()

            # Verificar si el DataFrame de predicciones tiene la columna 'date'
            if 'date' not in predictions_df.columns:
                st.write("Error: 'date' column not found in predictions DataFrame")
            else:
                # Asegurarse de que las fechas en ambos DataFrames son del mismo tipo y formato
                try:
                    predictions_df['date'] = pd.to_datetime(predictions_df['date'])
                except Exception as e:
                    st.write(f"Error converting 'date' column in predictions DataFrame: {e}")

                # Unir el DataFrame de predicciones con el DataFrame original usando pd.concat
                combined_df = pd.concat([merge_scaled_df, predictions_df], ignore_index=True)

                # Mostrar las primeras filas del DataFrame combinado para verificación
                st.write("Displaying the first few rows of the combined DataFrame:")
                st.write(combined_df.head())

                # Filtrar datos para obtener las ventas totales en los últimos 28 días
                current_date = combined_df['date'].max()
                start_date_recent = current_date - pd.DateOffset(days=28)
                recent_sales = combined_df[(combined_df['date'] >= start_date_recent) & (combined_df['date'] <= current_date) & (combined_df['id'] == selected_id)]['sales'].sum()

                # Crear un DataFrame para visualización de las ventas recientes
                recent_sales_df = pd.DataFrame({'Date Interval': [f'{start_date_recent.strftime("%Y-%m-%d")} - {current_date.strftime("%Y-%m-%d")}'], 'Total Sales': [recent_sales]})

                # Filtrar datos para obtener las ventas totales de los 12 periodos anteriores de 28 días
                historical_sales = []
                for i in range(12):
                    start_date_historical = current_date - pd.DateOffset(days=28 * (i + 2))  # Retrocede 28 días adicionales para cada periodo
                    end_date_historical = current_date - pd.DateOffset(days=28 * (i + 1))
                    sales_historical = combined_df[(combined_df['date'] >= start_date_historical) & (combined_df['date'] <= end_date_historical) & (combined_df['id'] == selected_id)]['sales'].sum()
                    historical_sales.append(sales_historical)

                # Crear un DataFrame para visualización de las ventas históricas
                historical_sales_df = pd.DataFrame({'Historical Period': [f'Period-{i+1}' for i in range(12)], 'Total Sales': historical_sales})

                # Crear un gráfico de barras para representar las ventas totales en los últimos 28 días y en periodos históricos
                fig_sales = px.bar(recent_sales_df, x='Date Interval', y='Total Sales', title=f'Sales for Last 28 Days for Product ID: {selected_id}',
                                    labels={'Total Sales': 'Total Sales', 'Date Interval': 'Date Interval'})
                fig_sales.add_bar(x=historical_sales_df['Historical Period'], y=historical_sales_df['Total Sales'], name='Historical Sales')

                # Personalizar la disposición del gráfico
                fig_sales.update_layout(xaxis_title='Date Interval', yaxis_title='Total Sales')

                # Mostrar el gráfico de barras
                st.plotly_chart(fig_sales, use_container_width=True)
        else:
            st.write("Please upload a CSV file and make predictions to proceed.")

