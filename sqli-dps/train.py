import html
import importlib.util
import os
import re
import sys

import numpy as np
import pandas as pd
import pkg_resources
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def get_package_file(filename: str) -> str:
    return pkg_resources.resource_filename("sqlidps", filename)


def decode_encodings(text: str) -> str:
    assert isinstance(text, str)
    try:
        text = text.replace("\\", "\\\\")
        text = text.encode("utf-8").decode("unicode_escape")
    except Exception as e:
        return ""
    text = re.sub(
        r"%([0-9A-Fa-f]{2})", lambda m: bytes.fromhex(m.group(1)).decode("latin1"), text
    )
    text = re.sub(r"[Uu]\+([0-9A-Fa-f]{4,6})", lambda m: chr(int(m.group(1), 16)), text)
    text = html.unescape(text)
    return text


# moudle_path = get_package_file("sql_tokenizer.so")
module_path = "sql_tokenizer.so"
module_name = "sql_tokenizer"

spec = importlib.util.spec_from_file_location(module_name, module_path)
sql_tokenizer = importlib.util.module_from_spec(spec)
sys.modules[module_name] = sql_tokenizer
spec.loader.exec_module(sql_tokenizer)


def train():
    np.set_printoptions(precision=5)
    pd.set_option("display.float_format", "{:.5f}".format)
    files = os.listdir()
    csvs = [file for file in files if file.endswith(".csv")]
    print(csvs)
    data = pd.read_csv(csvs[0])
    print(data)
    print(data.keys())
    drop_keys = data.keys()[2:]
    data = data.drop(drop_keys, axis=1)
    data = data.dropna()
    data["Query"] = data["Query"].str.lower()
    data["Query"] = data["Query"].apply(decode_encodings)
    X_train, X_test, y_train, y_test = train_test_split(
        data["Query"], data["Label"], test_size=0.2, random_state=42
    )
    pipeline = Pipeline(
        [
            (
                "count_vec",
                CountVectorizer(
                    tokenizer=sql_tokenizer.tokenize,
                    preprocessor=lambda x: x,
                    lowercase=False,
                ),
            ),
            ("tfidf", TfidfTransformer()),
            ("clf", RandomForestClassifier(n_estimators=200)),
        ]
    )
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0, digits=5))
    export_model(pipeline)


def export_model(pipeline, export_path="model.npz"):
    vec = pipeline.named_steps["count_vec"]
    vocab = vec.vocabulary_
    inv_vocab = {i: t for t, i in vocab.items()}
    idf = pipeline.named_steps["tfidf"].idf_

    rf = pipeline.named_steps["clf"]
    classes = rf.classes_
    n_trees = len(rf.estimators_)
    children_left = []
    children_right = []
    feature = []
    threshold = []
    value = []
    for tree in rf.estimators_:
        t = tree.tree_
        children_left.append(t.children_left)
        children_right.append(t.children_right)
        feature.append(t.feature)
        threshold.append(t.threshold)
        value.append(t.value.squeeze(axis=1))

    np.savez(
        export_path,
        inv_vocab=np.array([inv_vocab[i] for i in range(len(inv_vocab))], dtype=object),
        vocabulary_keys=np.array(list(vocab.keys()), dtype=object),
        vocabulary_vals=np.array(list(vocab.values()), dtype=np.int32),
        idf=idf,
        classes=classes,
        children_left=np.array(children_left, dtype=object),
        children_right=np.array(children_right, dtype=object),
        feature=np.array(feature, dtype=object),
        threshold=np.array(threshold, dtype=object),
        value=np.array(value, dtype=object),
    )
    print(f"Exported model components to {export_path}")


if __name__ == "__main__":
    train()
