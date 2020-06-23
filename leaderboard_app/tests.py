# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from leaderboard_app.models import *
from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker

fake = Faker()


class UserGetAPIViewTestCase(APITestCase):

    def setUp(self):
        # valid
        self.display_name = fake.name()
        self.created_user = Player.objects.create(display_name=self.display_name, rank=0, country_iso_code="tr",
                                                  points=0.0)
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
        user_id_str = self.user_id.__str__()
        response = self.client.get(self.valid_url)
        print(response.data)
        self.assertEqual({'user_id': user_id_str, 'display_name': self.display_name, 'rank': 0,
                          'country_iso_code': 'tr', 'points': 0.0}
                         , response.data)
        self.assertEqual(200, response.status_code)


class UserCreateAPIViewTestCase(APITestCase):

    def setUp(self):
        self.rank = 0
        self.display_name = fake.name()
        self.points = 1.23
        self.url = reverse("api:create-user")
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
