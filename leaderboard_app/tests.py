# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from leaderboard_app.models import *
from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker
import random

fake = Faker()

country_codes = ['TR',
                 'US',
                 'FR',
                 'ES',
                 'IT']


class UserGetAPIViewTestCase(APITestCase):

    def setUp(self):
        # valid
        self.display_name = fake.name()
        self.points = random.randint(5, 150)
        self.created_user = Player.objects.create(display_name=self.display_name, country_iso_code="tr",
                                                  points=self.points)
        self.user_id = self.created_user.user_id
        self.valid_url = reverse("api:get-user", kwargs={"user_id": self.user_id})

        # uuid not exists
        self.user_uuid_not_exists = "e4cdb120-28fc-4285-a78d-eb48660b7730"
        self.uuid_not_exist_url = reverse("api:get-user", kwargs={"user_id": self.user_uuid_not_exists})

        # invalid uuid
        self.user_invalid_uuid = "e4cdb120-28fc-4285-a78d-eb48660b77330"
        self.invalid_uuid_url = reverse("api:get-user", kwargs={"user_id": self.user_invalid_uuid})

    def test_get_user_fail_user_not_exists(self):
        response = self.client.get(self.uuid_not_exist_url)
        self.assertEqual("User Does not Exists", response.data["message"])
        self.assertEqual(404, response.status_code)

    def test_get_user_fail_invalid_uuid(self):
        response = self.client.get(self.invalid_uuid_url)
        self.assertEqual("Provide a valid UUID", response.data["message"])
        self.assertEqual(400, response.status_code)

    def test_get_user_success(self):
        response = self.client.get(self.valid_url)
        self.assertEqual(200, response.status_code)


class UserCreateAPIViewTestCase(APITestCase):

    def setUp(self):
        self.rank = 0
        self.display_name = fake.name()
        self.points = 1.23
        self.url = reverse("api:create-user")
        self.url_bulk = reverse("api:create-user-bulk")
        self.country_iso_code = "TR"

    def test_create_user_success(self):
        data = {"rank": self.rank, "display_name": self.display_name, "points": self.points,
                "country_iso_code": self.country_iso_code}
        response = self.client.post(self.url, data=data)
        self.assertEqual(201, response.status_code)

    def test_create_user_fail_country_code(self):
        data = {"rank": self.rank, "display_name": self.display_name, "points": self.points}
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

    def test_create_user_fail_display_name(self):
        data = {"rank": self.rank, "points": self.points,
                "country_iso_code": self.country_iso_code}
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

    def test_create_user_bulk_success(self):
        data = {"number_of_objects": 20}
        response = self.client.post(self.url_bulk, data=data)
        self.assertEqual(201, response.status_code)


class ScoreAPIViewTestCase(APITestCase):
    def setUp(self):
        self.create_url = reverse("api:score-submit")
        self.display_name = fake.name()
        self.points = random.randint(5, 150)
        self.country_iso_code = "TR"
        self.created_user = Player.objects.create(display_name=self.display_name, country_iso_code="tr",
                                                  points=self.points)

    def test_score_submit_success(self):
        data = {"score_worth": 200, "user_id": self.created_user.user_id}
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(201, response.status_code)

    def test_score_submit_not_exists(self):
        data = {"score_worth": 200, "user_id": "11"}
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(404, response.status_code)


class LeaderBoardAPIViewTestCase(APITestCase):
    def setUp(self):
        self.leaderboard_url_country = reverse("api:leaderboard-redis",
                                               kwargs={"country_iso_code": random.choice(country_codes)})
        self.leaderboard_url = reverse("api:leaderboard-redis",
                                       kwargs={"country_iso_code": ""})
        self.leaderboard_url_pagination = "/leaderboard/FR?limit=" + str(random.randint(1, 100)) + "?offset=" + str(
            random.randint(1, 100))

    def test_leaderboard_get_success(self):
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(200, response.status_code)

    def test_leaderboard_country_get_success(self):
        response = self.client.get(self.leaderboard_url_country)
        self.assertEqual(200, response.status_code)

    def test_leaderboard_pagination_get_success(self):
        response = self.client.get(self.leaderboard_url_pagination)
        self.assertEqual(200, response.status_code)
