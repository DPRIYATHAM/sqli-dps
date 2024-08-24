import unittest
import mysql.connector
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
                self.assertTrue(Types.number(case))

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
                self.assertFalse(Types.number(case))


class TestFloat(unittest.TestCase):

    def test_valid_numbers(self):
        valid_cases = [
            "0", "-3", "123.456", "-456.78", "0.1234567890123456",
            "1234567890.123456789", "-1234567890.987654321",
            "12345.67890123456789", "-12345.6789012345678"
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(Types.float(case))

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
                self.assertFalse(Types.float(case))


if __name__ == '__main__':
    unittest.main()
