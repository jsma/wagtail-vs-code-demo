import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")
django.setup()

from django.test import TestCase


class HomeTestCase(TestCase):
    def test_number_one(self):
        self.assertEqual(1, 1)
