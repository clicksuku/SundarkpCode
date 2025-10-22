import pickle
from fastapi import FastAPI
from lead import LeadPost

app = FastAPI()

with open('pipeline_v1.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary 
    dv, model = pickle.load(f_in)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict(request: LeadPost):
    x = dv.transform([request.dict()])
    y_pred = model.predict_proba(x)[0, 1]
    return {"probability": float(y_pred)}