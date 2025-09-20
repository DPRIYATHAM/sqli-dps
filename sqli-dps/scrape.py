import pandas as pd

with open("out.txt") as f:
    rows = f.readlines()

data = []
rows = [row.replace("+", ",").strip() for row in rows]
rows = [row.replace("→", ",") for row in rows]
raw_df = [row.split(",") for row in rows]

for row in raw_df:
    row_data = {}
    row_data["feature"] = row[0].strip()
    row_data["classifier"] = row[1].strip()
    row_data["acc"] = row[2].split(":")[1].strip()
    row_data["precision"] = row[3].split(":")[1].strip()
    row_data["recall"] = row[4].split(":")[1].strip()
    row_data["f1"] = row[5].split(":")[1].strip()
    row_data["auc"] = row[6].split(":")[1].strip()
    row_data["training_time"] = row[7].split(":")[1].strip()
    row_data["inference_time"] = row[8].split(":")[1].strip()
    data.append(row_data)

df = pd.DataFrame(data)
df.to_csv('result.csv', index=False)
