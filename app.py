import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Dictionary mapping visible names to corresponding IDs
id_to_name_map = {
    'FOODS_3_090_CA_3_validation': 'Bananas 1kg',
    'FOODS_3_586_TX_2_validation': 'Apples Pack of 6',
    'FOODS_3_586_TX_3_validation': 'Chicken Breast 500g',
    'FOODS_3_586_CA_3_validation': 'Avocados Pack of 4',
    'FOODS_3_090_CA_1_validation': 'Ground Beef 1kg',
    'FOODS_3_090_WI_3_validation': 'Oranges 1kg',
    'FOODS_3_090_TX_2_validation': 'Broccoli 500g',
    'FOODS_3_090_TX_3_validation': 'Eggs Pack of 12',
    'FOODS_3_252_TX_2_validation': 'Carrots 1kg',
    'FOODS_3_586_TX_1_validation': 'Salmon Fillet 500g',
    'FOODS_3_555_TX_2_validation': 'Grapes 1kg',
    'FOODS_3_090_TX_1_validation': 'Lettuce Pack of 2',
    'FOODS_3_120_CA_3_validation': 'Milk 1L',
    'FOODS_3_586_CA_1_validation': 'Pork Chops 500g',
    'FOODS_3_252_TX_3_validation': 'Potatoes 2kg',
    'FOODS_3_586_WI_3_validation': 'Tomatoes 1kg',
    'FOODS_3_694_WI_3_validation': 'Zucchini 500g',
    'FOODS_3_252_CA_3_validation': 'Cucumbers Pack of 3',
    'FOODS_3_541_CA_3_validation': 'Turkey Breast 500g',
    'FOODS_3_635_CA_3_validation': 'Peaches Pack of 6',
    'FOODS_3_226_WI_1_validation': 'Plums Pack of 6',
    'FOODS_3_555_TX_3_validation': 'Strawberries 500g',
    'FOODS_3_252_CA_1_validation': 'Watermelons 1 unit',
    'FOODS_3_377_TX_3_validation': 'Blueberries 500g',
    'FOODS_3_808_CA_3_validation': 'Cherries 500g',
    'FOODS_3_587_CA_3_validation': 'Pineapples 1 unit',
    'FOODS_3_226_WI_2_validation': 'Cabbages 1 unit',
    'FOODS_3_555_TX_1_validation': 'Celery Pack of 2',
    'FOODS_3_586_CA_2_validation': 'Mangos Pack of 4',
    'FOODS_3_377_TX_2_validation': 'Radishes 500g',
    'FOODS_3_120_CA_1_validation': 'Spinach 500g',
    'FOODS_3_694_WI_2_validation': 'Onions 1kg',
    'FOODS_3_555_CA_3_validation': 'Bell Peppers Pack of 3',
    'FOODS_3_555_WI_3_validation': 'Garlic 500g',
    'FOODS_3_252_CA_2_validation': 'Ginger 500g',
    'FOODS_3_252_TX_1_validation': 'Sweet Potatoes 1kg',
    'FOODS_3_090_CA_2_validation': 'Cauliflower 1 unit',
    'FOODS_3_681_CA_3_validation': 'Kale 500g',
    'FOODS_3_318_WI_3_validation': 'Cantaloupes 1 unit',
    'FOODS_3_714_WI_3_validation': 'Pears Pack of 6',
    'FOODS_3_714_CA_1_validation': 'Limes Pack of 6',
    'FOODS_3_090_CA_4_validation': 'Lemons Pack of 6',
    'FOODS_3_007_WI_2_validation': 'Papayas 1 unit',
    'FOODS_3_714_CA_3_validation': 'Grapefruits Pack of 4',
    'FOODS_3_587_CA_1_validation': 'Coconuts 1 unit',
    'FOODS_3_202_CA_3_validation': 'Avocados Pack of 4',
    'FOODS_3_587_TX_2_validation': 'Cranberries 500g',
    'FOODS_3_234_WI_2_validation': 'Apricots Pack of 6',
    'FOODS_3_607_CA_3_validation': 'Raspberries 500g'
}

# List of visible names for the selector
visible_names = list(id_to_name_map.values())

# Setting page configuration to use the full available width
st.set_page_config(layout="wide")

# Cumulative DataFrame to store predictions
if 'cumulative_predictions' not in st.session_state:
    st.session_state['cumulative_predictions'] = pd.DataFrame()

# Main page
st.title("Welcome to the M5 Forecasting System")
st.markdown("### Our objective is to predict sales for the next 28 days using sales records from 2011-01-29 to 2016-06-19.")
st.markdown("[Source](https://www.kaggle.com/competitions/m5-forecasting-accuracy)")

