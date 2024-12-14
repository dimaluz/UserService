import secrets
import string

import pytest
from django.db.utils import IntegrityError
from users.models import AccountOwner, AccountUser, Admin, BaseClient, BaseUser, Staff


@pytest.mark.django_db
class TestAdminModel:

    @staticmethod
    def generate_password(length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def test_admin_creation(self, admin):
        """Check if Admin is created successfully"""
        assert admin.role == BaseUser.Role.ADMIN
        assert Admin.objects.filter(id=admin.id).exists()

    def test_admin_unique_email(self, admin):
        """Check if email is unique for Admin"""
        with pytest.raises(IntegrityError):
            Admin.objects.create(
                first_name="John",
                last_name="Doe",
                email=admin.email,
                role=BaseUser.Role.ADMIN,
            )

    def test_admin_default_role(self):
        """Check if role is set by default as ADMIN"""
        password = self.generate_password()
        admin = Admin.objects.create_admin(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            password=password,
        )
        assert admin.role == BaseUser.Role.ADMIN

    def test_admin_full_name(self, admin):
        """Test for getting a full name"""
        full_name = f"{admin.first_name} {admin.last_name}"
        assert admin.get_full_name() == full_name

    def test_admin_str_method(self, admin):
        """Check __str__ method"""
        assert str(admin) == admin.email

    def test_admin_update_details(self, admin):
        """Check if update is working correctly for Admin"""
        admin.first_name = "UpdatedName"
        admin.save()
        updated_admin = Admin.objects.get(id=admin.id)
        assert updated_admin.first_name == "UpdatedName"


@pytest.mark.django_db
class TestStaffModel:

    @staticmethod
    def generate_password(length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def test_staff_creation(self, staff):
        """Check if Staff is created successfully"""
        assert staff.role == BaseUser.Role.STAFF
        assert Staff.objects.filter(id=staff.id).exists()

    def test_staff_unique_email(self, staff):
        """Check if email is unique for Staff"""
        with pytest.raises(IntegrityError):
            Staff.objects.create(
                first_name="John",
                last_name="Doe",
                email=staff.email,
                role=BaseUser.Role.STAFF,
            )

    def test_staff_default_role(self):
        """Check if role is set by default as STAFF"""
        password = self.generate_password()
        staff = Staff.objects.create_staff(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            password=password,
        )
        assert staff.role == BaseUser.Role.STAFF

    def test_staff_full_name(self, staff):
        """Test for getting a full name"""
        full_name = f"{staff.first_name} {staff.last_name}"
        assert staff.get_full_name() == full_name

    def test_staff_str_method(self, staff):
        """Check __str__ method"""
        assert str(staff) == staff.email

    def test_staff_update_details(self, staff):
        """Check if update is working correctly for Staff"""
        staff.first_name = "UpdatedName"
        staff.save()
        updated_staff = Staff.objects.get(id=staff.id)
        assert updated_staff.first_name == "UpdatedName"


@pytest.mark.django_db
class TestAccountOwnerModel:

    @staticmethod
    def generate_password(length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def test_account_owner_creation(self, account_owner):
        """Check if AccountOwner is created successfully"""
        assert account_owner.role == BaseClient.Role.ACCOUNT_OWNER
        assert AccountOwner.objects.filter(id=account_owner.id).exists()

    def test_account_owner_unique_email(self, account_owner):
        """Check if email is unique for AccountOwner"""
        with pytest.raises(IntegrityError):
            AccountOwner.objects.create(
                first_name="John",
                last_name="Doe",
                email=account_owner.email,
                phone_number="1234567890",
                company_name="Test Company",
                country="Testland",
                city="Testville",
                domain="test.com",
                role=BaseClient.Role.ACCOUNT_OWNER,
            )

    def test_account_owner_default_role(self):
        """Check if role is set by default as ACCOUNT_OWNER"""
        password = self.generate_password()
        account_owner = AccountOwner.objects.create_account_owner(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            phone_number="9876543210",
            company_name="Example Corp",
            country="Wonderland",
            city="Magic City",
            domain="example.com",
            password=password,
        )
        assert account_owner.role == BaseClient.Role.ACCOUNT_OWNER

    def test_account_owner_invalid_phone_number(self):
        """Check if invalid phone number raises an error"""
        password = self.generate_password()
        with pytest.raises(ValueError):
            AccountOwner.objects.create_account_owner(
                first_name="Invalid",
                last_name="Phone",
                email="invalid.phone@example.com",
                phone_number="InvalidPhone",  # Invalid phone number
                company_name="Invalid Corp",
                country="Nowhere",
                city="NoCity",
                domain="invalid.com",
                password=password,
            )

    def test_account_owner_full_name(self, account_owner):
        """Test for getting a full name"""
        full_name = f"{account_owner.first_name} {account_owner.last_name}"
        assert account_owner.get_full_name() == full_name

    def test_account_owner_str_method(self, account_owner):
        """Check __str__ method"""
        assert str(account_owner) == account_owner.email

    def test_account_owner_update_details(self, account_owner):
        """Check if update is working correctly for AccountOwner"""
        account_owner.first_name = "UpdatedName"
        account_owner.save()
        updated_owner = AccountOwner.objects.get(id=account_owner.id)
        assert updated_owner.first_name == "UpdatedName"


@pytest.mark.django_db
class TestAccountUserModel:

    @staticmethod
    def generate_password(length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def test_account_user_creation(self, account_user):
        """Check if AccountUser is created successfully"""
        assert account_user.role == BaseClient.Role.ACCOUNT_USER
        assert AccountUser.objects.filter(id=account_user.id).exists()

    def test_account_user_unique_email(self, account_user):
        """Check if email is unique for AccountUser"""
        with pytest.raises(IntegrityError):
            AccountUser.objects.create(
                first_name="John",
                last_name="Doe",
                email=account_user.email,
                phone_number="1234567890",
                company_name="Test Company",
                country="Testland",
                city="Testville",
                domain="test.com",
                role=BaseClient.Role.ACCOUNT_USER,
            )

    def test_account_user_default_role(self):
        """Check if role is set by default as ACCOUNT_USER"""
        password = self.generate_password()
        account_user = AccountUser.objects.create_account_user(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            phone_number="9876543210",
            company_name="Example Corp",
            country="Wonderland",
            city="Magic City",
            domain="example.com",
            password=password,
        )
        assert account_user.role == BaseClient.Role.ACCOUNT_USER

    def test_account_user_invalid_phone_number(self):
        """Check if invalid phone number raises an error"""
        password = self.generate_password()
        with pytest.raises(ValueError):
            AccountUser.objects.create_account_user(
                first_name="Invalid",
                last_name="Phone",
                email="invalid.phone@example.com",
                phone_number="InvalidPhone",  # Invalid phone number
                company_name="Invalid Corp",
                country="Nowhere",
                city="NoCity",
                domain="invalid.com",
                password=password,
            )

    def test_account_user_full_name(self, account_user):
        """Test for getting a full name"""
        full_name = f"{account_user.first_name} {account_user.last_name}"
        assert account_user.get_full_name() == full_name

    def test_account_user_str_method(self, account_user):
        """Check __str__ method"""
        assert str(account_user) == account_user.email

    def test_account_user_update_details(self, account_user):
        """Check if update is working correctly for AccountUser"""
        account_user.first_name = "UpdatedName"
        account_user.save()
        updated_user = AccountUser.objects.get(id=account_user.id)
        assert updated_user.first_name == "UpdatedName"
