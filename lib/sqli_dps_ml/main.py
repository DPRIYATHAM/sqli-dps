import token

tokens = token.tokenize("SELECT col1, col2 FROM my_table WHERE col1 = 10;")
print(
    tokens
)  # This will print a list of token names, e.g., ['KEYWORD', 'IDENTIFIER', ...]
