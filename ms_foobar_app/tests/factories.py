import factory
from datetime import timezone, timedelta
from factory import LazyFunction, LazyAttribute, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory
from random import randint, uniform

from ms_foobar_app.models import User

faker = Factory.create()

class UploadedFileFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    created_at = LazyAttribute(lambda o: faker.date_time(tzinfo = timezone(timedelta(0))).isoformat())
    file_type = fuzzy.FuzzyChoice(UploadedFile.FILE_TYPE_CHOICES,getter=lambda c: c[0])
    valid = LazyFunction(faker.boolean)
    user_id = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    verification_fields = LazyAttribute(lambda o: faker.text(max_nb_chars=255))



