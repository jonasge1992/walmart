from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from pmdarima import auto_arima

app = FastAPI()


@app.get('/predict')
def predict(id):

    loaded_model = pickle.load(open(f"../models/{id}_model", 'rb'))

    forecast = loaded_model.predict(28)

    return {"id": id,
        'model': loaded_model,
        "prediction for 28 days": forecast}


@app.get("/")
def root():
    return {
        "greeting": "Hello"
    }
