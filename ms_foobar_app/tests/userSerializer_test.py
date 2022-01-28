from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from ms_foobar_app.serializers import UserSerializer

from .factories import UserFactory


class UserSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory.create()

    def test_that_a_user_is_correctly_serialized(self):
        user = self.user
        serializer = UserSerializer
        serialized_user = serializer(user).data

        assert serialized_user['id'] == user.id
        assert serialized_user['first_name'] == user.first_name
        assert serialized_user['last_name'] == user.last_name
        assert serialized_user['dob'] == user.dob
        assert serialized_user['phone_number'] == user.phone_number
        assert serialized_user['role'] == user.role
        assert serialized_user['created_at'] == user.created_at
        assert serialized_user['nationality'] == user.nationality
        assert serialized_user['graduation_date'] == user.graduation_date
        assert serialized_user['gender'] == user.gender