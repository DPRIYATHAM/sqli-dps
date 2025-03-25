import time

import pandas as pd

import sqli_dps

df = pd.read_csv("../sqli_dps/sqliv2cleaned.csv")

start = time.time()
for index, row in df.iterrows():
    try:
        sqli_dps.SQLi.check(row.Sentence)
    except sqli_dps.PotentialSQLiPayload as e:
        if row.Label == 1:
            continue
        else:
            print(row.Sentence)
            exit(1)
end = time.time()

print((end - start) / len(df))
