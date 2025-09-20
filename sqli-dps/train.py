irport warnings

from pipelines import *
from sklearn.pipeline import Pipeline

warnings.filterwarnings(
    "ignore",
    message="The parameter 'token_pattern' will not be used since 'tokenizer' is not None",
)

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import cross_val_score


def train():
    np.set_printoptions(precision=5)
    pd.set_option("display.float_format", "{:.5f}".format)
    train_df = pd.read_csv("train.csv")
    test_df = pd.read_csv("test.csv")
    X_train, X_test, y_train, y_test = (
        train_df["Query"],
        test_df["Query"],
        train_df["Label"],
        test_df["Label"],
    )

    # feature_cache = {}
    # results = []
    # for f_name, f_pipe in feature_sets.items():
    #     if f_name not in feature_cache:
    #         feature_cache[f_name] = f_pipe.fit_transform(X_train, y_train)
    #     X_feat = feature_cache[f_name]
    #     feature_cache[f_name] = X_feat
    #     for c_name, clf in classifiers.items():
    #         scores = cross_val_score(
    #             clf, X_feat, y_train, cv=5, scoring="accuracy", n_jobs=-1
    #         )
    #         results.append((f_name, c_name, np.mean(scores)))
    #         print(f"{f_name} + {c_name} → Accuracy: {np.mean(scores):.4f}")
    # return results
    pipeline = Pipeline(
        [
            ("feature_pref", feature_sets["Grammer aware TF-IDF with n-gram"]),
            ("clf", classifiers["sqlidps"]),
        ]
    )
    # pipeline.fit(X_train, y_train)
    # y_pred = pipeline.predict(X_test)
    # print("Classification Report:")
    # print(classification_report(y_test, y_pred, zero_division=0, digits=5))
    # tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    # print(f"TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")
    # y_pred = pd.Series(y_pred)
    # failed = test_df[test_df["Label"] != y_pred]
    # failed.to_csv("failed.csv")
    # export_model(pipeline)


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
