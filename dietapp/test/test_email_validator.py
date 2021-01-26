import unittest
from dietapp.forms import validate_email_string


class TestEmailValidator(unittest.TestCase):
    def setUp(self):
        self.test_string_empty = ''
        self.test_string_valid = 'test@test.test'
        self.test_string_missing_at_sign = 'testtest.test'
        self.test_string_missing_dot = 'test@testtest'

    def test_valid(self):
        self.assertTrue(validate_email_string(self.test_string_valid))

    def test_empty(self):
        self.assertFalse(validate_email_string(self.test_string_empty))

    def test_missing_at_sign(self):
        self.assertFalse(validate_email_string(self.test_string_missing_at_sign))

    def test_missing_dot(self):
        self.assertFalse(validate_email_string(self.test_string_missing_dot))
