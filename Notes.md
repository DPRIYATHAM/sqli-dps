# Notes, References for SQLi DPS

1. **Signature-Based Detection Example**: This approach matches incoming queries against known SQL injection patterns using regular expressions.

    ```python
    import re

    # Example SQL query
    user_input = "SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'password'"

    # Common SQLi attack patterns
    sqli_patterns = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",          # Single quote, comment, or hash
        r"(\%22)|(\")|(\%3B)|(;)",                # Double quote or semicolon
        r"(\%6F)|(\%4F)|(\%52)|(\%72)|(\%3D)|=",  # 'or' or '='
        r"(\%28)|(\%29)|(\%30)|(\%31)|(\%32)|(\%33)|(\%34)|(\%35)|(\%36)|(\%37)|(\%38)|(\%39)|\d",  # Numbers
    ]

    # Check if the input matches any known SQLi patterns
    def detect_sqli(query):
        for pattern in sqli_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                print("Possible SQL Injection detected!")
                return True
        return False

    # Use the function
    if detect_sqli(user_input):
        print("SQL query is potentially dangerous!")
    else:
        print("SQL query seems safe.")
    ```

2. **Anomaly-Based Detection Example**: This method involves comparing the current query against "normal" queries to detect deviations that might indicate SQL injection.

    ```python
    def detect_anomalies(query, normal_queries):
        # Compare the query length with the average of normal queries
        average_length = sum(len(q) for q in normal_queries) / len(normal_queries)
        if abs(len(query) - average_length) > 20:  # Arbitrary threshold
            print("Anomalous query detected based on length!")
            return True

        # Additional checks for unusual patterns can be added here
        # Example: checking for too many OR statements, etc.

        return False

    # Example usage
    normal_queries = [
        "SELECT * FROM users WHERE username = 'user1' AND password = 'pass1'",
        "SELECT * FROM users WHERE username = 'user2' AND password = 'pass2'"
    ]

    user_query = "SELECT * FROM users WHERE username = 'admin' OR 1=1 --"

    if detect_anomalies(user_query, normal_queries):
        print("SQL query seems anomalous!")
    else:
        print("SQL query seems normal.")
    ```

3. **Input Validation Example**: This approach sanitizes user inputs to prevent malicious SQL code from being executed.

    ```python
    def sanitize_input(user_input):
        # Basic input sanitization
        user_input = user_input.replace("'", "''")  # Escape single quotes
        return user_input

    # Example usage
    user_input = "admin' OR 1=1 --"
    sanitized_input = sanitize_input(user_input)

    query = f"SELECT * FROM users WHERE username = '{sanitized_input}'"
    print("Sanitized SQL Query:", query)
    ```
