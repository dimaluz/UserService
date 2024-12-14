import pytest
from users.models import AccountOwner, AccountUser, BaseClient


@pytest.mark.django_db
class TestAccountRelatedInstanceSignal:

    def test_account_owner_created(self):
        """
        Check, that the BaseClient obj with the role = ACCOUNT_OWNER cteates AccountOwner.
        """
        base_client = BaseClient.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            phone_number="1234567890",
            company_name="Example Corp",
            country="Wonderland",
            city="Magic City",
            domain="example.com",
            role=BaseClient.Role.ACCOUNT_OWNER,
            password="12345",
        )

        # Check, if AccountOwner was created
        account_owner = AccountOwner.objects.filter(id=base_client.id).first()
        assert account_owner is not None
        assert account_owner.first_name == "Alice"
        assert account_owner.role == BaseClient.Role.ACCOUNT_OWNER

    def test_account_user_created(self):
        """
        Check, that the BaseClient obj with the role = ACCOUNT_USER cteates AccountUser.
        """
        base_client = BaseClient.objects.create(
            first_name="Bob",
            last_name="Johnson",
            email="bob.johnson@example.com",
            phone_number="9876543210",
            company_name="Example Inc",
            country="Wonderland",
            city="Dream City",
            domain="example.org",
            role=BaseClient.Role.ACCOUNT_USER,
            password="123492",
        )

        # Check, if AccountUser was created
        account_user = AccountUser.objects.filter(id=base_client.id).first()
        assert account_user is not None
        assert account_user.email == "bob.johnson@example.com"

    def test_signal_not_triggered_for_existing_instance(self):
        """
        Checks that the signal does not create duplicate objects if BaseClient already exists.
        """
        base_client = BaseClient.objects.create(
            first_name="Charlie",
            last_name="Brown",
            email="charlie.brown@example.com",
            phone_number="1122334455",
            company_name="Test Corp",
            country="Wonderland",
            city="Happy City",
            domain="example.net",
            role=BaseClient.Role.ACCOUNT_OWNER,
        )

        # Make sure, that AccountOwner was created
        AccountOwner.objects.get(id=base_client.id)

        # Updating of the existed BaseClient object
        base_client.first_name = "Charles"
        base_client.save()

        # Check that resaving does not create a new AccountOwner object
        account_owners_count = AccountOwner.objects.filter(id=base_client.id).count()
        assert account_owners_count == 1
