import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import SVC
from sql_tokenizer import tokenize
from utils import decode_encodings
from xgboost import XGBClassifier


class BoCVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer="char")

    def fit(self, X, y=None):
        return self.vectorizer.fit(X)

    def transform(self, X):
        return self.vectorizer.transform(X)


class Preprocessor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        lower = X.str.lower()
        return lower.apply(decode_encodings)


feature_sets = {
    "BoC only": Pipeline(
        [
            ("preprocess", Preprocessor()),
            ("boc", BoCVectorizer()),
        ]
    ),
    # "TF-IDF word": Pipeline(
    #     [
    #         ("preprocess", Preprocessor()),
    #         ("tfidf", TfidfVectorizer(analyzer="word")),
    #     ]
    # ),
    # "TF-IDF word n-gram": Pipeline(
    #     [
    #         ("preprocess", Preprocessor()),
    #         ("tfidf_ngram", TfidfVectorizer(analyzer="word", ngram_range=(1, 3))),
    #     ]
    # ),
    "Grammer aware TF-IDF": Pipeline(
        [
            ("preprocess", Preprocessor()),
            (
                "count_vec",
                CountVectorizer(
                    tokenizer=tokenize,
                    preprocessor=lambda x: x,
                ),
            ),
            ("tfidf", TfidfTransformer()),
        ]
    ),
    "Grammer aware TF-IDF with n-gram": Pipeline(
        [
            ("preprocess", Preprocessor()),
            (
                "count_vec",
                CountVectorizer(
                    tokenizer=tokenize,
                    preprocessor=lambda x: x,
                    ngram_range=(1, 3),
                ),
            ),
            ("tfidf", TfidfTransformer()),
        ]
    ),
    "Combined features": Pipeline(
        [
            ("preprocess", Preprocessor()),
            (
                "features",
                FeatureUnion(
                    [
                        ("boc", BoCVectorizer()),
                        ("tfidf", TfidfVectorizer(analyzer="word")),
                        (
                            "tfidf_ngram",
                            TfidfVectorizer(analyzer="word", ngram_range=(1, 3)),
                        ),
                    ]
                ),
            ),
        ]
    ),
    "Grammer aware Combined features": Pipeline(
        [
            ("preprocess", Preprocessor()),
            (
                "features",
                FeatureUnion(
                    [
                        ("boc", BoCVectorizer()),
                        (
                            "tfidf_ngram",
                            Pipeline(
                                [
                                    (
                                        "count_vec",
                                        CountVectorizer(
                                            tokenizer=tokenize,
                                            preprocessor=lambda x: x,
                                            ngram_range=(1, 3),
                                        ),
                                    ),
                                    ("tfidf", TfidfTransformer()),
                                ]
                            ),
                        ),
                        (
                            "tfidf",
                            Pipeline(
                                [
                                    ("preprocess", Preprocessor()),
                                    (
                                        "count_vec",
                                        CountVectorizer(
                                            tokenizer=tokenize,
                                            preprocessor=lambda x: x,
                                        ),
                                    ),
                                    ("tfidf", TfidfTransformer()),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ]
    ),
}

classifiers = {
    "proposed-ensemble": Pipeline(
        [
            (
                "vote",
                VotingClassifier(
                    estimators=[
                        ("nb", MultinomialNB()),
                        ("svm", SVC(probability=True)),
                        (
                            "xgb",
                            XGBClassifier(eval_metric="logloss"),
                        ),
                    ],
                    voting="soft",
                ),
            ),
        ]
    ),
    "sqlidps": Pipeline(
        [
            ("rfc", RandomForestClassifier(n_estimators=200)),
        ]
    ),
}
