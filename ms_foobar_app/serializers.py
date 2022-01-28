from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField
from django.core.exceptions import PermissionDenied

from .constants import INVALID_CODE
from .models import User, VerificationLoginToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.crypto import get_random_string

from .service import initialize_login_token_generation, initialize_login_token_without_password_generation, \
    activate_user_after_verifying_phone_number, delete_old_user_login_codes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'dob', 'phone_number', 'role', 'created_at', 'nationality',
                  'graduation_date', 'email',
                  'gender']


class UserPostSerializer(serializers.ModelSerializer):
    resend_code = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone_number', 'password', 'gender', 'role', 'dob', 'resend_code')

    def create(self, validated_data):
        validated_data['username'] = (validated_data['first_name'] + validated_data[
            'last_name']).lower() + get_random_string(length=4)
        try:
            validated_data['email']
        except Exception as e:
            validated_data['email'] = validated_data['username'] + "@Foobar.co.ug"
        user = User(**validated_data)
        # NOTE: Without this, User will never sign_in and password will not be encrypted
        user.set_password(validated_data['password'])
        user.save()
        initialize_login_token_without_password_generation(user.phone_number or user.email)
        return user


class VerificationLoginTokenSerializer(serializers.Serializer):
    user_field = serializers.CharField()
    password = PasswordField()

    class Meta:
        fields = ('user_field', 'password')

    def save(self):
        print('token generation started')
        initialize_login_token_generation(self.validated_data['user_field'], self.validated_data['password'])


class ResendCodeTokenSerializer(serializers.Serializer):
    resend_code = serializers.CharField()

    class Meta:
        fields = ('resend_code',)

    def save(self):
        print('token generation started')
        try:
            verification_token = VerificationLoginToken.objects.get(id=self.validated_data['resend_code'])
            initialize_login_token_without_password_generation(verification_token.user.phone_number
                                                               or verification_token.user.email)
        except VerificationLoginToken.DoesNotExist:
            raise PermissionDenied(INVALID_CODE)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'] = serializers.CharField()
        del self.fields[self.username_field]
        del self.fields['password']

    def validate(self, attrs):
        """
        Receives the sms code and verifies if its valid, then sends a JWT token with other params
        :param attrs: contains sms code that user receives when they attempt to login
        :return: token and user models dictionary
        """
        try:
            self.user = VerificationLoginToken.objects.get(Q(code=attrs['code']) &
                                                           Q(expiry_date__gte=timezone.now())).user
        except Exception as e:
            print(e)
            raise PermissionDenied(INVALID_CODE)
        return self.generate_response()

    @classmethod
    def get_token(cls, user):
        """
        Generates a token with the provided payload items
        :param user: user object that is being authenticated
        :return: token_payload with generated (refresh)token
        """
        token_payload = super().get_token(user)
        token_payload['role'] = user.role
        return token_payload

    def generate_response(self):
        """
        Generates response composed of the token and some additional model fields
        :param refresh: object containing tokens
        :return: token and user models dictionary
        """
        refresh = self.get_token(self.user)
        data = dict()
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['role'] = self.user.role
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['phone_number'] = self.user.phone_number
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['dob'] = self.user.dob
        data['gender'] = self.user.gender
        activate_user_after_verifying_phone_number(self.user)
        delete_old_user_login_codes(self.user)
        return data
