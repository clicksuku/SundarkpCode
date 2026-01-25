🏡 Airbnb Vienna -- Price Prediction & Listing Classification System
===================================================================

## Table of Contents

- [0. Problem Statement](#0-problem-statement)
- [1. Installation and Running the Project](#1-installation-and-running-the-project)
  - [Running locally](#running-locally)
  - [Clone the Repository](#clone-the-repository)
  - [Create Virtual Environment](#create-virtual-environment)
  - [Install Dependencies](#install-dependencies)
- [2. Dataset and Project Details](#2-dataset-and-project-details)
  - [Dataset Source](#dataset-source)
  - [Key Dataset Files](#key-dataset-files)
  - [Key Features Used](#key-features-used)
  - [Data Preprocessing](#data-preprocessing)
- [3. Visualization](#3-visualization)
- [4. Regression Model -- Price Prediction](#4-regression-model----price-prediction)
  - [Objective](#objective)
  - [Target Variable](#target-variable)
  - [Models Implemented](#models-implemented)
  - [Evaluation Metrics](#evaluation-metrics)
  - [Model Selection](#model-selection)
- [5. Classification Model -- Host vs Superhost Listings](#5-classification-model----host-vs-superhost-listings)
  - [Objective](#objective-1)
  - [Target Definition](#target-definition)
  - [Models Implemented](#models-implemented-1)
  - [Data Loading](#data-loading)
  - [Feature Set Definition](#feature-set-definition)
  - [Data Cleaning & Feature Engineering](#data-cleaning--feature-engineering)
  - [Train/Validation/Test Split](#trainvalidationtest-split)
  - [Baseline Model](#baseline-model)
  - [Threshold / Precision-Recall Analysis](#threshold--precision-recall-analysis)
  - [Cross-Validation for Regularization (C)](#cross-validation-for-regularization-c)
  - [GridSearchCV (Final Model Selection)](#gridsearchcv-final-model-selection)
  - [Final Evaluation (Validation Set)](#final-evaluation-validation-set)
  - [Exported Artifact](#exported-artifact)
  - [Analysis of Approaches, Results, and Final Outcome](#analysis-of-approaches-results-and-final-outcome)
- [6. Abandoned Project - CNN Project for Premium/Non-Premium Classification](#6-abandoned-project---cnn-project-for-premiumnon-premium-classification)
- [7. CNN Project to identify Room Type - Multi class identification with Softmax function](#7-cnn-project-to-identify-room-type---multi-class-identification-with-softmax-function)
- [8. Converting Jupyter Notebooks with Jupytext](#8-converting-jupyter-notebooks-with-jupytext)
- [9. Requirements and Installation](#9-requirements-and-installation)
- [10. FastAPI Deployment and Serving](#10-fastapi-deployment-and-serving)
  - [Run API Locally](#run-api-locally)
  - [Available Endpoints](#available-endpoints)
- [11. Docker Deployment](#11-docker-deployment)
- [12. Kubernetes Deployment](#12-kubernetes-deployment)
  - [Kubernetes Manifests](#kubernetes-manifests)
  - [Deployment Commands](#deployment-commands)
  - [Testing Kubernetes Deployment](#testing-kubernetes-deployment)
- [13. Project Characterestics](#13-project-characterestics)
- [14. Project Highlights](#14-project-highlights)
- [15. Contributing](#15-contributing)
- [16. Evaluation](#16-evaluation)

* * * * *

0\. Problem Statement
------------------------------------------

The short-term rental market is highly competitive, and pricing or positioning a listing incorrectly can significantly impact occupancy and revenue. Hosts and property managers often struggle to determine:

-   What is a **fair nightly price** for a listing?

-   Which listings are likely to be rented out based on the Host characterestics whether the host is **Superhost** versus **Normal Host**?

This project applies **Machine Learning techniques** on the **Airbnb Vienna public dataset** to solve two core problems:

### Regression Problem

Predict the **nightly price** of an Airbnb listing based on location, room characteristics, availability, host attributes, and review metrics.

### Classification Problem

Classify listings into **Host vs Superhost** categories based on pricing, amenities, and demand-related features.\
This enables better market segmentation and pricing strategy insights.

The project follows an **end-to-end ML lifecycle**: data analysis → modeling → evaluation → deployment using **FastAPI, Docker, and Kubernetes**.

* * * * *

Project Structure (Repository Overview)
------------------------------------------

This document explains the structure of the repository and how the different folders/scripts connect end-to-end.

---

## A. High-level layout

```text
skpmlzoomcamp_finalproject_2025/
├── Analysis/
├── Data/
├── data_room_classifier/
├── Notebook/
├── scripts/
├── _models/
├── Docker/
├── Kubernetes/
├── README.md
├── readme_cnn.md
├── requirements.txt
├── pyproject.toml
└── uv.lock
```


## B. Folder-by-folder explanation

### `Data/`

Holds the Airbnb Vienna tabular data files used for regression/classification.

Typical contents (based on your README updates):

- `listings.csv`
- `listings_detailed.csv`
- `data_dictionary.xlsx`

This folder is the starting point for tabular ML.


### `data_room_classifier/`

Holds the image dataset used for CNN training and inference.

Expected structure (as used in the notebook):

```text
data_room_classifier/
├── train/
│   ├── kitchen/
│   ├── livingroom/
│   └── ...
└── test/
    ├── kitchen/
    ├── livingroom/
    └── ...
```

This folder is the starting point for the CNN room classifier.


### `Notebook/`

Contains Jupyter notebooks used for experimentation, EDA, training, and evaluation.

In this project, the notebooks are the “research” layer where you:

- Explore data
- Prototype feature engineering
- Train models
- Validate results
- Export model artifacts

Examples:

- `airbnb_classification.ipynb`
- `airbnb_cnn_roomtype_classification.ipynb`

### `scripts/`

Contains Python scripts (exported/cleaned versions of notebook logic, plus helper utilities).

Purpose:

- Make training reproducible without running notebooks
- Enable automation (future: pipelines, CI, cron retraining)

Examples (based on repo contents):

- `airbnb_classification.py`
- `airbnb_regression.py`
- CNN scripts for room-type classification
- `download_dataset.py`


### `_models/`

Central folder for **trained model artifacts** used at inference time.

This folder is important because both Docker/FastAPI serving and K8s deployment depend on these artifacts.

Typical artifacts in this project:

- `classification_model.bin` (classification model + DictVectorizer)
- `regression_model.json` (XGBoost regression model)
- `cnn_room_classifier_effnet.keras` (Keras CNN model)
- `cnn_room_classifier_effnet.onnx` or `cnn_room_classifier_effnet_fixed.onnx` (ONNX export)

### `Docker/`

Production-serving layer for running the inference API.

Contains:

- `api_model_server.py`
  - FastAPI app
  - Loads models from `_models/`
  - Exposes endpoints for regression / classification / CNN
- `api_client.py`
  - Makes example requests to the API endpoints
  - Useful for local testing
- `AirbnbProperty.py`, `AirbnbSuperhost.py`
  - Pydantic request schemas
- `dockerfile`
  - Builds the container image
- `requirements.txt`
  - Runtime dependencies (FastAPI, xgboost, tensorflow, etc.)

This folder is what you run when you want to serve the models.

### `Kubernetes/`

Kubernetes deployment manifests for running the Docker image in a cluster.

Contains:

- `deployment.yaml`
  - Defines pod replicas and container image
- `service.yaml`
  - Exposes the deployment internally/externally
- `README.md`
  - `kubectl apply`, verify, port-forward commands

This folder is used when deploying the API beyond local Docker.

### `Analysis/`

Typically used for:

- project artifacts
- images/plots
- intermediate analysis outputs

(Your repo contains this folder; exact contents can evolve.)

### Root-level files

- `README.md`
  - Primary project documentation
- `readme_cnn.md`
  - Focused documentation for the CNN room classifier notebook
- `requirements.txt`
  - Development dependencies (root-level)
- `pyproject.toml` / `uv.lock`
  - Python project metadata / lockfile (if using `uv`)

## C. End-to-end workflow (how everything connects)

### Step A: Train models (Notebook / scripts)

- Tabular models:
  - Work in `Notebook/airbnb_regression.ipynb` and `Notebook/airbnb_classification.ipynb` (or scripts)
  - Export artifacts into `_models/`

- CNN model:
  - Work in `Notebook/airbnb_cnn_roomtype_classification.ipynb`
  - Export artifacts into `_models/`

### Step B: Serve models locally (FastAPI)

- Run `Docker/api_model_server.py` with Uvicorn
- Test with `Docker/api_client.py`

### Step C: Containerize (Docker)

- Build image using `Docker/dockerfile`
- Run container and confirm endpoints

### Step D: Deploy (Kubernetes)

- Update `Kubernetes/deployment.yaml` to use your image tag
- `kubectl apply ...`
- Verify pods + service
- Port-forward or load balancer access

## D. Notes / conventions

- `_models/` is the single source of truth for inference artifacts.
- `Notebook/` is for exploration; `scripts/` is for reproducible runs.
- `Docker/` is the deployment unit for FastAPI serving.
- `Kubernetes/` is the cluster deployment layer for that Docker image.

* * * * *

1\. Installation and Running the Project
----------------------------------------

## Running locally

### Clone the Repository

`git clone https://github.com/clicksuku/skpmlzoomcamp_finalproject_2025.git

### Create Virtual Environment

`python3 -m venv mlenv source mlenv/bin/activate `

### Install Dependencies

`pip install -r requirements.txt `

* * * * *

2\. Dataset and Project Details
-------------------------------

### Dataset Source

-   **Dataset**: Airbnb Vienna Open Dataset

-   **Source**: Inside Airbnb (Publicly available)

-   **City**: Vienna, Austria

### Key Dataset Files

-   `Data/listings.csv` -- Listing-level information
-   `Data/listings_detailed.csv` -- Detailed listing-level information
-   'Data/data_dictionary.xlsx' -- Data dictionary of the data considered

### Key Features Used

| Feature | Description |
| --- | --- |
| `room_type` | Entire home / Private room / Shared room |
| `accommodates` | Number of guests |
| `bedrooms`, `beds`, `bathrooms` | Property attributes |
| `number_of_reviews` | Engagement indicator |
| `review_scores_rating` | Guest satisfaction |
| `availability_365` | Demand proxy |
| `host_is_superhost` | Host quality indicator |
| `log_price` | Target variable (Regression) |

### Data Preprocessing

-   Concatenated listing and listing details

-   Remove duplicate columns after concatenation

-   Remove NA

-   Missing value imputation

-   Room code mapping for room types

-   Removed % from host response rate and host acceptance rate
-   Currency normalization and price cleaning

-   Outlier removal using IQR

-   One-hot encoding for categorical features

* * * * *

3\. Visualization 
----------------------------------------

- Histogram Plots
- Box And Whisper Plots
- Scatter Plots
- Heatmap
- Pie Chart


  <img width="802" height="376" alt="image" src="https://github.com/user-attachments/assets/59284e38-403c-4bca-883c-32115f9a519e" />
  <img width="755" height="421" alt="image" src="https://github.com/user-attachments/assets/60650228-3c2c-4024-846f-2b8049298660" />
  <img width="781" height="540" alt="image" src="https://github.com/user-attachments/assets/4c3cd742-81cd-41df-bf1c-11ab8f4a308e" />
  <img width="784" height="379" alt="image" src="https://github.com/user-attachments/assets/45243c17-92b5-4774-b0d4-08d2d39bcc40" />
  <img width="809" height="416" alt="image" src="https://github.com/user-attachments/assets/a25b9a98-70be-4416-8600-e1be779a85d2" />
  <img width="610" height="519" alt="image" src="https://github.com/user-attachments/assets/959e276a-00fe-4d3c-9338-68d732c61319" />
  <img width="646" height="441" alt="image" src="https://github.com/user-attachments/assets/04e6af35-1092-429f-96da-f68b98db215d" />




* * * * *

4\. Regression Model -- Price Prediction
---------------------------------------

### Objective

Predict the **nightly price** of Airbnb listings in Vienna.

### Target Variable

-   `price` (log-transformed for stability)

### Models Implemented

1.  **Linear Regression** (Baseline)

2.  **Random Forest Regressor**

3.  **Gradient Boosting Regressor**

### Evaluation Metrics

-   **RMSE** -- Root Mean Squared Error

-   **MAE** -- Mean Absolute Error

-   **R² Score**

### Model Selection

Gradient Boosting Regressor performed best due to:

-   Non-linear relationship handling

-   Robustness to outliers

-   Superior RMSE and R² scores

***. Key Observaions from Regression:**

**✅**** Neighborhood Features WORKED!**

-   Adding neighborhood information boosted R² by **6.6 percentage points** (0.332 → 0.398)
-   This confirms location is a major price driver

**✅**** Proper Encoding:**

-   "Others" (locations beyond top 10 is categorized as 'Others') in Neighbourhood is included as a category (coefficient: 0.1056)
-   This serves as the baseline for neighborhood comparisons

***\. Feature Analysis by Impact:***

**🏆**** Top Price Drivers (>15% premium):**

1.  **Hotel Room (+67.4%)**: e^0.5153 = 1.674
2.  **Entire Home/Apt (+43.8%)**: e^0.3633 = 1.438
3.  **Bathrooms (+18.6%)**: Each additional bathroom
4.  **Leopoldstadt (+18.4%)**: Premium neighborhood
5.  **Neubau (+18.0%)**: Premium neighborhood

**Strong Positive Influencers (10-15% premium):**

1.  **Review Scores Rating (+16.4%)**: Quality premium
2.  **Bedrooms (+15.5%)**: Each additional bedroom
3.  **Landstraße (+12.5%)**: Above-average neighborhood
4.  **Superhost (+12.3%)**: Host reputation premium
5.  **Instant Bookable (+11.2%)**: Convenience premium

**Baseline Neighborhood:**

-   **"Others" (+11.1%)**: Slightly above average - interesting!

-   This means all other neighborhoods are compared to "Others"
-   Some neighborhoods are below "Others" (negative coefficients)

**Significant Discounts:**

-   **Shared Room (-53.8%)**: Massive discount: e^-0.7708 = 0.462
-   **Host Identity Verified (-32.8%)**: Surprisingly large negative effect
-   **Meidling (-14.4%)**, **Ottakring (-16.3%)**: Below-average neighborhoods

***\. Business Insights & Strategy:**

***Pricing Strategy:***

1.  **Property Type Hierarchy**: Hotel rooms command highest premium, followed by entire homes
2.  **Location Matters**: Leopoldstadt, Neubau, Landstraße are premium areas
3.  **Quality Pays**: Higher ratings = 16% price premium
4.  **Size Premium**: Bathrooms add more value (18.6%) than bedrooms (15.5%)

**Counterintuitive Findings:**

 **Host Identity Verified (-32.8%)**: This is suspiciously large

-   Possible issue: New hosts verify identity but charge less?
-   Check correlation with other variables

  **Favoriten, Brigittenau discounts**: Working-class areas as expected


***\. Detailed Breakdown:***

**A. Host Identity Verified Relationships:**

-   **With log_price: -0.105** → Verified hosts charge **10.5% less** on average (in log space)
-   **With superhost: 0.092** → Weak positive correlation with being a superhost
-   **With reviews: 0.112** → Verified hosts have slightly more reviews
-   **With instant bookable: -0.082** → Verified hosts are LESS likely to offer instant booking

**B. Other Interesting Correlations:**

**Superhost Effects:**

-   **Superhost → Rating: 0.327** → Strong! Superhosts have much higher ratings
-   **Superhost → Price: 0.128** → Superhosts charge 12.8% MORE (expected)
-   **Superhost → Instant booking: -0.182** → Superhosts are LESS likely to offer instant booking

**Response/Acceptance Rates:**

-   **Response ↔ Acceptance: 0.552** → Strong correlation - hosts who respond quickly also accept more bookings
-   **Acceptance → Instant booking: 0.450** → Strong! Hosts who accept more also offer instant booking

**Rating Effects:**

-   **Rating → Price: 0.175** → Higher ratings = 17.5% higher prices (makes sense)
-   **Rating → Superhost: 0.327** → Higher ratings help become superhost
-   **Rating → Instant booking: -0.189** → Higher-rated listings are LESS likely to offer instant booking

***\. Why ****host_identity_verified**** Has Negative Coefficient:**

**Possible Explanations:**

1.  **New Host Effect**: New hosts verify identity but charge less to attract first bookings
2.  **Budget Host Strategy**: Hosts focusing on budget segment verify but keep prices low
3.  **Professional vs Casual**: Casual hosts verify but aren't optimizing for max revenue
4.  **Market Segment**: Verified hosts might dominate budget segments

**Evidence Supporting This:**

-   Verified hosts have more reviews (0.112 correlation) → More established but cheaper
-   Verified hosts less likely to offer instant booking (-0.082) → Different strategy
-   Weak correlation with superhost (0.092) → Not the premium hosts

**\. Business Interpretation:**

**Two Types of Verified Hosts Emerge:**

1.  **Premium Verified Hosts**:

-   Also superhosts (some correlation: 0.092)
-   Higher ratings
-   Higher prices

2.  **Budget Verified Hosts**:

-   Verify identity (trust signal)
-   Charge less to compete
-   More reviews from volume strategy
-   Less likely to offer premium features (instant booking)

**\. Actionable Insights:**

**For Hosts:**

-   **If you verify identity**: Be aware you might be pricing too low
-   **Combine verification with superhost status** to command premium prices

**For Platform:**

-   Verification alone doesn't command price premium
-   Need to encourage verified hosts to also pursue superhost status
-   Consider tiered verification system

* * * * *

5\. Classification Model -- Host vs Superhost Listings
----------------------------------------------------------

### Objective

This document summarizes the key steps, experiments, evaluation results, and final outcome of the notebook:

- `Notebook/airbnb_classification.ipynb`

The objective of the notebook is to train a **binary classification** model to predict whether a host is a **Superhost**.

- **Task**: Binary classification
- **Target**: `host_is_superhost`
- **Prediction**: `P(host_is_superhost = 1)`


### Target Definition

`Superhost = 1  if probability > 80%  `

### Models Implemented

1.  **Logistic Regression**

2.  **Decision Tree Classifier**

### Data Loading

The notebook loads two Vienna Airbnb datasets and then merges them:

- `../data/listings.csv`
- `../data/listings_detailed.csv`

They are concatenated column-wise and duplicate columns are removed.

---

### Feature Set Definition

Features are defined in groups.

#### Host features

- `host_response_rate`
- `host_acceptance_rate`
- `host_identity_verified`
- `host_listings_count`
- `host_is_superhost` *(this is the target, later separated)*

#### Review features

- `review_scores_rating`
- `review_scores_cleanliness`
- `review_scores_communication`
- `review_scores_accuracy`
- `number_of_reviews`
- `number_of_reviews_ltm`
- `reviews_per_month`

#### Listing features

- `instant_bookable`
- `calculated_host_listings_count`
- `availability_30`

#### Categorical features

- `room_type`
- `neighbourhood`

All features combined:

```text
['host_response_rate',
 'host_acceptance_rate',
 'host_identity_verified',
 'host_listings_count',
 'host_is_superhost',
 'review_scores_rating',
 'review_scores_cleanliness',
 'review_scores_communication',
 'review_scores_accuracy',
 'number_of_reviews',
 'number_of_reviews_ltm',
 'reviews_per_month',
 'instant_bookable',
 'calculated_host_listings_count',
 'availability_30',
 'room_type',
 'neighbourhood']
```

---

### Data Cleaning & Feature Engineering

The notebook performs a clear end-to-end preprocessing pipeline via helper functions.

#### Merge and subset

- Concatenate `listings` and `listings_detailed`
- Remove duplicated columns
- Keep only `all_features`
- Drop rows with missing values: `dropna()`

#### Normalize percentage columns

These are originally strings like `"96%"`:

- `host_response_rate`
- `host_acceptance_rate`

Processing:

- remove `%`
- cast to `float`

#### One-hot encode `room_type`

The notebook creates a boolean column per unique `room_type` value and drops the original `room_type` column.

#### Convert `t` / `f` flags to boolean

For columns:

- `instant_bookable`
- `host_identity_verified`
- `host_is_superhost`

Mapping:

- `t -> 1`, `f -> 0`, then cast to `bool`

#### Fix encoding issues in neighbourhood

`neighbourhood` values may have encoding artifacts. The notebook attempts:

- `latin1` encode
- `utf-8` decode (ignore errors)

#### Group neighbourhoods into top-N + "Others"

To avoid high-cardinality neighbourhoods, it groups:

- neighbourhoods with count >= `min_count` (300)
- all others become `Others`

Then it one-hot encodes the grouped neighbourhoods and drops original neighbourhood columns.

#### Column standardization

- replace `/` with `_`
- lowercase
- replace spaces with `_`

#### Final cleaned dataset size

After cleaning:

- total rows: **8690**

---

### Train/Validation/Test Split

The notebook creates a dataset that still contains the target column and then splits:

- **Train+Val**: 80%
- **Test**: 20%

Then splits Train+Val into:

- **Train**: 60% (of total)
- **Validation**: 20% (of total)

Based on the printed sizes:

- Train: **5214**
- Validation: **1738**
- Test: **1738**

The target vectors are created (`y_train`, `y_val`, `y_test`) and then `host_is_superhost` is removed from feature frames.

---

### Baseline Model

####  Baseline logistic regression

A baseline model is trained:

- `LogisticRegression(solver='liblinear', C=1.0, max_iter=2000, random_state=42)`

The features are vectorized using:

- `DictVectorizer()`

The prediction used is:

- `y_pred_val = predict_proba(X_val)[:, 1]`

#### Baseline ROC AUC

Baseline validation ROC AUC:

- **0.8233**

This is a good baseline, showing the signal in host/review/listing features.

---

### Threshold / Precision-Recall Analysis

A custom function `p_r_dataframe` computes precision, recall, and F1 score across thresholds from 0 to 1.

Best threshold by F1 on validation was found at:

- **threshold ≈ 0.33**

Interpretation:

- The default 0.5 threshold is not necessarily optimal.
- Since superhost can be imbalanced, lowering the threshold can improve recall and F1.

---

### Cross-Validation for Regularization (C)

The notebook performs 5-fold CV across values of `C`:

- `[0.001, 0.01, 0.1, 0.5, 1, 5, 10]`

Metric:

- ROC AUC

Mean CV AUC results (approx):

- `C=0.001` -> **0.781**
- `C=0.01` -> **0.824**
- `C=0.1` -> **0.838**
- `C=0.5` -> **0.839**
- `C=1` -> **0.839**
- `C=5` -> **0.840**
- `C=10` -> **0.840**

Observation:

- Performance improves quickly as `C` increases, then plateaus.

---

### GridSearchCV (Final Model Selection)

A `GridSearchCV` is run on Logistic Regression (balanced class weights):

- solver: `lbfgs`
- `class_weight='balanced'`
- scoring: `roc_auc`
- CV folds: 5

Parameter grid:

- `C: [0.001, 0.01, 0.1, 1, 10, 100]`

Best parameter:

- **Best C = 100**

Best cross-validated ROC AUC:

- **0.8401**

The CV table shows a plateau from `C=10` to `C=100`.

---

### Final Evaluation (Validation Set)

Using the best estimator from GridSearchCV, evaluation is computed on the validation set.

#### Metrics

- **F1 score**: **0.6903**
- **ROC AUC**: **0.8472**

#### Confusion matrix

```text
[[757 359]
 [105 517]]
```

Interpretation (with `class_weight='balanced'`):

- The model prioritizes recall for the positive class (Superhost), at the cost of more false positives.

---

### Exported Artifact

The final output is a pickled artifact saved to:

- `../_models/classification_model.bin`

Contents:

- `(final_classification_model, dv_log_reg)`

This is later loaded by the FastAPI server for inference.

---

### Analysis of Approaches, Results, and Final Outcome

### A. What approaches were tried?

#### A1. Baseline logistic regression (simple train/val)

- Pros:
  - Quick baseline
  - Establishes a starting AUC (0.823)
- Cons:
  - Hyperparameters not tuned
  - Threshold not optimized

#### A2. Threshold analysis using Precision/Recall and F1

- The notebook explicitly searches thresholds and finds **~0.33** works best for F1.
- This is important because:
  - If Superhost is rarer, using 0.5 can under-predict positives.

#### A3. K-Fold CV for regularization strength (C)

- Evaluates how stable ROC AUC is across folds.
- Helps detect overfitting/underfitting behavior as `C` changes.

#### A4. GridSearchCV (final selection)

- Uses `class_weight='balanced'` which is appropriate for imbalanced labels.
- Selects `C=100` with best mean ROC AUC.

### B. Key results

- Baseline validation ROC AUC: **0.8233**
- Best CV ROC AUC (GridSearch): **0.8401**
- Validation ROC AUC (final model): **0.8472**
- Validation F1 (final model): **0.6903**

### C. What is the final outcome?

- A tuned **Logistic Regression** classifier (with `class_weight='balanced'` and `C=100`).
- A production-ready artifact:
  - `classification_model.bin` containing both model and feature vectorizer.

### D. Notes / Potential improvements

- Consider evaluating on the held-out **test set** (currently the notebook evaluates on validation).
- Consider adding probability calibration if using probabilities for decision-making.
- Try tree-based models (e.g., XGBoost classifier) as a comparison baseline.
- Track metrics at multiple thresholds (0.5, best-F1 threshold, business threshold like 0.8).


### Evaluation Metrics

-   **F1 Score**

-   **ROC-AUC**

-   **Confusion Matrix**

-   **Precision & Recall**


* * * * *

6\. **Abandoned Project** - CNN Project for Premium/Non-Premium Classification
----------------------------------------------

The primary objective was to automatically categorize real estate property images as either "Premium" or "Non-Premium" based on learned visual features. The project encompassed a complete machine learning pipeline, from dataset construction and label engineering to model implementation and performance assessment.

**Methodology**

**Data Acquisition and Preprocessing**\
The initial phase involved constructing a labeled image dataset from a source dataset containing property listings. The preprocessing and labeling pipeline was executed as follows:

- **Data Cleaning:** The raw dataset was cleansed to handle missing or inconsistent entries.

- **Neighborhood Encoding:** Categorical `Neighborhood` data was converted into a machine-readable format.

- **Label Generation (Premium/Non-Premium):** A heuristic rule-based system was implemented to generate ground truth labels. For each distinct neighborhood:

o The 75th percentile was calculated for both listing price and review ratings.

o Any property exceeding both the price and rating thresholds for its neighborhood was assigned a "Premium" label (`1`). All other properties were labeled "Non-Premium" (`0`).

- **Image Dataset Compilation:** Using image URLs associated with each property, a balanced sample of approximately 300 images was downloaded and systematically stored in separate directories corresponding to their assigned `Premium` or `Non-Premium` class.

**Model Architecture and Training**\
A supervised learning approach was adopted using TensorFlow and Keras.

- **Data Pipeline:** Images were loaded, resized, normalized, and split into distinct training and validation subsets to facilitate model training and prevent overfitting.

- **Base Model & Transfer Learning:** The EfficientNetB0 architecture, pre-trained on the ImageNet dataset, was employed as a foundational feature extractor. This approach leverages learned hierarchical features from a large corpus of general images.

- **Custom Classification Head:** On top of the frozen base model, a custom classification head was appended:

o A global average pooling layer condensed the extracted feature maps.

o A Dense layer with a ReLU activation function introduced non-linearity.

o A final Dense layer with a sigmoid activation function produced a probabilistic output between 0 and 1, corresponding to the `Non-Premium` and `Premium` classes, respectively.

- **Training Configuration:** The model was compiled using the Adam optimizer and binary cross-entropy loss function, suitable for binary classification tasks. It was subsequently fit on the training data, with performance monitored on the held-out validation set.

**Evaluation and Analysis**\
A separate test set of approximately 100 images (containing a mix of both classes) was compiled to evaluate the model's generalizability.

- **Prediction:** The trained model generated prediction probabilities for each test image.

- **Performance Metrics:** A comprehensive evaluation was conducted by analyzing the Confusion Matrix and Classification Report (precision, recall, F1-score) across various classification thresholds.

- **Threshold Selection:** A classification threshold of 0.6 was empirically determined to offer an optimal balance of metrics. At this threshold, the model demonstrated satisfactory accuracy, recall, and precision for the `Non-Premium` class, and acceptable, though less robust, performance for the `Premium` class.

**Conclusion and Future Work**

The implemented CNN classifier successfully established a baseline for image-based property categorization. However, the final model performance, particularly regarding the `Premium` class, did not meet the target thresholds for reliable deployment. The heuristic labeling strategy, while practical, may not have generated sufficiently robust or accurate ground truth labels, directly impacting the model's learning capability. Furthermore, the limited size of the training dataset likely constrained the model's ability to learn discriminative features effectively.

In essence,

- Leveraged the Place365 Dataset but the data size was huge and required large disk space. (~30 GB). Could not process the same on Google Colab for the same reason

- Tried Tensorflow Datasets place365_small which was also relatively large and processing was still a challenge.

- Even after setting the above, the prediction results were not great.

Despite the implementation of state-of-the-art CNN architectures, the heuristic method of labeling (based on price/review thresholds) introduced significant noise into the training labels. Due to the suboptimal convergence and limited predictive power observed during this phase, the decision was made to pivot the research focus toward a more viable project scope.


* * * * *

## 7. CNN Project to identify Room Type - Multi class identification with Softmax function

## Airbnb Vienna — CNN Room Type Classification (EfficientNet)

This document summarizes the workflow implemented in:

- `Notebook/airbnb_cnn_roomtype_classification.ipynb`

The notebook builds an **image classifier** for predicting the **room type** from photos using **transfer learning** with EfficientNet.

---

## Problem Statement

Airbnb-style listings often include many indoor photos. Automatically identifying the **type of room** (e.g., `kitchen`, `livingroom`, `dining_room`, etc.) enables:

- Better listing understanding and content organization
- Automatic tagging/search/filtering
- Downstream analytics (e.g., “Which room photos correlate with higher prices?”)
- Potential quality checks (e.g., missing required room images)

### Task

- **Type**: Multi-class image classification
- **Input**: A room image
- **Output**: One of **18 room classes**

Classes used (from the dataset folder structure):

- `closet`, `computerroom`, `corridor`, `dining_room`, `elevator`, `gameroom`, `garage`, `gym`, `kitchen`, `livingroom`, `lobby`, `meeting_room`, `office`, `pantry`, `restaurant`, `restaurant_kitchen`, `tv_studio`, `waitingroom`

---

## Dataset & Data Loading

The dataset is stored as an image directory dataset with this structure:

- `../data_room_classifier/train/<class_name>/*.jpg`
- `../data_room_classifier/test/<class_name>/*.jpg`

The notebook uses `tf.keras.preprocessing.image_dataset_from_directory`:

- `IMG_SIZE = (224, 224)`
- `BATCH_SIZE = 32`
- `label_mode = "categorical"` (one-hot labels)

Observed dataset sizes (as printed in the notebook run):

- **Train**: 3861 images
- **Test**: 621 images
- **Classes**: 18

### Notes on “analysis” for image datasets

The primary “EDA” for an image classification dataset usually includes:

- Checking class list consistency between train and test
- Confirming counts per class (imbalance)
- Visual inspection of sample images per class
- Checking resolution, aspect ratio, and common artifacts

In this notebook, the key dataset verification step is:

- `train_ds.class_names` and `test_ds.class_names` match exactly

---

## Data Cleaning & Preprocessing

For CNN-based classification, “cleaning” is primarily about ensuring consistent input tensors and handling variability.

###  Resizing / batching

Images are resized to `224x224` and batched.

### Normalization

The model uses:

- `tf.keras.applications.efficientnet.preprocess_input`

This applies EfficientNet-compatible preprocessing to input tensors.

### Data augmentation

A strong augmentation pipeline is applied during training:

- Random horizontal flip
- Random rotation (0.1)
- Random zoom (0.1)
- Random contrast (0.1)

This helps reduce overfitting and improves generalization on varied room photos.

---

## Algorithm / Model Architecture

### Transfer learning backbone: EfficientNetB0

The notebook uses:

- `EfficientNetB0(include_top=False, weights="imagenet", input_shape=(224,224,3))`

This means:

- The pretrained EfficientNet convolutional base is reused
- A custom classification head is trained for the 18 classes

###  Classification head

A Sequential model is constructed:

1. `data_augmentation`
2. `EfficientNetB0` base model
3. `GlobalAveragePooling2D`
4. `Dense(256, relu)`
5. `Dropout(0.5)`
6. `Dense(NUM_CLASSES, softmax)`

### Loss and optimizer

Compiled with:

- **Loss**: `categorical_crossentropy`
- **Optimizer**: Adam
  - Initial stage learning rate: `1e-3`
  - Fine-tuning stage learning rate: `1e-4`
- **Metric**: accuracy

---

## Training Strategy

The notebook uses a two-stage training approach.

###  Stage 1: Train only the head (frozen backbone)

- `base_model.trainable = False`
- Train for `EPOCHS = 15`

Observed results during this stage:

- Validation accuracy rises quickly and stabilizes around **~0.80**
- Final epoch shown: **val_accuracy ~ 0.8084**

### Stage 2: Fine-tuning (unfreeze top EfficientNet layers)

Fine-tuning configuration:

- `base_model.trainable = True`
- Freeze all but the top ~50 layers:
  - `for layer in base_model.layers[:-50]: layer.trainable = False`
- Re-compile with smaller LR `1e-4`
- Train for `fine_tune_epochs = 10`

Observed results in fine-tuning:

- Accuracy on train increases substantially (up to ~0.94 shown)
- Validation accuracy remains around **~0.81**

Interpretation:

- Fine-tuning improves fit on training data.
- Validation accuracy does not improve dramatically, indicating limited generalization gains (likely due to dataset size, class imbalance, or visual similarity between classes).

---

##  Evaluation & Results

The notebook evaluates using:

- `classification_report` (precision/recall/F1 per class)
- Confusion-matrix-style analysis via predictions over `test_ds`

###  Overall performance

From the printed `classification_report`:

- **Accuracy**: **0.81** (621 test images)
- **Macro avg F1**: **0.79**
- **Weighted avg F1**: **0.81**

###  Class-level observations (selected)

Strong classes (high precision/recall):

- `closet`: very high performance
- `kitchen`: strong (precision ~0.80, recall ~0.92)
- `pantry`: very high
- `gym`: very high

Weaker classes (low support and/or visually ambiguous):

- `corridor`, `office`, `computerroom`

These have small support counts and may require:

- More data
- Better class definitions
- Additional augmentation
- Potential merging of similar classes

---

## Exporting the Model

###  Keras model export

The notebook saves the trained Keras model to:

- `../_models/cnn_room_classifier_effnet.keras`

This is the artifact later used for inference.

### Inference tests on sample images

The notebook tests predictions on local sample images such as:

- `living_room.jpg`
- `dining_room.jpg`
- `Kitchen.jpg`, `Kitchen1.jpg`, `Kitchen2.jpg`

Example outcomes shown:

- `Kitchen.jpg` -> predicted `kitchen` with very high confidence (~99%+)
- Some non-kitchen images show lower confidence and confusion (expected with similar indoor scenes).

---

## ONNX Conversion & ONNX Runtime Testing

The notebook attempts ONNX export using `tf2onnx`:

- Loads the Keras model
- Wraps a serving function
- Converts with `opset=13`

Output path (as shown):

- `../_models/cnn_room_classifier_effnet_fixed.onnx`

Then it tests ONNX inference using `onnxruntime.InferenceSession`.

### Important note

The ONNX model used for runtime inference in the notebook is:

- `../_models/cnn_room_classifier_effnet.onnx`

The notebook also uses a multi-input feed for EfficientNet normalization nodes:

- `input`
- `.../Sub/y:0` (mean)
- `.../Sqrt/x:0` (std)

This explains why ONNX inference needs extra inputs beyond the image tensor.

---

# Takeaways

## Key takeaways

- **Transfer learning works well** on a moderate-sized dataset: ~0.81 test accuracy across 18 classes.
- **Data augmentation** is essential for robustness.
- Fine-tuning improves training accuracy strongly but yields **limited validation gains**, suggesting dataset constraints.
- Some classes are easy (`kitchen`, `closet`, `pantry`), while others are **hard/ambiguous** (`corridor`, `office`, `computerroom`).

## Practical improvements (next iterations)

- Add class distribution analysis + class weights (import exists but not used in training loop).
- Introduce a clearer train/val split (currently test set is used as validation during training).
- Use callbacks:
  - `EarlyStopping`
  - `ReduceLROnPlateau`
  - `ModelCheckpoint`
- Consider increasing input size (e.g., 256/299) if compute allows.
- Consider cleaning/standardizing the ONNX export so the deployed ONNX model has a single input tensor (or document the required extra inputs clearly).



8\. Converting Jupyter Notebooks with Jupytext
----------------------------------------------

To ensure reproducibility and clean pipelines, notebooks were converted to scripts using **Jupytext**.

### Install Jupytext

`pip install jupytext `

### Convert Notebooks

`jupytext --to py notebooks/airbnb_regression.ipynb
jupytext --to py notebooks/airbnb_classification.ipynb `

### Generated Scripts

-   `airbnb_regression.py`

-   `airbnb_classification.py`

* * * * *

9\. Requirements and Installation
---------------------------------

`requirements.txt`


- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- jupytext
- fastapi
- uvicorn
- pydantic
- joblib
- requests 
'''

* * * * *

10\. FastAPI Deployment and Serving
----------------------------------

### Run API Locally

`uvicorn api.app:app --host 0.0.0.0 --port 8000 `

### Available Endpoints

| Endpoint | Description |
| --- | --- |
| `/predict_price` | Predict nightly price |
| `/predict_superhost` | Predict Superhost |
| `/health` | Health check |


* * * * *

11\. Docker Deployment
---------------------

### Build Docker Image

`docker build -t mlcampfinal:latest .

### Run Container

`docker run -p 8000:8000 mlcampfinal:latest `

* * * * *

12\. Kubernetes Deployment
-------------------------

### Kubernetes Manifests

Create `Kubernetes/` directory with the following files:

#### 1\. Deployment Configuration

yaml

# k8s/deployment.yaml

```
yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: airbnb-vienna-deployment
  labels:
    app: airbnb-vienna
spec:
  replicas: 1
  selector:
    matchLabels:
      app: airbnb-vienna
  template:
    metadata:
      labels:
        app: airbnb-vienna
    spec:
      containers:
      - name: airbnb-model-api
        image: mlcampfinal:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000 
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

#### \. Service Configuration

```
yaml

apiVersion: v1
kind: Service
metadata:
  name: airbnb-vienna-service
spec:
  selector:
    app: airbnb-vienna 
  ports:
    - protocol: TCP
      port: 8000         
      targetPort: 8000  
```


### Deployment Commands

```
bash

# minikube install and start with Docker as driver
minikube start --driver=docker

#minikube image load with Docker contents
minikube image build -t mlcampfinal:latest .

# Apply Kubernetes configurations
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment status
kubectl get pods
```

#### Kubectl port forward for the client to access

```
kubectl port-forward service/airbnb-vienna-service 8000:8000
```


### Testing Kubernetes Deployment


#### Test API endpoint
'''
python api_client.py
'''

### Screenshots

#### Minikube Start with Docker driver
<img width="1144" height="296" alt="image" src="https://github.com/user-attachments/assets/7e35519f-452c-49a4-bd9d-75cea7ca1aa1" />
#### Minikube Image ls to show the loaded Docker image into Minikube Cache
<img width="615" height="254" alt="image" src="https://github.com/user-attachments/assets/1c4ad594-2259-42e0-b2c6-6754388ebbe1" />
#### Before Deployment
<img width="887" height="103" alt="image" src="https://github.com/user-attachments/assets/578dc60d-eaac-4aff-9dde-3079e870a472" />
#### Applying YAMLs 
<img width="672" height="101" alt="image" src="https://github.com/user-attachments/assets/1a8e501d-4e24-4a01-82a1-80d148dcac9f" />
#### After Deployment
<img width="1067" height="343" alt="image" src="https://github.com/user-attachments/assets/8fbc8372-ccd0-41b4-84d7-636ec1a07470" />
#### Running the port forward for the API client to hit
<img width="717" height="104" alt="image" src="https://github.com/user-attachments/assets/2052bbbb-3aa8-45f0-a0f6-ec7441f60f71" />

#### Regression run from Api Client
<img width="1440" height="356" alt="image" src="https://github.com/user-attachments/assets/63fc3ac1-16b9-455b-aff6-ebfd46ca199f" />

#### Classification run from Api Client for Superhost
<img width="640" height="211" alt="image" src="https://github.com/user-attachments/assets/6cce9029-72a8-4aed-b9db-acf95cd8edcd" />

#### Identifying the Room type - With Model stored in Keras format
<img width="720" height="193" alt="image" src="https://github.com/user-attachments/assets/90809c10-e499-487f-9ff8-9c7ac1760d44" />

#### Identifying the Room type - With Model stored in ONNX format
<img width="974" height="532" alt="image" src="https://github.com/user-attachments/assets/ac5a4cfb-590c-4fed-b230-46e1e981a25f" />








* * * * *

13\. Project Characterestics
-----------------------

### Business Impact

-   **Price Optimization**: Helps hosts maximize revenue

-   **Market Analysis**: Identifies factors affecting pricing

-   **User Experience**: Better search and filtering for guests

### Technical Achievements

-   **Model Performance**: XGBoost achieved 0.809 R² (regression) and 0.834 accuracy (classification)

-   **Scalability**: Containerized deployment with auto-scaling

-   **Maintainability**: Modular code structure with comprehensive documentation

### Future Improvements

1.  **Real-time Features**: Incorporate seasonal demand data

2.  **Ensemble Methods**: Stacking/blending multiple models

3.  **A/B Testing**: Deploy new models with canary releases

4.  **Feature Store**: Implement for consistent feature engineering

5.  **MLOps Pipeline**: Automated retraining and monitoring

* * * * *

14\. Project Highlights
-----------------------

-   End-to-end ML lifecycle

-   Public dataset with real-world complexity

-   Multiple models with comparative evaluation

-   Reproducible pipelines

-   Production-ready deployment (FastAPI + Docker + Kubernetes)

* * * * *

15\. Contributing
-----------------

1.  Fork the repository

2.  Create a feature branch

3.  Add tests for new functionality

4.  Ensure all tests pass

5.  Submit a pull request


* * * * *

## 16. Evaluation 


---

# 🧠 Project Evaluation Rubric

## **Problem Description**

| Points | Description                                                                                                             | Status |
| :----: | :---------------------------------------------------------------------------------------------------------------------- | :----: |
|    0   | Problem is not described                                                                                                |        |
|    1   | Problem is described in README briefly without much details                                                             |    |
|    2   | Problem is described in README with enough context, so it's clear what the problem is and how the solution will be used |   ✅   |

---

## **Exploratory Data Analysis (EDA)**

| Points | Description                                                                                                                                                                                                       | Status |
| :----: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----: |
|    0   | No EDA                                                                                                                                                                                                            |        |
|    1   | Basic EDA (looking at min–max values, checking for missing values)                                                                                                                                                |    |
|    2   | Extensive EDA (ranges of values, missing values, analysis of target variable, feature importance analysis). <br>For images: analyzing the content of the images. <br>For texts: frequent words, word clouds, etc. |  ✅   |

---

## **Model Training**

| Points | Description                                                                                                                                                           | Status |
| :----: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----: |
|    0   | No model training                                                                                                                                                     |        |
|    1   | Trained only one model, no parameter tuning                                                                                                                           |        |
|    2   | Trained multiple models (linear and tree-based). For neural networks: tried multiple variations – with dropout or without, with extra inner layers or without         |    |
|    3   | Trained multiple models and tuned their parameters. For neural networks: same as previous, but also with tuning (learning rate, dropout rate, inner layer size, etc.) |  ✅   |

---

## **Exporting Notebook to Script**

| Points | Description                                                       | Status |
| :----: | :---------------------------------------------------------------- | :----: |
|    0   | No script for training a model                                    |        |
|    1   | The logic for training the model is exported to a separate script |    ✅   |

---

## **Reproducibility**

| Points | Description                                                                                                                                                                                     | Status |
| :----: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----: |
|    0   | Not possible to execute the notebook and the training script. Data is missing or not easily accessible                                                                                          |        |
|    1   | It's possible to re-execute the notebook and the training script without errors. The dataset is committed in the project repository or there are clear instructions on how to download the data |    ✅   |

---

## **Model Deployment**

| Points | Description                                                     | Status |
| :----: | :-------------------------------------------------------------- | :----: |
|    0   | Model is not deployed                                           |        |
|    1   | Model is deployed (with Flask, BentoML, or a similar framework) |    ✅   |

---

## **Dependency and Environment Management**

| Points | Description                                                                                                                                  | Status |
| :----: | :------------------------------------------------------------------------------------------------------------------------------------------- | :----: |
|    0   | No dependency management                                                                                                                     |        |
|    1   | Provided a file with dependencies (`requirements.txt`, `Pipfile`, `bentofile.yaml`, etc.)                                                    |    |
|    2   | Provided a file with dependencies **and** used virtual environment. README explains how to install dependencies and activate the environment |  ✅    |

---

## **Containerization**

| Points | Description                                                                                  | Status |
| :----: | :------------------------------------------------------------------------------------------- | :----: |
|    0   | No containerization                                                                          |        |
|    1   | `Dockerfile` is provided or a tool that creates a Docker image is used (e.g., BentoML)       |    |
|    2   | The application is containerized **and** README describes how to build and run the container |  ✅    |

---

## **Cloud Deployment**

| Points | Description                                                                                                            | Status |
| :----: | :--------------------------------------------------------------------------------------------------------------------- | :----: |
|    0   | No deployment to the cloud                                                                                             |        |
|    1   | Documentation clearly describes (with code) how to deploy the service to cloud or Kubernetes cluster (local or remote) |        |
|    2   | Code for cloud/Kubernetes deployment is available, with URL for testing or a video/screenshot of testing it            |   ✅   |

---
