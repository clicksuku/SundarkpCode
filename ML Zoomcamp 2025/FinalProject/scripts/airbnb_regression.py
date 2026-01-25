# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import json
import numpy as np
import seaborn as sn
import pickle

from matplotlib import pyplot as plt
from io import StringIO
# %matplotlib inline

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, f1_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

# %%
df_listings_details = pd.read_csv('../data/listings_detailed.csv')
df_listings = pd.read_csv('../data/listings.csv')

# %%
pd.set_option('display.max_columns', None)
pd.set_option('future.no_silent_downcasting', True)

# %%
selected_columns = ['room_type', 'minimum_nights', 'neighbourhood',
   'availability_eoy', 'availability_365', 
    'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 'host_identity_verified',
    'accommodates', 'bathrooms', 'bedrooms', 'beds',
    'estimated_occupancy_l365d', 'estimated_revenue_l365d',
    'number_of_reviews', 'number_of_reviews_l30d', 'reviews_per_month', 
    'review_scores_rating', 'review_scores_value', 
    'instant_bookable', 'calculated_host_listings_count', 'price']


# %%
def normalize_rooms(df):
    unique_rooms = df['room_type'].unique()
    for g in unique_rooms:
        df[g] = df['room_type'].apply(lambda x: g in x)
    df = df.drop('room_type', axis=1)
    return df


# %%
def normalize_locations(df):
    unique_rooms = df['neighbourhood_grouped'].unique()
    for g in unique_rooms:
        df[g] = df['neighbourhood_grouped'].apply(lambda x: g in x)
    df = df.drop('neighbourhood_grouped', axis=1)
    df = df.drop('neighbourhood', axis=1)
    return df


# %%
def group_neighborhoods(df, min_count=300, neighborhood_col='neighbourhood'):
    room_counts = df[neighborhood_col].value_counts()
    neighborhoods_to_keep = room_counts[room_counts >= min_count].index.tolist()
    df['neighbourhood_grouped'] = df[neighborhood_col].apply(
        lambda x: x if x in neighborhoods_to_keep else 'Others'
    )
    return df


# %%
def normalize_tf_cols(df, column):
    df[column] = df[column].replace({'t': 1, 'f': 0}).astype(bool)
    return df


# %%
def fix_encoding(df_cleaned):
    encoding_map = {}
    for val in df_cleaned['neighbourhood'].unique():
        try:
            clean_val = val.encode("latin1").decode("utf-8", errors="ignore")
            encoding_map[val] = clean_val
        except (UnicodeEncodeError, AttributeError):
            encoding_map[val] = val
    df_cleaned['neighbourhood'] = df_cleaned['neighbourhood'].map(encoding_map)
    return df_cleaned


# %%
def data_cleanup(df_1, df_2):
    df_merged_listings = pd.concat([df_listings, df_listings_details], axis=1)
    df_merged_listings = df_merged_listings.loc[:, ~df_merged_listings.columns.duplicated()]
    df_cleaned = df_merged_listings[selected_columns].dropna() 
    df_cleaned = df_cleaned[df_cleaned['availability_eoy']> 0]
    df_cleaned = df_cleaned[df_cleaned['availability_365']> 0]
    df_cleaned = df_cleaned[df_cleaned['estimated_occupancy_l365d']> 0]
    df_cleaned['host_response_rate'] = df_cleaned['host_response_rate'].str.replace('%', '', regex=False).astype(float)
    df_cleaned['host_acceptance_rate'] = df_cleaned['host_acceptance_rate'].str.replace('%', '', regex=False).astype(float)
    df_cleaned = normalize_rooms(df_cleaned)
    df_cleaned = normalize_tf_cols(df_cleaned, 'instant_bookable')
    df_cleaned = normalize_tf_cols(df_cleaned, 'host_identity_verified')
    df_cleaned = normalize_tf_cols(df_cleaned, 'host_is_superhost')
    df_cleaned = fix_encoding(df_cleaned)
    df_cleaned.columns = df_cleaned.columns.str.replace('/','_')
    df_cleaned = group_neighborhoods(df_cleaned, 300, 'neighbourhood')
    df_cleaned = normalize_locations(df_cleaned)
    df_cleaned.columns = df_cleaned.columns.str.lower()
    df_cleaned.columns = df_cleaned.columns.str.replace(' ','_')
    return df_cleaned


