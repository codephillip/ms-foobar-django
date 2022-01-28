import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import User, VerificationLoginToken
from .factories import UserFactory

faker = Factory.create()


class User_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        UserFactory.create_batch(size=3)

    def test_signup_user(self):
        """
        Ensure we can signup a new user.
        """
        client = self.api_client
        user_count = User.objects.count()
        verification_token_count = VerificationLoginToken.objects.count()
        user_detail_url = reverse('register')
        user_role = "applicant"
        data = {
            "first_name": "foobizz3",
            "last_name": "foobizz4",
            "email": "foobar3@foobizz2.com",
            "phone_number": "+256740456291",
            "password": "foobar#123",
            "gender": "male",
            "role": "applicant",
            "dob": "2000-09-02"
        }
        response = client.patch(user_detail_url, data=data)
        assert User.objects.count() == user_count + 1
        assert VerificationLoginToken.objects.count() == verification_token_count + 1
        assert response.status_code == status.HTTP_201_CREATED
        assert user_role == User.objects.first().role
