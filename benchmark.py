import time
from sqlidps import *

with open("sqli-dps/sqliv6-unbalanced-62-38.csv") as f:
    data = f.readlines()

queries = [query.split(",")[0] for query in data]

start = time.perf_counter()
for query in queries:
    try:
        SQLi.check(query)
    except PotentialSQLiPayload:
        pass
end = time.perf_counter()

print(f"Time per Inference: {((end - start) * 1000) / len(queries):.2f}ms")
