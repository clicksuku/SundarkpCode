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

# %% id="DVdBkMcLFvbe"
import pandas as pd
import numpy as np
import seaborn as sn

from matplotlib import pyplot as plt
from io import StringIO
# %matplotlib inline

# %%
# !python --version

# %% id="q6SNieOQF2O5"
import os
import ssl
import requests

from tqdm import tqdm
from PIL import Image
from io import BytesIO
from urllib import request

# %% id="wPZMC4DfG80v"
pd.set_option('display.max_columns', None)
pd.set_option('future.no_silent_downcasting', True)

# %% id="s_HcX2oRHbgz"
df_listings_details = pd.read_csv('../data/listings_detailed.csv')
df_listings = pd.read_csv('../data/listings.csv')

# %% id="MQtN3J1SH28v"
selected_columns = ['id','room_type', 'minimum_nights', 'neighbourhood',
   'availability_eoy', 'availability_365', 'picture_url',
    'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 'host_identity_verified',
    'accommodates', 'bathrooms', 'bedrooms', 'beds',
    'estimated_occupancy_l365d', 'estimated_revenue_l365d',
    'number_of_reviews', 'number_of_reviews_l30d', 'reviews_per_month',
    'review_scores_rating', 'review_scores_value',
    'instant_bookable', 'calculated_host_listings_count', 'price']


# %% id="Dz3a-5bzH5pe"
def normalize_tf_cols(df, column):
    df[column] = df[column].replace({'t': 1, 'f': 0}).astype(bool)
    return df


# %% id="x_YvrezEH_Sp"
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


# %% id="vFFrFCE2IARI"
def data_cleanup(df_1, df_2):
    df_merged_listings = pd.concat([df_listings, df_listings_details], axis=1)
    df_merged_listings = df_merged_listings.loc[:, ~df_merged_listings.columns.duplicated()]
    df_cleaned = df_merged_listings[selected_columns].dropna()
    df_cleaned = df_cleaned[df_cleaned['availability_eoy']> 0]
    df_cleaned = df_cleaned[df_cleaned['availability_365']> 0]
    df_cleaned = df_cleaned[df_cleaned['estimated_occupancy_l365d']> 0]
    df_cleaned['host_response_rate'] = df_cleaned['host_response_rate'].str.replace('%', '', regex=False).astype(float)
    df_cleaned['host_acceptance_rate'] = df_cleaned['host_acceptance_rate'].str.replace('%', '', regex=False).astype(float)
    df_cleaned = normalize_tf_cols(df_cleaned, 'instant_bookable')
    df_cleaned = normalize_tf_cols(df_cleaned, 'host_identity_verified')
    df_cleaned = normalize_tf_cols(df_cleaned, 'host_is_superhost')
    df_cleaned = fix_encoding(df_cleaned)
    df_cleaned.columns = df_cleaned.columns.str.replace('/','_')
    df_cleaned.columns = df_cleaned.columns.str.lower()
    df_cleaned.columns = df_cleaned.columns.str.replace(' ','_')
    return df_cleaned


# %% id="-oAo1OanIBdb"
df_cleaned = data_cleanup(df_listings, df_listings_details)
df_cleaned = df_cleaned.reset_index(drop=True)


# %% id="WSr256k1ICu4"
def identify_premium_properties(df, threshold=0.5):
    neighborhood_premium_stats = df_cleaned.groupby('neighbourhood').agg({
        'id':'count',
        'price':  lambda x: x.quantile(threshold),
        'review_scores_value': lambda x: x.quantile(threshold)
    })
    neighborhood_premium_stats = neighborhood_premium_stats.rename(
    columns={
        'price': 'price_q_threshold',
        'review_scores_value': 'rating_q_threshold'
    })
    neighborhood_premium_stats = neighborhood_premium_stats.reset_index()
    df_premium = df_cleaned.merge(
        neighborhood_premium_stats[['neighbourhood', 'price_q_threshold', 'rating_q_threshold']],
        on='neighbourhood',
        how='left'
    )
    df_premium['is_premium'] = (
            (df_premium['price'] >= df_premium['price_q_threshold']) &
            (df_premium['review_scores_value'] >= df_premium['rating_q_threshold'])
        )
    df_premium['is_premium'] = df_premium['is_premium'].astype(int)
    return df_premium


# %% id="ZohvfXvDIHUF"
df_premium = identify_premium_properties(df_cleaned, 0.5)

# %% colab={"base_uri": "https://localhost:8080/", "height": 112} id="wfoXlevqIIzv" outputId="85dc3e83-e861-4316-f7da-8090dad181cc"
df_premium[['id', 'picture_url']].head(2)


# %% id="Y1rA4iTOIKir"
def download_image_from_url(url):
    context = ssl._create_unverified_context()
    try:
        with request.urlopen(url, context=context) as resp:
            buffer = resp.read()
        stream = BytesIO(buffer)
        img = Image.open(stream)
        return img
    except:
        print("Image Not found exception")
        return None
    print("Image Not found")
    return None


# %% id="kcqEYyPWIMQU"
def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


# %% colab={"base_uri": "https://localhost:8080/"} id="8YpdaB85IP2s" outputId="c8112511-a947-434a-dcf8-65790a5e45bc"
sample_df = df_premium.sample(100, random_state=42)

