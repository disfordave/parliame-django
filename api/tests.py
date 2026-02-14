from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Country, Chamber, Party, Poll, PollResult


class CountryTests(TestCase):
    def test_create_country(self):
        belgium = Country.objects.create(code="be", name="Belgium", emoji="🇧🇪")
        self.assertEqual(belgium.code, "be")


class DataIntegrityTests(TestCase):
    def setUp(self):
        self.be = Country.objects.create(code="be", name="Belgium", emoji="🇧🇪")
        self.fr = Country.objects.create(code="fr", name="France", emoji="🇫🇷")

        self.be_chamber = Chamber.objects.create(
            slug="be-federal",
            country=self.be,
            name="Federal Parliament",
            short_name="Fed",
            total_seats=150,
        )

        self.party_be = Party.objects.create(
            slug="be-nva",
            country=self.be,
            name="N-VA",
            short_name="N-VA",
            colour="#FFFF00",
            position=5,
        )
        self.party_fr = Party.objects.create(
            slug="fr-enmarche",
            country=self.fr,
            name="En Marche",
            short_name="LREM",
            colour="#FF0000",
            position=5,
        )

        self.poll = Poll.objects.create(
            slug="be-poll-1",
            name="Election 2024",
            chamber=self.be_chamber,
            date="2024-06-09",
        )

    def test_poll_result_valid_country(self):
        result = PollResult(poll=self.poll, party=self.party_be, seats=10)
        try:
            result.full_clean()
            result.save()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for valid country!")

    def test_poll_result_invalid_country(self):
        result = PollResult(poll=self.poll, party=self.party_fr, seats=10)

        with self.assertRaises(ValidationError) as cm:
            result.full_clean()
            result.save()

        self.assertIn("Party must belong to the same country", str(cm.exception))


class APITests(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(code="be", name="Belgium")
        self.chamber = Chamber.objects.create(
            slug="be-fed",
            country=self.country,
            name="Fed",
            short_name="Fed",
            total_seats=150,
        )
        self.party = Party.objects.create(
            slug="be-ps",
            country=self.country,
            name="Parti Socialiste",
            short_name="PS",
            colour="red",
            position=2,
        )

        self.admin_user = self.client.post(
            "/admin/", {"username": "admin", "password": "password"}
        )

    def test_create_poll_via_api(self):
        url = reverse("poll-list")
        data = {
            "slug": "be-new-poll",
            "name": "New Poll",
            "chamber": "be-fed",
            "type": "poll",
            "date": "2025-01-01",
            "official": False,
            "results": [{"party": "be-ps", "seats": 25, "vote_share": 15.5}],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
