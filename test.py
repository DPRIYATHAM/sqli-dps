import pandas as pd

from sqlidps import PotentialSQLiPayload, SQLi

df = pd.read_csv("Modified_SQL_Dataset.csv")

results = []

for _, row in df.iterrows():
    query = row["Query"].lower()
    label = row["Label"]

    system_detected = 0
    try:
        SQLi.check(query)
        system_detected = 0
    except PotentialSQLiPayload:
        system_detected = 1

    results.append({"Query": query, "Label": label, "Detected": system_detected})

results_df = pd.DataFrame(results)

false_positives = results_df[(results_df["Label"] == 0) & (results_df["Detected"] == 1)]
false_negatives = results_df[(results_df["Label"] == 1) & (results_df["Detected"] == 0)]

false_negatives.to_csv("false_negatives.csv")
false_positives.to_csv("false_positives.csv")

print("False Positives:", len(false_positives))
print("False Negatives:", len(false_negatives))
