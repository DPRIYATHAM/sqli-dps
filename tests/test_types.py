import unittest
from lib.sqli_dps.type import Types


class TestNumber(unittest.TestCase):
    def test_valid_numbers(self):
        valid_cases = [
            "0", "5", "-3", "123", "-4567",
            "1234567890123456789", "-9876543210987654321",
            "12345678901234567890", "-1234567890123456789"
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(Types.number(case, []))

    def test_invalid_numbers(self):
        invalid_cases = [
            "12-34", "", " ",  #
            "123 456", "1,234", "--123",
            "12@34", "56#78", "90%12", "7*89",
            "abcd", "12b34", "-abc", "45fgh67",
            "' OR '1'='1", "1; DROP TABLE users", "' OR 1=1 --",
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(Types.number(case, []))


class TestFloat(unittest.TestCase):

    def test_valid_numbers(self):
        valid_cases = [
            "0", "-3", "123.456", "-456.78", "0.1234567890123456",
            "1234567890.123456789", "-1234567890.987654321",
            "12345.67890123456789", "-12345.6789012345678"
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(Types.float(case, []))

    def test_invalid_numbers(self):
        invalid_cases = [
            "12a.34", "-9.8.7", "3..14",
            "12-34.5", " ", "", ".",
            "123 .456", "1,234.56", "--123.45",
            "12@34.56", "56#78.90", "90%12.34", "7*89.12",
            "abcd.ef", "12b34.56", "-abc.def", "45fgh67.89",
            "' OR '1'='1", "1; DROP TABLE users", "' OR 1=1 --",
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(Types.float(case, []))


class TestDecimal(unittest.TestCase):
    def test_valid_cases(self):
        valid_cases = [
            ["123.45", [5, 2]],
            ["0.99", [3, 2]],
            ["12345", [5, 0]],
            ["1234567890.123", [13, 3]],
            ["0", [1, 0]],
            ["1", [10, 2]]
        ]
        for case, args in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(Types.decimal(case, args))

    def test_invalid_cases(self):
        invalid_cases = [
            ["123.456", [5, 2]],
            ["123456", [5, 2]],
            ["12345.6789", [7, 2]],
            ["123.456", [6, 2]],
            ["12.345", [4, 2]],
            ["123.45", [3, 2]]
        ]
        for case, args in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(Types.decimal(case, args))

    def test_edge_cases(self):
        self.assertTrue(Types.decimal("1.1", [2, 1]))
        self.assertTrue(Types.decimal("99999", [5, 0]))
        self.assertFalse(Types.decimal("1.123", [2, 2]))
        self.assertTrue(Types.decimal("0.0", [2, 1]))


class TestChar(unittest.TestCase):
    def test_valid_cases(self):
        valid_cases = [
            ["abc", [5]],
            ["", [1]],
            ["a", [1]],
            ["hello", [5]]
        ]
        for case, args in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(Types.char(case, args))

    def test_invalid_cases(self):
        invalid_cases = [
            ["abcdef", [5]],
            ["test", [3]],
            ["longstring", [5]]
        ]

        for case, args in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(Types.char(case, args))

    def test_edge_cases(self):
        self.assertTrue(Types.char("", [0]))
        self.assertFalse(Types.char("a", [0]))
        self.assertTrue(Types.char("abcdefghij", [10]))
        self.assertFalse(Types.char("abcdefghijk", [10]))


class TestDate(unittest.TestCase):
    def test_valid_dates(self):
        # Valid dates
        valid_dates = [
            "2024-09-03",
            "2000-01-01",
            "1999-12-31",
            "2024-02-29"
        ]

        for date in valid_dates:
            with self.subTest(date=date):
                self.assertTrue(Types.date(date, []))

    def test_invalid_dates(self):
        # Invalid dates
        invalid_dates = [
            "2024-09-31",
            "2024-02-30",
            "2024-13-01",
            "2024-00-10",
            "2024-09-00",
            "abcd-ef-gh",
            "2024-09-3",
            "2024/09/03"
        ]

        for date in invalid_dates:
            with self.subTest(date=date):
                self.assertFalse(Types.date(date, []))

    def test_edge_cases(self):
        edge_cases = [
            ("0001-01-01", True),
            ("0000-00-00", False),
            ("9999-12-31", True)
        ]

        for date, expected in edge_cases:
            with self.subTest(date=date):
                self.assertEqual(Types.date(date, []), expected, f"Failed for edge case date: {date}")


class TestDatetimeValidation(unittest.TestCase):
    def test_valid_datetimes(self):
        valid = [
            "2024-09-03 14:55:00",
            "2000-01-01 00:00:00",
            "1999-12-31 23:59:59",
            "2024-02-29 12:34:56"  
        ]

        for case in valid:
            with self.subTest(datetime=case):
                self.assertTrue(Types.datetime(case, []))

    def test_invalid_datetimes(self):
        invalid = [
            "2024-09-31 14:55:00",
            "2024-02-30 12:34:56",
            "2024-13-01 00:00:00",
            "2024-00-10 00:00:00",
            "2024-09-01 24:00:00",
            "2024-09-01 23:60:00",
            "2024-09-01 23:59:60",
            "abcd-ef-gh ij:kl:mn",
            "2024-09-03 14:55",
            "2024/09/03 14:55:00",
            "2024-09-03 14:55:00 AM"
        ]

        for case in invalid:
            with self.subTest(datetime=case):
                self.assertFalse(Types.datetime(case, []))
    def test_edge_cases(self):
        edge_cases = [
            ("0001-01-01 00:00:00", True),
            ("9999-12-31 23:59:59", True),
            ("0000-00-00 00:00:00", False)
        ]

        for case, expected in edge_cases:
            with self.subTest(datetime=case):
                self.assertEqual(Types.datetime(case, []), expected)


if __name__ == '__main__':
    unittest.main()