for _, row in tqdm(sample_df.iterrows(), total=len(sample_df)):
    url = row['picture_url']
    listing_id = row['id']

    if pd.isna(url):
        continue

    if row['is_premium'] == 1:
        folder = images_dir + "/premium"
    else:
        folder = images_dir + "/non_premium"

    save_path = f"{folder}/{listing_id}.jpg"
    print(save_path)
    img = download_image_from_url(url)

    if img is None:
        print(img)
        continue;

    resized_img =  prepare_image(img, (300,400))
    resized_img.save(save_path)

# %%
# !pip install tensorflow-macos tensorflow-metal

# %%
# !pip list | grep numpy

# %%
import tensorflow as tf
from tensorflow.keras import layers

# %%
images_dir = '../images'

# %% colab={"base_uri": "https://localhost:8080/"} id="h-yt9MoBIuXq" outputId="92ce07ab-a863-4859-f03d-59bb292a03d2"
img_size = (224, 224)
batch_size = 10

dataset = tf.keras.preprocessing.image_dataset_from_directory(
    images_dir,
    image_size=img_size,
    batch_size=batch_size,
    label_mode="binary"
)

# %% colab={"base_uri": "https://localhost:8080/"} id="S1_HNJ9NJx00" outputId="845a929e-0522-40fa-9589-7e326a84eadf"
train_ds = dataset.take(int(len(dataset)*0.8))
val_ds   = dataset.skip(int(len(dataset)*0.8))
train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds   = val_ds.prefetch(tf.data.AUTOTUNE)
len(dataset), len(train_ds), len(val_ds)

# %% id="WJKpaIluJ67u"
augment = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.1)
])

# %% id="qDDQIUoFJ-0h"
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import models

base = EfficientNetB0(
    include_top=False,
    input_shape=img_size + (3,),
    weights="imagenet"
)

base.trainable = False


# %% id="QdcVaFVXKBwJ"
inputs = layers.Input(shape=img_size + (3,))
x = augment(inputs)
x = tf.keras.applications.efficientnet.preprocess_input(x)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)

x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.4)(x)

outputs = layers.Dense(1, activation="sigmoid")(x)

model = models.Model(inputs, outputs)

# %% colab={"base_uri": "https://localhost:8080/"} id="-zhgdlUQWcI7" outputId="91096f66-130b-4c70-b9cf-a56096c40287"
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.array([0, 1]),
    y=[0]* 75 + [1]* 24
)

class_weights = {0: class_weights[0], 1: class_weights[1]}
class_weights

# %% colab={"base_uri": "https://localhost:8080/"} id="icJRPywRKJlh" outputId="f3d5b904-739d-466c-bfcd-5af75a67e727"
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=8,
    class_weight=class_weights
)

# %% colab={"base_uri": "https://localhost:8080/"} id="wqHE_kmOKNi-" outputId="560a18b2-77de-4647-f885-24c4ea66f962"
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

y_true = np.concatenate([y for _, y in val_ds], axis=0)
y_pred = model.predict(val_ds).ravel()
y_class = (y_pred >= 0.46).astype(int)
print(confusion_matrix(y_true, y_class))
print(classification_report(y_true, y_class))

# %% id="8mKLGjKHf8Hp"
model.save(output_dir + "cnn_premium_detector.keras")

# %% colab={"base_uri": "https://localhost:8080/"} id="Z0SGWI4ELjiS" outputId="a9fe054c-ed8f-4e07-ed2b-3e85ce8cd325"
sample_df = df_premium.sample(100, random_state=30)

for _, row in tqdm(sample_df.iterrows(), total=len(sample_df)):
    url = row['picture_url']
    listing_id = row['id']

    if pd.isna(url):
        continue

    if row['is_premium'] == 1:
        folder = images_dir + "/test/premium"
    else:
        folder = images_dir + "/test/non_premium"

    save_path = f"{folder}/{listing_id}.jpg"
    print(save_path)
    img = download_image_from_url(url)

    if img is None:
        print(img)
        continue;

    resized_img =  prepare_image(img, (300,400))
    resized_img.save(save_path)


# %% id="F5xb74q_L-ta"
def predict_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize(img_size)

    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    prob = model.predict(arr)[0][0]

    print("Path:", path)
    print("Premium probability:", prob)

    if prob >= 0.6:
        print("Prediction → PREMIUM")
        return True
    else:
        print("Prediction → NON-PREMIUM")
        return False


# %% colab={"base_uri": "https://localhost:8080/"} id="5bMBw6dRPCxm" outputId="ba5ba2cd-3285-4d49-b1e4-2cfb60e9b5ca"
test_dir = '/content/drive/MyDrive/colab_nbs/airbnb/test'
test_folder = test_dir + "/images"
non_premium_count = 0
premium_count = 0
for filename in os.listdir(test_folder):
  full_path = os.path.join(test_folder, filename)
  result = predict_image(full_path)
  if(result is True):
    premium_count = premium_count + 1
  else:
    non_premium_count = non_premium_count + 1
print("Total Premium", premium_count )
print("Total Non-Premium", non_premium_count )

# %% id="jTMRLPHEPQeK"
