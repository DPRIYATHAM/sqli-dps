import html
import os
import re

import numpy as np
import pandas as pd

csvs = [file for file in os.listdir() if file.endswith(".csv")]
df = pd.read_csv(csvs[0])


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


df = df.dropna()
df["Query"] = df["Query"].str.lower()
df["Query"] = df["Query"].apply(decode_encodings)
df.to_csv("sqliv6.csv", index=False)
