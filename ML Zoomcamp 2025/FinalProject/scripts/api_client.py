from lzma import is_check_supported
import requests
import pandas as pd
import numpy as np
import json

url_property_price = "http://127.0.0.1:8000/predict_property_price"
url_superhost = "http://127.0.0.1:8000/predict_superhost"

# List of features used in the model
interested_features = [
    'host_response_rate', 'host_acceptance_rate', 
    'host_is_superhost', 'host_identity_verified',
    'accommodates', 'bathrooms', 'bedrooms', 'beds',
    'number_of_reviews', 'review_scores_rating',  
    'minimum_nights','instant_bookable', 
    'entire_home_apt', 'private_room', 'shared_room', 'hotel_room',          
    'leopoldstadt', 'others', 'margareten', 'brigittenau', 
    'landstrae', 'ottakring', 'rudolfsheim_fnfhaus', 
    'neubau', 'alsergrund', 'meidling', 'favoriten'
]

properties = [
    {"minimum_nights":31,"host_response_rate":96.0,"host_acceptance_rate":88.0,"host_is_superhost":True,"host_identity_verified":True,"accommodates":2,"bathrooms":1.0,"bedrooms":0.0,"beds":1.0,"number_of_reviews":74,"review_scores_rating":4.86,"instant_bookable":True,"entire_home_apt":True,"private_room":False,"shared_room":False,"hotel_room":False,"leopoldstadt":False,"others":False,"margareten":True,"brigittenau":False,"landstrae":False,"ottakring":False,"rudolfsheim_fnfhaus":False,"neubau":False,"alsergrund":False,"meidling":False,"favoriten":False},
    {"minimum_nights":1,"host_response_rate":100.0,"host_acceptance_rate":98.0,"host_is_superhost":False,"host_identity_verified":True,"accommodates":3,"bathrooms":1.0,"bedrooms":1.0,"beds":2.0,"number_of_reviews":345,"review_scores_rating":4.7,"instant_bookable":False,"entire_home_apt":True,"private_room":False,"shared_room":False,"hotel_room":False,"leopoldstadt":False,"others":False,"margareten":False,"brigittenau":False,"landstrae":False,"ottakring":False,"rudolfsheim_fnfhaus":False,"neubau":False,"alsergrund":False,"meidling":True,"favoriten":False},
    {"minimum_nights":2,"host_response_rate":100.0,"host_acceptance_rate":100.0,"host_is_superhost":False,"host_identity_verified":True,"accommodates":5,"bathrooms":1.0,"bedrooms":2.0,"beds":4.0,"number_of_reviews":7,"review_scores_rating":5.0,"instant_bookable":True,"entire_home_apt":True,"private_room":False,"shared_room":False,"hotel_room":False,"leopoldstadt":False,"others":True,"margareten":False,"brigittenau":False,"landstrae":False,"ottakring":False,"rudolfsheim_fnfhaus":False,"neubau":False,"alsergrund":False,"meidling":False,"favoriten":False},
    {"minimum_nights":1,"host_response_rate":100.0,"host_acceptance_rate":99.0,"host_is_superhost":False,"host_identity_verified":True,"accommodates":2,"bathrooms":2.0,"bedrooms":1.0,"beds":1.0,"number_of_reviews":2,"review_scores_rating":4.0,"instant_bookable":True,"entire_home_apt":False,"private_room":True,"shared_room":False,"hotel_room":False,"leopoldstadt":False,"others":False,"margareten":False,"brigittenau":False,"landstrae":False,"ottakring":False,"rudolfsheim_fnfhaus":False,"neubau":False,"alsergrund":False,"meidling":True,"favoriten":False},
    {"minimum_nights":2,"host_response_rate":100.0,"host_acceptance_rate":92.0,"host_is_superhost":True,"host_identity_verified":True,"accommodates":2,"bathrooms":1.5,"bedrooms":1.0,"beds":2.0,"number_of_reviews":91,"review_scores_rating":4.7,"instant_bookable":False,"entire_home_apt":True,"private_room":False,"shared_room":False,"hotel_room":False,"leopoldstadt":False,"others":True,"margareten":False,"brigittenau":False,"landstrae":False,"ottakring":False,"rudolfsheim_fnfhaus":False,"neubau":False,"alsergrund":False,"meidling":False,"favoriten":False}
]