st.markdown("### Now, we will use models to predict sales 28 days ahead.")

# Dropdown box to select visible name
selected_name = st.selectbox("Select a product for prediction", visible_names)

# Get the ID corresponding to the selected visible name
selected_id = list(id_to_name_map.keys())[list(id_to_name_map.values()).index(selected_name)]

if st.button("Make Prediction", help="Make prediction using the API"):
    try:
        # Make a GET request to the API
        api_url = f"https://walmart-lvvu2engva-ew.a.run.app/predict?id={selected_id}"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP status codes 4xx/5xx

        # Parse the JSON response
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

        # Convert predictions to a DataFrame
        prediction_df = pd.DataFrame(list(simulated_response["prediction"].items()), columns=["date", "sales"])
        prediction_df["date"] = pd.to_datetime(prediction_df["date"])
        prediction_df["id"] = id_to_name_map[simulated_response["id"]]
        prediction_df["type"] = "Prediction"

        # Convert actual data to a DataFrame
        actual_dates = list(simulated_response["prediction"].keys())  # Use the same dates as in predictions
        actual_sales = list(simulated_response["actual"].values())
        actual_df = pd.DataFrame({"date": actual_dates, "sales": actual_sales})
        actual_df["date"] = pd.to_datetime(actual_df["date"])
        actual_df["id"] = id_to_name_map[simulated_response["id"]]
        actual_df["type"] = "Actual"

        # Print the first date and sales value from the actual data
        first_actual_date = actual_df.iloc[0]['date']
        first_actual_sales = actual_df.iloc[0]['sales']
        st.write(f"The first date in actual data is {first_actual_date} and the sales value is {first_actual_sales}")

        # Convert historical data to a DataFrame
        history_df = pd.DataFrame(list(simulated_response["history"].items()), columns=["date", "sales"])
        history_df["date"] = pd.to_datetime(history_df["date"])
        history_df["id"] = id_to_name_map[simulated_response["id"]]
        history_df["type"] = "History"

        # Combine history and actual data to ensure continuity
        combined_history_actual_df = pd.concat([history_df, actual_df])
        combined_history_actual_df = combined_history_actual_df.sort_values(by="date")

        # Combine all DataFrames
        combined_df = pd.concat([combined_history_actual_df, prediction_df])

        # Ensure the combined DataFrame is sorted by date
        combined_df = combined_df.sort_values(by="date")

        # Filter data from January 9, 2016 onwards
        combined_df = combined_df[combined_df["date"] >= pd.to_datetime('2016-01-09')]

        # Pivot the DataFrame to have dates as columns
        pivot_df = prediction_df.pivot(index="id", columns="date", values="sales").reset_index()
        pivot_df.columns.name = None  # Remove column names

        # Show the pivoted DataFrame
        st.write("Predictions DataFrame:")
        st.write(pivot_df)

        # Create the figure with custom traces
        fig = go.Figure()

        # Add traces for history and actual data combined
        combined_df['color'] = combined_df.apply(lambda row: 'lightblue' if row['date'] >= pd.to_datetime('2016-03-28') else 'skyblue', axis=1)
        combined_trace = go.Scatter(x=combined_df["date"], y=combined_df["sales"], mode='lines', name='History and Actual',
                                    line=dict(color='skyblue'), showlegend=True)

        fig.add_trace(combined_trace)

        # Highlight the segment after March 28, 2016 with light blue color
        actual_trace = go.Scatter(x=combined_df[combined_df["date"] >= pd.to_datetime('2016-03-28')]["date"],
                                  y=combined_df[combined_df["date"] >= pd.to_datetime('2016-03-28')]["sales"],
                                  mode='lines', name='Actual',
                                  line=dict(color='lightblue'), showlegend=True)

        fig.add_trace(actual_trace)

        # Add traces for prediction data with light orange color
        fig.add_trace(go.Scatter(x=combined_df[combined_df["type"] == "Prediction"]["date"],
                                 y=combined_df[combined_df["type"] == "Prediction"]["sales"],
                                 mode='lines',
                                 name='Prediction',
                                 line=dict(color='orange')))

        # Update the layout of the figure
        fig.update_layout(
            title=f"Sales Forecast for {id_to_name_map[simulated_response['id']]} Over 28 Days",
            xaxis_title="Date",
            yaxis_title="Sales",
            autosize=False,
            width=1800,
            height=600,
            margin=dict(l=50, r=50, b=100, t=100, pad=4)
        )

        # Display the figure
        st.plotly_chart(fig)

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while making the API request: {e}")
    except KeyError as e:
        st.error(f"An error occurred while processing the API response: {e}")
