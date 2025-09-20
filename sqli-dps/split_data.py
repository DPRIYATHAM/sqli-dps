import argparse

import pandas as pd
from sklearn.model_selection import train_test_split


def split(
    input: str,
    ratio: float,
    test_name: str,
    train_name: str,
    stratify_col: str,
    random_state: int,
) -> None:

    try:
        df = pd.read_csv(input)
        train_df, test_df = train_test_split(
            df, test_size=ratio, stratify=df[stratify_col], random_state=random_state
        )
        train_df.to_csv(train_name, index=False)
        test_df.to_csv(test_name, index=False)
    except FileNotFoundError:
        print(f"file `{input}` not found...")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="use this to split a database into train and test files based on equal distribution of `stratify_col`"
    )
    parser.add_argument(
        "-f", "--file", default="stratified_ready.csv", type=str, help="Input csv file"
    )
    parser.add_argument(
        "-tr", "--test-ratio", default=0.15, type=float, help="Test file ratio"
    )
    parser.add_argument(
        "-ten",
        "--test-file-name",
        default="test.csv",
        type=str,
        help="Test file name",
    )
    parser.add_argument(
        "-trn",
        "--train-file-name",
        default="train.csv",
        type=str,
        help="Train file name",
    )
    parser.add_argument(
        "-s",
        "--stratify-col",
        default="stratify_col",
        type=str,
        help="Name of column to stratified",
    )
    parser.add_argument(
        "-r",
        "--random-state",
        default=42,
        type=int,
        help="Random state for `sklearn.model_selection.train_test_split`",
    )
    args = parser.parse_args()
    split(
        args.file,
        args.test_ratio,
        args.test_file_name,
        args.train_file_name,
        args.stratify_col,
        args.random_state
    )
