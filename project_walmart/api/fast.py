from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from pmdarima import auto_arima
import os
#from darts.models import TFTModel
import datetime
import pandas as pd

app = FastAPI()


@app.get('/predict')
def predict(id):

    full_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    loaded_model, product_data, data_test = pickle.load(open(os.path.join(full_path,"models",f"{id}_model.pkl"), 'rb'))

    X_test = data_test.drop(columns="sales")

    history = product_data.iloc[-224:-28]["sales"].to_dict()

    actual = data_test["sales"].to_dict()



    model_name = loaded_model.__class__.__name__
    print(model_name)

    if model_name == "Prophet":
        future_dates = loaded_model.make_future_dataframe(periods=28, freq='D')
        loading = loaded_model.predict(future_dates)
        yhat = loading["yhat"][-28:]
        dates = loading["ds"][-28:]
        forecast = {}
        for items, salesf in zip(dates,yhat):
            forecast[items] = salesf

    elif model_name == "Booster":
        forecast = {}
        forecast_raw = loaded_model.predict(X_test)
        dates = X_test.index

        for items, salesf in zip(dates,forecast_raw):
            forecast[items] = salesf

    elif model_name == "RandomForestRegressor":
        forecast = {}
        forecast_raw = loaded_model.predict(X_test)
        dates = X_test.index

        for items, salesf in zip(dates,forecast_raw):
            forecast[items] = salesf


    elif model_name == "HoltWintersResultsWrapper":
        lower_bound = data_test.index.min()
        upper_bound = data_test.index.max()
        forecast = loaded_model.predict(start=lower_bound,end=upper_bound)
    else:

        forecast = loaded_model.predict(28)
    #except:
    #    model_loaded = TFTModel.load(os.path.join(full_path,"models",f"{id}_model.pt"))
     #   df = model_loaded.predict(28).pd_dataframe()
    #    model_name = model_loaded.__class__.__name__
    #    df.reset_index(drop=False, inplace=True)
     #   df['date'] = pd.to_datetime(df['date'])  # Convert 'date' column to datetime
    #    forecast = df.set_index('date')['sales'].to_dict()




    return {"id": id,
            "model": model_name,
        "prediction": forecast,
        "actual": actual,
        "history": history}

@app.get("/full_history")

def full_history(id):
    full_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    loaded_model, product_data, data_test = pickle.load(open(os.path.join(full_path,"models",f"{id}_model.pkl"), 'rb'))


    history = product_data.iloc[:-28]["sales"].to_dict()


    return {"id": id,
    "history": history}


@app.get('/productlist')
def productlist():

    listofproducts = ['FOODS_3_090_CA_3_validation',
                    'FOODS_3_586_TX_2_validation',
                    'FOODS_3_586_TX_3_validation',
                    'FOODS_3_586_CA_3_validation',
                    'FOODS_3_090_CA_1_validation',
                    'FOODS_3_090_WI_3_validation',
                    'FOODS_3_090_TX_2_validation',
                    'FOODS_3_090_TX_3_validation',
                    'FOODS_3_252_TX_2_validation',
                    'FOODS_3_586_TX_1_validation',
                    'FOODS_3_555_TX_2_validation',
                    'FOODS_3_090_TX_1_validation',
                    'FOODS_3_120_CA_3_validation',
                    'FOODS_3_586_CA_1_validation',
                    'FOODS_3_252_TX_3_validation',
                    'FOODS_3_586_WI_3_validation',
                    'FOODS_3_694_WI_3_validation',
                    'FOODS_3_252_CA_3_validation',
                    'FOODS_3_541_CA_3_validation',
                    'FOODS_3_635_CA_3_validation',
                    'FOODS_3_226_WI_1_validation',
                    'FOODS_3_555_TX_3_validation',
                    'FOODS_3_252_CA_1_validation',
                    'FOODS_3_377_TX_3_validation',
                    'FOODS_3_808_CA_3_validation',
                    'FOODS_3_587_CA_3_validation',
                    'FOODS_3_226_WI_2_validation',
                    'FOODS_3_555_TX_1_validation',
                    'FOODS_3_586_CA_2_validation',
                    'FOODS_3_377_TX_2_validation',
                    'FOODS_3_120_CA_1_validation',
                    'FOODS_3_694_WI_2_validation',
                    'FOODS_3_555_CA_3_validation',
                    'FOODS_3_555_WI_3_validation',
                    'FOODS_3_252_CA_2_validation',
                    'FOODS_3_252_TX_1_validation',
                    'FOODS_3_090_CA_2_validation',
                    'FOODS_3_681_CA_3_validation',
                    'FOODS_3_318_WI_3_validation',
                    'FOODS_3_714_WI_3_validation',
                    'FOODS_3_714_CA_1_validation',
                    'FOODS_3_090_CA_4_validation',
                    'FOODS_3_007_WI_2_validation',
                    'FOODS_3_714_CA_3_validation',
                    'FOODS_3_587_CA_1_validation',
                    'FOODS_3_202_CA_3_validation',
                    'FOODS_3_587_TX_2_validation',
                    'FOODS_3_234_WI_2_validation',
                    'FOODS_3_607_CA_3_validation']
    empty_dict = {}
    empty_dict["products"] = listofproducts

    return empty_dict




@app.get("/")
def root():
    return {
        "greeting": "Hello, welcome to our Walmart Forecasting API for the LeWagon Project Week! Please see /docs for more info or use the /predict endpoint."
    }