properties_superhost = [
  {"host_response_rate":100.0,"host_acceptance_rate":100.0,"host_identity_verified":True,"host_listings_count":3.0,"review_scores_rating":5.0,"review_scores_cleanliness":5.0,"review_scores_communication":5.0,"review_scores_accuracy":5.0,"number_of_reviews":13,"number_of_reviews_ltm":13,"reviews_per_month":4.87,"instant_bookable":False,"calculated_host_listings_count":3,"availability_30":3},
  {"host_response_rate":96.0,"host_acceptance_rate":88.0,"host_identity_verified":True,"host_listings_count":5.0,"review_scores_rating":4.88,"review_scores_cleanliness":4.88,"review_scores_communication":4.94,"review_scores_accuracy":4.94,"number_of_reviews":16,"number_of_reviews_ltm":2,"reviews_per_month":0.44,"instant_bookable":True,"calculated_host_listings_count":4,"availability_30":5},
  {"host_response_rate":100.0,"host_acceptance_rate":100.0,"host_identity_verified":True,"host_listings_count":1.0,"review_scores_rating":4.95,"review_scores_cleanliness":4.91,"review_scores_communication":4.95,"review_scores_accuracy":4.95,"number_of_reviews":22,"number_of_reviews_ltm":16,"reviews_per_month":1.62,"instant_bookable":False,"calculated_host_listings_count":1,"availability_30":15},
  {"host_response_rate":90.0,"host_acceptance_rate":96.0,"host_identity_verified":True,"host_listings_count":1.0,"review_scores_rating":4.85,"review_scores_cleanliness":4.96,"review_scores_communication":4.92,"review_scores_accuracy":4.9,"number_of_reviews":161,"number_of_reviews_ltm":34,"reviews_per_month":1.66,"instant_bookable":True,"calculated_host_listings_count":1,"availability_30":7},
  {"host_response_rate":100.0,"host_acceptance_rate":100.0,"host_identity_verified":True,"host_listings_count":2.0,"review_scores_rating":5.0,"review_scores_cleanliness":5.0,"review_scores_communication":5.0,"review_scores_accuracy":4.96,"number_of_reviews":26,"number_of_reviews_ltm":14,"reviews_per_month":1.2,"instant_bookable":True,"calculated_host_listings_count":1,"availability_30":3}
]


df_new_data = pd.DataFrame(properties)
df_new_data_superhost = pd.DataFrame(properties_superhost)

for index, row in df_new_data.iterrows():
  print(properties[index])
  json_string = json.dumps(properties[index])
  print(json_string)
  predicted_property_price = requests.post(url_property_price, json=properties[index])
  property_price=np.expm1(predicted_property_price.json()['property_price'])
  print(f"Property Price: ${property_price}")
  input()

for index, row in df_new_data_superhost.iterrows():
    try:
        # Print which property we're processing
        print(f"\n{'='*50}")
        print(f"Processing property {index + 1}/{len(df_new_data_superhost)}")
        
        # Make the request
        response = requests.post(
            url_superhost, 
            json=properties_superhost[index],
            headers={'Content-Type': 'application/json'}
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Parse the JSON response
                result = response.json()
                probability = result.get('probability', 0)
                
                # Format the probability as percentage with 2 decimal places
                print(f"\nSuperhost probability: {probability:.2%}")
                
                # Check if probability is greater than 0.8 (80%)
                if probability > 0.8:
                    print("✅ This host is a SuperHost!")
                else:
                    print("❌ This is not a SuperHost")
                    
                print(f"Full response: {result}")
            except json.JSONDecodeError:
                print("Failed to parse JSON response")
                print(f"Raw response: {response.text}")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error making request: {str(e)}")
    
    input("\nPress Enter to continue to the next property...")
    print("="*50)
print("\n\n")
    