# %%
df_cleaned = data_cleanup(df_listings, df_listings_details)

# %%
df_cleaned['log_price'] = np.log1p(df_cleaned['price'])

# %%
interested_features = ['minimum_nights',
    'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 'host_identity_verified',
    'accommodates', 'bathrooms', 'bedrooms', 'beds',
    'number_of_reviews', 'review_scores_rating',  
    'instant_bookable', 'entire_home_apt', 'private_room', 'shared_room', 'hotel_room',          
    'leopoldstadt', 'others', 'margareten', 'brigittenau', 'landstrae', 'ottakring', 
    'rudolfsheim-fnfhaus', 'neubau', 'alsergrund', 'meidling', 'favoriten']

target = 'log_price'

# %%
X_full = df_cleaned[interested_features]
y_full = df_cleaned[target]

X_train_val, X_test, y_train_val, y_test = train_test_split(X_full, y_full, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42)
len(X_train), len(X_val), len(X_test)

# %%
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

# %%
y_pred_linear_val = lin_reg.predict(X_val)

# %%
r2s_lin_reg = r2_score(y_val, y_pred_linear_val)
rmse_lin_reg = mean_squared_error(y_val, y_pred_linear_val) 

print("R^2 Score", r2s_lin_reg)
print("RMSE", rmse_lin_reg)

np.set_printoptions(suppress=True, precision=6)
coefficients = pd.DataFrame({'feature':interested_features, 'coefficient' : lin_reg.coef_})
coefficients_desc = coefficients.round(4).sort_values(by=['coefficient'], ascending=False)
print(coefficients_desc)

# %%
correlation_columns = [
    'host_identity_verified',
    'host_is_superhost', 
    'host_response_rate',
    'host_acceptance_rate',
    'review_scores_rating',
    'number_of_reviews',
    'instant_bookable',
    'log_price'  
]

corr_matrix = df_cleaned[correlation_columns].corr()
print("Correlation Matrix for Host-Related Features:")
print(corr_matrix.round(3))

# %%
rf_regression= RandomForestRegressor(n_estimators=10,random_state=42, n_jobs=-1)
rf_regression.fit(X_train, y_train)

# %%
y_pred_rf_val = rf_regression.predict(X_val)

# %%
print("R^2 Score", r2_score(y_val, y_pred_rf_val))
print("RMSE", mean_squared_error(y_val, y_pred_rf_val))

# %%
interested_features

importances = rf_regression.feature_importances_
most_important_index = np.argmax(importances)
most_important_index
most_important_feature = interested_features[most_important_index]
print(most_important_feature)

feat_imp = pd.Series(importances, index=X_full.columns).sort_values(ascending=False)
print(feat_imp)


# %%
def random_forest_varied_depth_estimator(depth, estimator):
    rf= RandomForestRegressor(n_estimators=estimator,max_depth=depth, random_state=1, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    r2s = r2_score(y_val, y_pred)
    return rmse, r2s


# %%
def find_best_depth_estimator():
    depths = [10,15,20,25, 30, 35]
    estimators = np.arange(10,210,10)

    rmse_summary = {}
    r2s_summary = {}
    results_list = []
    
    for depth in depths:
        rmses=[]
        r2ses=[]
        for estimator in estimators:
            rmse, r2s = random_forest_varied_depth_estimator(depth, estimator)
            rmses.append(rmse)
            r2ses.append(r2s)
            results_list.append({
                'depth' : depth,
                'estimator' : estimator,
                'rmse': rmse,
                'r2s' : r2s
            })
            
        rmse_summary[depth] = np.mean(rmses)
        r2s_summary[depth] = np.mean(r2ses)

    best_depth= min(rmse_summary, key=rmse_summary.get)
    
    results_df=pd.DataFrame(results_list)
    best_results_from_max_depth = results_df[results_df['depth']==best_depth]
    
    best_result_row = best_results_from_max_depth.loc[best_results_from_max_depth['rmse'].idxmin()]
    best_estimator = int(best_result_row['estimator'])
    return best_depth, best_estimator


# %%
best_max_depth, best_estimator = find_best_depth_estimator()
print("MAX Depth : ",best_max_depth)
print("Estimator : ",best_estimator)

best_rf_regressor = RandomForestRegressor(n_estimators=best_estimator,random_state=42, n_jobs=-1, max_depth=best_max_depth)
best_rf_regressor.fit(X_train, y_train)

y_pred_best_rf_val = rf_regression.predict(X_val)

# %%
print(best_max_depth, best_estimator)
r2s_rf_reg  = r2_score(y_val, y_pred_best_rf_val)
rmse_rf_reg = mean_squared_error(y_val, y_pred_best_rf_val)

print("R2 Square of Random Forest : ", r2s_rf_reg)
print("RMSE of Random Forest : ", rmse_rf_reg)

# %%
if(rmse_rf_reg < rmse_lin_reg):
    print("Random Forest is better")
else:
    print("Linear Regression is better")

# %%
gb_model = GradientBoostingRegressor(
    n_estimators=100,      # Number of boosting stages
    learning_rate=0.1,     # How much each tree contributes
    max_depth=3,           # Maximum depth of each tree
    min_samples_split=2,   # Minimum samples required to split
    min_samples_leaf=1,    # Minimum samples required at leaf node
    random_state=42
)

# Train the model
gb_model.fit(X_train, y_train)

# Make predictions
y_pred_val_gb = gb_model.predict(X_val)

# Calculate metrics
rmse = np.sqrt(mean_squared_error(y_val, y_pred_val_gb))
r2 = r2_score(y_val, y_pred_val_gb)
mae = mean_absolute_error(y_val, y_pred_val_gb)

print("\nGradient Boosting Results:")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.2f}")


