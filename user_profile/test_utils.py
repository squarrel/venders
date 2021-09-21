from django.test import TestCase
from user_profile.utils import count_change


class TestUtils(TestCase):
    def test_count_change(self):
        amount = 543
        result = count_change(amount)
        expected_coins = {
            '100': 5,
            '50': 0,
            '20': 2,
            '10': 0,
            '5': 0
        }
        expected_remainder = 3

        self.assertEqual(result, (expected_coins, expected_remainder))
