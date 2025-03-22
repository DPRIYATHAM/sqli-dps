import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import sql_tokenizer  # Assuming this module contains your custom tokenize method

np.set_printoptions(precision=5)
pd.set_option("display.float_format", "{:.5f}".format)

files = os.listdir()
csvs = [file for file in files if file.endswith(".csv")]
dfs = [pd.read_csv(csv, encoding="utf-16") for csv in csvs]

drop_keys = data.keys()[2:]
data = data.drop(drop_keys, axis=1)
data = data.dropna()
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    data["Query"], data["Label"], test_size=0.2, random_state=42
)

# Create a pipeline that vectorizes the text using your custom tokenizer and then applies a RandomForest classifier.
pipeline = Pipeline(
    [
        ("tfidf", TfidfVectorizer(tokenizer=sql_tokenizer.tokenize, lowercase=False)),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]
)

"""
* RandomForestClassifier
* SVC
* PassiveAggressive
* XGBoost
* OneVsRest
"""

# Train the classifier
pipeline.fit(X_train, y_train)

# Evaluate the classifier on the test set
y_pred = pipeline.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0, digits=5))

joblib.dump(pipeline, "model.pkl")
