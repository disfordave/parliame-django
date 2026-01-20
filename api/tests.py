from django.test import TestCase
from .models import Country


class CountryTests(TestCase):
    def test_create_country(self):
        belgium = Country.objects.create(code="be", name="Belgium", emoji="🇧🇪")
        self.assertEqual(belgium.code, "be")
