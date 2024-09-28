import mysql.connector
from lib.sqli_dps.sanitizer import Sanitizier

if __name__ == "__main__":
    con = mysql.connector.connect(
        host="localhost",
        user="arjun",
        password="arjun2005",
        database="test"
    )
    query = r"SELECT * FROM Products WHERE product_name=::product_name:: and price=::price::"
    parameters = {
        'product_name': "akfla; adfk' --",
        'price': "1"
    }
    cursor = Sanitizier(query, "Products", parameters).execute(con)
    # for row in cursor.fetchall():
    #     print(row)
    #
