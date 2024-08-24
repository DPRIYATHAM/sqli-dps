# sqli-dps
SQL Injections Detection and Prevention System


## Usage
```python
    con = mysql.connector.connect(host=..., user=..., password=..., database=...)
    query = r"SELECT * FROM Reviews WHERE review_id=::review_id:: and product_id=::product_id::"
    parameters = {
        'review_id': 1,
        'product_id': 1
    }
    cursor = Sanitizier(query=query, table="Reviews", parameters=parameters).execute(con)
```
