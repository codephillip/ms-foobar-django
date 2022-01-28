import random

from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from django_currentuser.middleware import get_current_user

from ms_foobar_app.constants import PHONE_NUMBER_REGEX
from ms_foobar_django.settings import LOGIN_CODE_VALIDATION_MINUTES_WINDOW


def default_email():
    return get_random_string(length=8) + "@mail.com"


class User(AbstractUser):
    ADMIN = 'admin'
    APPLICANT = 'applicant'
    RECORDS_OFFICER = 'records officer'
    ACCOUNTANT = 'accountant'
    DATA_OFFICER = 'data officer'
    REGISTRAR = 'registrar'
    ROLE_CHOICES = [
        (ADMIN, ADMIN),
        (APPLICANT, APPLICANT),
        (RECORDS_OFFICER, RECORDS_OFFICER),
        (ACCOUNTANT, ACCOUNTANT),
        (DATA_OFFICER, DATA_OFFICER),
        (REGISTRAR, REGISTRAR)
    ]
    FEMALE = 'female'
    MALE = 'male'
    GENDER_CHOICES = [
        (FEMALE, FEMALE),
        (MALE, MALE)
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, default=default_email)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True, validators=[
        RegexValidator(
            regex=PHONE_NUMBER_REGEX,
            message='Wrong phone number format',
        )
    ])
    role = models.CharField(max_length=15, choices=ROLE_CHOICES,
                            null=True, blank=True, default=APPLICANT)
    created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              null=True, blank=True, default=FEMALE)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.UUIDField(null=True, blank=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["role", "username"]

    class Meta:
        db_table = "user"

    @property
    def resend_code(self):
        try:
            return VerificationLoginToken.objects.filter(user_id=self.id).first().id
        except Exception as e:
            print(e)
            return ""

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if not user.is_anonymous:
                self.updated_by = user.id
                self.updated_at = timezone.now()
        except Exception as e:
            print(e)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + str(self.id) + self.role


def generate_expiry_date():
    now = timezone.now()
    return now + timezone.timedelta(minutes=LOGIN_CODE_VALIDATION_MINUTES_WINDOW)


def generate_random_token():
    return str(random.randint(100000, 999999))


class VerificationLoginToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(default=generate_random_token, max_length=6)
    expiry_date = models.DateTimeField(default=generate_expiry_date)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']


class PhoneOrEmailBackend(object):
    """
    Custom backend to perform phone or email authentication
    """

    def authenticate(self, username=None, password=None):
        model = get_user_model()
        try:
            user = model.objects.get(email=username)
            if user.check_password(password):
                return user  # return user on valid credentials
        except model.DoesNotExist:
            return None
        except:
            return None

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None


def deactivate_user(sender, instance, created, update_fields, **kwargs):
    """
    Users are deactivated by default until they verify their phone number except admins
    """
    if created and instance.role != User.ADMIN:
        instance.is_active = False
        instance.save(update_fields=['is_active'])


post_save.connect(deactivate_user, sender=User)
