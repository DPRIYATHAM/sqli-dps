class ValidationError(Exception):
    def __init__(self, field_name, field_type, field_value):
        super().__init__(f"The parameter {field_value} did not match the type {field_type} for {field_name}")
        self.field_name = field_name
        self.field_type = field_type




