from django.core.exceptions import PermissionDenied

from .constants import WELCOME_MESSAGE, TOKEN_MESSAGE, INVALID_CREDENTIALS, EMAIL_TOKEN_SUBJECT, \
    EMAIL_TOKEN_MESSAGE, EMAIL_WELCOME_MESSAGE, EMAIL_WELCOME_SUBJECT, EventSubjects
from .events.event_publisher import EventPublisher
from .models import User, VerificationLoginToken
import requests


def send_sms(phone_number, message):
    try:
        bus = EventPublisher()
        bus.run()
        bus.publish(EventSubjects.SmsNotificationCreated, {
            "message": message,
            "phoneNumbers": [phone_number]
        })
    except Exception as e:
        print(e)


def send_email(recipients, message, subject):
    # todo replace with event bus
    try:
        result = requests.post("http://Foobar-django-emailnotifier-srv:4004/api/v1/emails", json={
            "recipients": recipients,
            "message": message,
            "subject": subject
        })
        print(result.status_code)
        print(result.text)
    except Exception as e:
        print(e)


def send_login_token(user):
    code = generate_user_sms_token(user)
    if user.phone_number:
        send_sms(phone_number=user.phone_number,
                 message=TOKEN_MESSAGE.format(code))
    if user.email:
        send_email(recipients=user.email,
                   message=EMAIL_TOKEN_MESSAGE.format(user.first_name, code),
                   subject=EMAIL_TOKEN_SUBJECT)


def generate_user_sms_token(user):
    """
    Generates sms login codes.
    :param user: user for whom the code will be generated
    :return: code - used to login
    """
    return VerificationLoginToken.objects.create(user=user).code


def activate_user_after_verifying_phone_number(user):
    if not user.is_active:
        user.is_active = True
        user.save()
        send_sms(user.phone_number, WELCOME_MESSAGE.format(user.first_name))
        send_email(user.email, EMAIL_WELCOME_MESSAGE.format(user.first_name), EMAIL_WELCOME_SUBJECT)


def get_user_by_user_field(user_field):
    users = User.objects.filter(phone_number=user_field)
    return users.first() if users.count() == 1 else User.objects.filter(email=user_field).first()


def initialize_login_token_generation(user_field, password):
    user = get_user_by_user_field(user_field)
    if not user.check_password(password):
        raise PermissionDenied(INVALID_CREDENTIALS)
    send_login_token(user)


def initialize_login_token_without_password_generation(user_field):
    send_login_token(get_user_by_user_field(user_field))


def delete_old_user_login_codes(user):
    VerificationLoginToken.objects.filter(user=user).delete()
