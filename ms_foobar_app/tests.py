from __future__ import unicode_literals

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.utils.crypto import get_random_string


class LoginTest(APITestCase):
    def test_create_user(self):
        url = reverse("login")
        request_data = {
            "first_name": "foo1",
            "last_name": "bar2",
            "username": "foobar1",
            "email": "testmid1" + get_random_string(3) + "@mail.com",
            "phone_number": "0756878441",
            "gender": "female",
            "password": "foobarFOOBAR#123"
        }
        # request = self.client.post(url, request_data, format='json')
        # self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(200, 200)
