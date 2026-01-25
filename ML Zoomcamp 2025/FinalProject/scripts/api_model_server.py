import pickle
import xgboost as xgb
import pandas as pd
from fastapi import FastAPI
from AirbnbProperty import AirbnbProperty
from AirbnbSuperhost import AirbnbSuperhost

app = FastAPI()

with open('classification_model.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary 
    model_classification, dv_classification = pickle.load(f_in)

model_regression = xgb.XGBRegressor()
model_regression.load_model('regression_model.json')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict_property_price")
async def predict_property_price(request: AirbnbProperty):
    X_input = pd.DataFrame([request.dict()])
    expected_features = model_regression.get_booster().feature_names
    X_input = X_input[expected_features]
    y_pred = model_regression.predict(X_input)
    return {"property_price": float(y_pred)}


@app.post("/predict_superhost")
async def predict_hit(request: AirbnbSuperhost):
    print(request.dict())
    x = dv_classification.transform([request.dict()])
    y_pred = model_classification.predict_proba(x)[0, 1]
    return {"probability": float(y_pred)}