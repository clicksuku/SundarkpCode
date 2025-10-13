import pandas as pd
import numpy as np

# Question 1
print(pd.__version__)

file_path = "car_fuel_efficiency.csv"
df = pd.read_csv(file_path)

# Question 2
print(len(df))

# Question 3
print(df['fuel_type'].unique())

# Question 4
print(df.columns[df.isna().any()])

# Question 5
print(df[df['origin']=='Asia']['fuel_efficiency_mpg'].max())

# Question 6
print(df['horsepower'].median())
frequentHorsePower=df['horsepower'].mode()[0]
print(frequentHorsePower)
df['horsepower'].fillna(frequentHorsePower, inplace=True)
print(df['horsepower'].median())

# Question 7
df_asia=df[df['origin']=='Asia']
selected_columns=df_asia[['vehicle_weight','model_year']]
select_top_columns=selected_columns.head(7)
print(select_top_columns)

X = select_top_columns.values              
XTX = X.T @ X              
XTX_inv = np.linalg.inv(XTX)
print(XTX_inv)

y = np.array([1100, 1300, 800, 900, 1000, 1100, 1200]) 
w = XTX_inv @ X.T @ y 
w_sum = w.sum()
print(w_sum)