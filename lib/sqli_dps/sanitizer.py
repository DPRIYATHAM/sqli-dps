import os.path
import re
from lib.sqli_dps.type import Types
import mysql.connector
import json
from lib.sqli_dps.errors import ValidationError

def validators():
    return {
        'tinyint': Types.number,
        'smallint': Types.number,
        'mediumint': Types.number,
        'int': Types.number,
        'bigint': Types.number,
        'float': Types.float,
        'double': Types.float,
        'decimal': Types.decimal,  # fix: decimal includes parameter (Form: decimal(n, m))
        'date': Types.date,
        'datetime': Types.datetime,
        'timestamp': Types.timestamp,
        'time': Types.time,
        'year': Types.year
    }


class Sanitizier:
    def __init__(self, query: str, table:str,  parameters: dict):
        self.con = None
        self.database = None
        self.query = query
        self.table = table
        self.parameters = parameters

    def _sanitize(self):
        self._load_schema()
        group = re.finditer(r"(::[a-zA-z0-9_]{1,64}::)", self.query)
        validator = validators()
        for match in group:
            field_name = match.group().strip("::")
            field_type = self.metadata[self.table][field_name]
            if validator[field_type](self.parameters[field_name]):
                self.query = self.query.replace(match.group(), self.parameters[field_name])
            else:
                raise ValidationError(field_name, field_type, self.parameters[field_name])
        self.sanitized_query = self.query

    def _load_schema(self):
        metadata_path = os.path.join("config", self.database + '.json')
        if os.path.exists(metadata_path):
            with open(metadata_path) as f:
                self.metadata = json.load(f)
        else:
            self._fetch_schema()

    def execute(self, connection:  mysql.connector.connection_cext.CMySQLConnection) -> mysql.connector.abstracts.MySQLConnectionAbstract :
        cursor = connection.cursor()
        assert connection.database is not None, "No Database Selected"
        self.database = connection.database
        self.con = connection
        self._load_schema()
        self._sanitize()
        cursor.execute(self.sanitized_query)
        # print(self.sanitized_query)
        return cursor

    def _fetch_schema(self):
        assert self.con.is_connected(), "Connection Failed"
        local_cursor = self.con.cursor()
        _metadata = {}
        if not os.path.exists("config/"):
            os.mkdir("config")
        local_cursor.execute("show tables")
        for table in local_cursor.fetchall():
            local_cursor.execute(f"describe {table[0]}")
            _metadata[table[0]] = {col[0]: col[1] for col in local_cursor.fetchall()}
        with open(os.path.join("config", self.con.database + '.json'), 'w+') as f:
            json.dump(_metadata, f, indent=True)
        self.metadata = _metadata




