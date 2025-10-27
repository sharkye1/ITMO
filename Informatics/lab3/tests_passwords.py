import unittest
import io
import contextlib

from Informatics_Lab3_Task3 import solve


class TestPasswordChecker(unittest.TestCase):
    """Tests for `solve` in the same style as the provided tests.py.

    Each test captures stdout and compares printed messages.
    """

    # messages from Informatics_Lab3_Task3.py (must match exactly)
    QTY_MSG = "Количество цифр в вашем пароле должно составлять 25."
    MONTH_MSG = "В вашем пароле должен быть указан месяц года."
    SPECIAL_MSG = "В вашем пароле должен быть специальный символ."
    UPPER_MSG = "В вашем пароле должна быть заглавная буква."
    DIGIT_MSG = "Ваш пароль должен содержать цифру."
    LEN_MSG = "Длина вашего пароля должна составлять не менее 5 символов."

    def run_and_get(self, password: str) -> str:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            solve(password)
        return buf.getvalue().strip()

    # 3 correct passwords (no messages printed)
    def test_valid_1(self):
        pw = "Январь!" + "1" * 25
        self.assertEqual(self.run_and_get(pw), "")

    def test_valid_2(self):
        pw = "Май#" + "2" * 25
        self.assertEqual(self.run_and_get(pw), "")

    def test_valid_3(self):
        pw = "Декабрь$" + "3" * 25
        self.assertEqual(self.run_and_get(pw), "")

    # 3 passwords with exactly one failing requirement
    def test_one_error_no_special(self):
        # has 25 digits, month and uppercase, but no special symbol
        pw = "Январь" + "1" * 25
        self.assertEqual(self.run_and_get(pw), self.SPECIAL_MSG)

    def test_one_error_no_upper(self):
        # has 25 digits, month and special, but no uppercase letter
        pw = "январь!" + "1" * 25
        self.assertEqual(self.run_and_get(pw), self.UPPER_MSG)

    def test_one_error_qty_digits(self):
        # has month, uppercase and special, but only 24 digits -> qty error only
        pw = "Январь!" + "1" * 24
        self.assertEqual(self.run_and_get(pw), self.QTY_MSG)

    # 3 passwords with exactly two failing requirements
    def test_two_errors_special_and_upper(self):
        # month present (lowercase), no special, no uppercase, digits=25
        pw = "январь" + "1" * 25
        expected = "\n".join([self.SPECIAL_MSG, self.UPPER_MSG])
        self.assertEqual(self.run_and_get(pw), expected)

    def test_two_errors_month_and_special(self):
        # uppercase present, digits=25, but no month and no special
        pw = "A" + "1" * 25
        expected = "\n".join([self.MONTH_MSG, self.SPECIAL_MSG])
        self.assertEqual(self.run_and_get(pw), expected)

    def test_two_errors_month_and_upper(self):
        # special present, digits=25, but no month and no uppercase
        pw = "!" + "1" * 25
        expected = "\n".join([self.MONTH_MSG, self.UPPER_MSG])
        self.assertEqual(self.run_and_get(pw), expected)

    # 3 passwords with exactly three failing requirements
    def test_three_errors_month_special_upper(self):
        # only digits (25) -> missing month, special, uppercase
        pw = "1" * 25
        expected = "\n".join([self.MONTH_MSG, self.SPECIAL_MSG, self.UPPER_MSG])
        self.assertEqual(self.run_and_get(pw), expected)

    def test_three_errors_qty_special_upper(self):
        # month present (lowercase), but qty !=25 and missing special and uppercase
        pw = "январь" + "1" * 24
        expected = "\n".join([self.QTY_MSG, self.SPECIAL_MSG, self.UPPER_MSG])
        self.assertEqual(self.run_and_get(pw), expected)

    def test_three_errors_qty_month_special(self):
        # uppercase present, qty !=25, missing month and special
        pw = "A" + "1" * 24
        expected = "\n".join([self.QTY_MSG, self.MONTH_MSG, self.SPECIAL_MSG])
        self.assertEqual(self.run_and_get(pw), expected)

    # 2 passwords with four failing requirements
    def test_four_errors_qty_month_special_upper(self):
        # only 24 digits, nothing else -> qty + month + special + upper
        pw = "1" * 24
        expected = "\n".join([
            self.QTY_MSG,
            self.MONTH_MSG,
            self.SPECIAL_MSG,
            self.UPPER_MSG,
        ])
        self.assertEqual(self.run_and_get(pw), expected)

    def test_four_errors_qty_month_special_digit(self):
        # no digits at all (qty mismatch + missing month + missing special + missing digit presence)
        # keep length >=5 and include an uppercase so upper/length are OK
        pw = "Abcde"
        expected = "\n".join([
            self.QTY_MSG,
            self.MONTH_MSG,
            self.SPECIAL_MSG,
            self.DIGIT_MSG,
        ])
        self.assertEqual(self.run_and_get(pw), expected)

    # 1 password that fails all requirements (none satisfied)
    def test_fails_everything(self):
        # short, no uppercase, no digits, no month, no special -> everything fails
        pw = "abc"
        expected = "\n".join([
            self.QTY_MSG,
            self.MONTH_MSG,
            self.SPECIAL_MSG,
            self.UPPER_MSG,
            self.DIGIT_MSG,
            self.LEN_MSG,
        ])
        self.assertEqual(self.run_and_get(pw), expected)


if __name__ == "__main__":
    unittest.main()
