import requests

url = "http://127.0.0.1:8000/predict"

lead = {
    "lead_source": "paid_ads",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0
}

response = requests.post(url, json=lead)
print(response.json())