feature_importance = pd.DataFrame({
    'feature': X_full.columns,
    'importance': gb_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n Feature Importance:")
print(feature_importance)

# Plot feature importance
plt.figure(figsize=(10, 6))
sn.barplot(data=feature_importance, x='importance', y='feature')
plt.title('Gradient Boosting - Feature Importance')
plt.xlabel('Importance Score')
plt.ylabel('Feature')

# %%
print("Model Type:", type(gb_model))
print("Model Parameters:", gb_model.get_params())

# %%
import xgboost as xgb

# %%
xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',  # For regression tasks
    n_estimators=100,              # Number of trees
    learning_rate=0.1,             # Step size shrinkage
    max_depth=3,                   # Maximum tree depth
    random_state=42
)

# Train the model
xgb_model.fit(X_train, y_train)

# Make predictions
y_pred_compare_xgb_vals = xgb_model.predict(X_val)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_val, y_pred_compare_xgb_vals))
r2 = r2_score(y_val, y_pred_compare_xgb_vals)
mae = mean_absolute_error(y_val, y_pred_compare_xgb_vals)

print("XGBoost Results:")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.2f}")

# %%
model_params = xgb_model.get_xgb_params()
print(model_params)

# %%
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100,random_state=42, n_jobs=-1, max_depth=10),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42,loss='squared_error'),
    'XGB Regression' : xgb.XGBRegressor(objective='reg:squarederror',learning_rate=0.1,max_depth=3,random_state=42)
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred_compare_vals = model.predict(X_val)
    results[name] = {
        'RMSE': np.sqrt(mean_squared_error(y_val, y_pred_compare_vals)),
        'R²': r2_score(y_val, y_pred_compare_vals),
        'MAE': mean_absolute_error(y_val, y_pred_compare_vals)
    }

    plt.figure(figsize=(12, 6))

    print("Name of Model", name)
    # Plot 1: Predictions vs Actual
    plt.subplot(1, 2, 1)
    plt.scatter(y_val, y_pred_compare_vals, alpha=0.7, s=100)
    plt.plot([y_val.min(), y_val.max()], [y_pred_compare_vals.min(), y_pred_compare_vals.max()], 'r--', lw=2)
    plt.xlabel('Actual Price ($)')
    plt.ylabel('Predicted Price ($)')
    plt.title(f"{name} : Actual vs Predicted")
    
    # Plot 2: Residuals
    plt.subplot(1, 2, 2)
    residuals = y_val - y_pred_compare_vals
    plt.scatter(y_pred_compare_vals, residuals, alpha=0.7, s=100)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Price ($)')
    plt.ylabel('Residuals')
    plt.title(f"{name} : Residual Plot")

# Compare results
results_df = pd.DataFrame(results).T
print("\nModel Comparison:")
print(results_df.round(4))

# %%
chosen_model = xgb_model

with open('../_models/regression_model.bin', 'wb') as f:
    pickle.dump(chosen_model, f)

# %%
