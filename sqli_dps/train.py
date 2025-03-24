import importlib.util
import os
import sys

import joblib
import numpy as np
import pandas as pd
import pkg_resources
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def get_package_file(filename: str) -> str:
    return pkg_resources.resource_filename("sqli_dps", filename)


# moudle_path = get_package_file("sql_tokenizer.so")
module_path = "sql_tokenizer.so"
module_name = "sql_tokenizer"

spec = importlib.util.spec_from_file_location(module_name, module_path)
sql_tokenizer = importlib.util.module_from_spec(spec)
sys.modules[module_name] = sql_tokenizer
spec.loader.exec_module(sql_tokenizer)

np.set_printoptions(precision=5)
pd.set_option("display.float_format", "{:.5f}".format)
files = os.listdir()
csvs = [file for file in files if file.endswith(".csv")]
print(csvs)
data = pd.read_csv(csvs[1])
print(data.keys())
drop_keys = data.keys()[2:]
data = data.drop(drop_keys, axis=1)
data = data.dropna()
X_train, X_test, y_train, y_test = train_test_split(
    data["Query"], data["Label"], test_size=0.2, random_state=42
)
pipeline = Pipeline(
    [
        ("tfidf", TfidfVectorizer(tokenizer=sql_tokenizer.tokenize, lowercase=False)),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
        # ("clf", SVC(kernel="linear", C=1.0, random_state=42)),
        # ("clf", PassiveAggressiveClassifier(max_iter=1000, random_state=42)),
        # (
        #     "clf",
        #     OneVsRestClassifier(
        #         SVC(kernel="linear", probability=True, random_state=42)
        #     ),
        # ),
        # ("clf", xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")),
    ]
)

# *RandomForestClassifier
# *SVC
# *PassiveAggressive
# *XGBoost
# *OneVsRest
#


def main():
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0, digits=5))
    joblib.dump(pipeline, "model.pkl")


main()
