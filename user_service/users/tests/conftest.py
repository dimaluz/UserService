import os

import pytest
from faker import Faker

from .factories import AccountOwnerFactory, AccountUserFactory, AdminFactory, StaffFactory


if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    raise RuntimeError("DJANGO_SETTINGS_MODULE is not set")


@pytest.fixture
def admin(db):
    return AdminFactory()


@pytest.fixture
def staff(db):
    return StaffFactory()


@pytest.fixture
def account_owner(db):
    return AccountOwnerFactory()


@pytest.fixture
def account_user(db):
    return AccountUserFactory()


@pytest.fixture(scope="session", autouse=True)
def clear_faker_unique():
    """Clean the cache of Faker unique values after tests execution"""
    yield
    fake = Faker()
    fake.unique.clear()
