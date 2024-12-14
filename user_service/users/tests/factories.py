import secrets
import string

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker
from users.models import AccountOwner, AccountUser, Admin, BaseClient, BaseUser, Staff


fake = Faker()


# ========= Users Factory ==========
class BaseUserFactory(DjangoModelFactory):

    class Meta:
        model = BaseUser
        skip_postgeneration_save = True

    @staticmethod
    def generate_password(length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(alphabet) for _ in range(length))

    email = factory.LazyAttribute(lambda _: fake.unique.email()[:255])
    password = factory.PostGenerationMethodCall("set_password", factory.LazyFunction(generate_password))
    first_name = factory.LazyAttribute(lambda _: fake.unique.first_name()[:30])
    last_name = factory.LazyAttribute(lambda _: fake.unique.last_name()[:30])
    date_joined = factory.LazyFunction(timezone.now)


class AdminFactory(BaseUserFactory):

    class Meta:
        model = Admin
        # skip_postgeneration_save = True

    role = BaseUser.Role.ADMIN


class StaffFactory(BaseUserFactory):

    class Meta:
        model = Staff
        # skip_postgeneration_save = True

    role = BaseUser.Role.STAFF


# ========= Clients Factory ==========
class BaseClientFactory(DjangoModelFactory):

    class Meta:
        model = BaseClient
        skip_postgeneration_save = True

    first_name = factory.LazyAttribute(lambda _: fake.unique.first_name()[:30])
    last_name = factory.LazyAttribute(lambda _: fake.unique.last_name()[:30])
    email = factory.LazyAttribute(lambda _: fake.unique.email()[:255])
    phone_number = factory.LazyAttribute(lambda _: fake.unique.msisdn()[:15])
    company_name = factory.LazyAttribute(lambda _: fake.unique.company()[:100])
    country = factory.LazyAttribute(lambda _: fake.unique.country()[:50])
    city = factory.LazyAttribute(lambda _: fake.unique.city()[:50])
    domain = factory.LazyAttribute(lambda _: fake.unique.domain_name()[:100])


class AccountOwnerFactory(BaseClientFactory):

    class Meta:
        model = AccountOwner
        # skip_postgeneration_save = True

    role = BaseClient.Role.ACCOUNT_OWNER


class AccountUserFactory(BaseClientFactory):

    class Meta:
        model = AccountUser
        # skip_postgeneration_save = True

    role = BaseClient.Role.ACCOUNT_USER
