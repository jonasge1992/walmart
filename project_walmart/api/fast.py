from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from pmdarima import auto_arima
import os

app = FastAPI()


@app.get('/predict')
def predict(id):

    full_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    loaded_model = pickle.load(open(os.path.join(full_path,"models",f"{id}_model.pkl"), 'rb'))

    #HOBBIES_1_008_CA_1_validation

    forecast = loaded_model.predict(28)

    model_name = loaded_model.__class__.__name__

    return {"id": id,
            "model": model_name,
        "prediction for 28 days": forecast}


@app.get("/")
def root():
    return {
        "greeting": "Hello"
    }
