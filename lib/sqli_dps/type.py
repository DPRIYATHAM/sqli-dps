import re


class Types:
    # Numeric types
    @staticmethod
    def number(parameter: str) -> bool:
        """Number: tinyint, smallint, mediumint, int, bigint"""
        try:
            int(parameter)
            return True
        except ValueError:
            return False

    @staticmethod
    def float(parameter: str) -> bool:
        """float: float, double"""
        try:
            float(parameter)
            return True
        except ValueError:
            return False

    @staticmethod
    def decimal(parameter: str) -> bool:
        """decimal: decimal/numeric"""
        pass

    # Date and Time types
    @staticmethod
    def date(parameter: str) -> bool:
        """date: regex YYYY-MM-DD """
        return re.match(r"\d{4}-\d{2}-\d{2}", parameter) is not None

    @staticmethod
    def datetime(parameter: str) -> bool:
        """datetime: regex YYYY-MM-DD HH:MM:SS """
        return re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", parameter) is not None

    @staticmethod
    def timestamp(parameter: str) -> bool:
        pass

    @staticmethod
    def time(parameter: str) -> bool:
        """time: regex HH:MM:SS"""
        return re.match(r"\d{2}:\d{2}:\d{2}", parameter) is not None

    @staticmethod
    def year(parameter: str) -> bool:
        """year: regex YYYY"""
        return re.match(r"\d{4}", parameter) is not None

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

