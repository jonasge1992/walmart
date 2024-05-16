from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from pmdarima import auto_arima
import os
from darts.models import TFTModel
import os
import datetime
import pandas as pd

app = FastAPI()


@app.get('/predict')
def predict(id):

    full_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    try:

        loaded_model = pickle.load(open(os.path.join(full_path,"models",f"{id}_model.pkl"), 'rb'))

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
            forecast = "Best Model was LightGBM, Forecast cannot be displayed in API yet (work in progress)."

        elif model_name == "RandomForestRegressor":
            forecast = "Best Model was RandomForestRegressor, Forecast cannot be displayed in API yet (work in progress)."

        else:

            forecast = loaded_model.predict(28)
    except:
        model_loaded = TFTModel.load(os.path.join(full_path,"models",f"{id}_model.pt"))
        df = model_loaded.predict(28).pd_dataframe()
        model_name = model_loaded.__class__.__name__
        df.reset_index(drop=False, inplace=True)
        df['date'] = pd.to_datetime(df['date'])  # Convert 'date' column to datetime
        forecast = df.set_index('date')['sales'].to_dict()




    return {"id": id,
            "model": model_name,
        "prediction for 28 days": forecast}


@app.get("/")
def root():
    return {
        "greeting": "Hello"
    }
