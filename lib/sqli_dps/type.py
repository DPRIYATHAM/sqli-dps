import re
from datetime import datetime


class Obfuscate:
    chars = ["'", '"', ';', '-', '*', '(', ')', '=', '<', '>', '%', '_', '|', '\\', ',', '@', '#', '`', '^', '~', '&',
             '$', '!', '/']

    @staticmethod
    def encode(string: str):
        for char in Obfuscate.chars:
            string = string.replace(char, f"&{ord(char)};")
        return string

    @staticmethod
    def decode(string: str):
        for char in Obfuscate.chars:
            string = re.sub(r"&%d+;" % ord(char), char, string)
        return string


class Types:
    # Numeric types verified: ✅
    @staticmethod
    def number(parameter: str, args: list) -> bool:
        """Number: tinyint, smallint, mediumint, int, bigint"""
        try:
            int(parameter)
            return True
        except ValueError:
            return False

    @staticmethod
    def float(parameter: str, args: list) -> bool:
        """float: float, double"""
        try:
            float(parameter)
            return True
        except ValueError:
            return False

    @staticmethod
    def decimal(parameter: str, args: list) -> bool:
        """decimal: decimal/numeric"""
        precision, scale = int(args[0]), int(args[1])
        int_part = precision - scale if precision - scale > 0 else 1
        pattern = r'^\d{1,%d}(\.\d{0,%d})?$' % (int_part, scale)
        return bool(re.match(pattern, parameter))

    # Date and Time types
    @staticmethod
    def date(parameter: str, args: list) -> bool:
        """date: YYYY-MM-DD """
        if re.match(r"\d{4}-\d{2}-\d{2}", parameter) is None:
            return False
        try:
            datetime.strptime(parameter, '%Y-%m-%d')
            return True
        except ValueError:
            return False


    @staticmethod
    def datetime(parameter: str, args: list) -> bool:
        """datetime: regex YYYY-MM-DD HH:MM:SS """
        if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", parameter) is None:
            return False
        try:
            datetime.strptime(parameter, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False


    @staticmethod
    def timestamp(parameter: str, args: list) -> bool:
        pass


    @staticmethod
    def time(parameter: str, args: list) -> bool:
        """time: regex HH:MM:SS"""
        return re.match(r"\d{2}:\d{2}:\d{2}", parameter) is not None


    @staticmethod
    def year(parameter: str, args: list) -> bool:
        """year: regex YYYY"""
        return re.match(r"\d{4}", parameter) is not None


    # text types verified: ✅
    @staticmethod
    def char(parameter: str, args: list):
        return len(parameter) <= int(args[0])


# pending types
"""
string {
    char
    varchar
    text: (tinytext, mediumtext, longtext)
    blob: (tinyblob, mediumblob, longblob)
}

binary {
    binary
    varbinary
}

spatial {
    geometry
    point
    linestring
    polygon
    multipoint
    multistring
    multipolygon
    geometrycollection
}

json {
    json
}

enum {
    enum
    set
}
"""
