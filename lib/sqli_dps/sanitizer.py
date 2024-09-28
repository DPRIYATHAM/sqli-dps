import os.path
import re
from lib.sqli_dps.type import Types, Obfuscate
import mysql.connector
import json
from lib.sqli_dps.errors import ValidationError


def validators(type):
     types = {
        'tinyint': Types.number, 'smallint': Types.number, 'mediumint': Types.number, 'int': Types.number,
        'bigint': Types.number,
        'float': Types.float, 'double': Types.float,
        'decimal': Types.decimal,  # fix: decimal includes parameter (Form: decimal(n, m))
        'date': Types.date,
        'datetime': Types.datetime,
        'timestamp': Types.timestamp,
        'time': Types.time,
        'year': Types.year,
        'char': Types.char, 'varchar':Types.char
    }
     try:
        return types[type]
     except KeyError:
         return lambda x, y: x


class Schema:
    def __init__(self, database):
        self.database = database
        self.metadata = None

    def __getitem__(self, item):
        assert len(item) == 2, "Expected Table name and column Name"
        type = self.metadata[item[0]][item[1]]
        if "(" in type:
            group = list(re.finditer(r"(?P<type>\w+\s*)\((?P<args>\s*[^()]+\s*\))", type))
            parameters = group[0].groupdict()
            args = (parameters["args"]
             .strip("(")
             .strip(")")
             .split(","))
            return parameters['type'], args
        return type, []

    def load(self):
        metadata_path = os.path.join("config", self.database + '.json')
        if os.path.exists(metadata_path):
            with open(metadata_path) as f:
                self.metadata = json.load(f)
        else:
            raise FileNotFoundError("missing configuration files")

    def set_metadata(self, data):
        with open(os.path.join("config", self.database + '.json'), 'w+') as f:
            json.dump(data, f, indent=True)
        self.metadata = data


class Sanitizier:
    def __init__(self, query: str, table: str, parameters: dict):
        self.con = None
        self.database = None
        self.query = query
        self.table = table
        self.parameters = parameters
        self.schema = None

    def _sanitize(self):
        group = re.finditer(r"(::[a-zA-z0-9_]{1,64}::)", self.query)
        for match in group:
            field_name = match.group().strip("::")
            field_type, args = self.schema[self.table, field_name]
            if validators(field_type)(self.parameters[field_name], args):
                parameter = self.parameters[field_name]
                self.query = self.query.replace(
                    match.group(),
                    '"' + Obfuscate.encode(parameter) + '"' if "char" in field_type or 'text' in field_type else parameter
                )
            else:
                raise ValidationError(field_name, field_type, self.parameters[field_name])
        self.sanitized_query = self.query


    def execute(self,
                connection: mysql.connector.connection_cext.CMySQLConnection) -> mysql.connector.abstracts.MySQLConnectionAbstract:
        cursor = connection.cursor()
        assert connection.database is not None, "No Database Selected"
        self.database = connection.database
        self.con = connection
        self._load_schema()
        self._sanitize()
        # cursor.execute(self.sanitized_query)
        print(self.sanitized_query)
        return cursor

    def _load_schema(self):
        self.schema = Schema(self.database)
        try:
            self.schema.load()
        except FileNotFoundError as f:
            assert self.con.is_connected(), "Connection Failed"
            local_cursor = self.con.cursor()
            _metadata = {}
            local_cursor.execute("show tables")
            for table in local_cursor.fetchall():
                local_cursor.execute(f"describe {table[0]}")
                _metadata[table[0]] = {col[0]: col[1] for col in local_cursor.fetchall()}
            self.schema.set_metadata(_metadata)