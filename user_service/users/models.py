import re
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# ======= User Managers =======
class BaseUserMgr(BaseUserManager):

    def create_user(self, email, password, role="Staff", **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        if role not in BaseUser.Role.values:
            raise ValueError(f"Invalid role: {role}")
        extra_fields.setdefault("is_active", True)
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        if password and password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, role="Admin", **extra_fields)


class AdminMgr(models.Manager):

    def create_admin(self, **kwargs):
        kwargs["role"] = BaseUser.Role.ADMIN
        return self.model.objects.create(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(role=BaseUser.Role.ADMIN)


class StaffMgr(models.Manager):

    def create_staff(self, **kwargs):
        kwargs["role"] = BaseUser.Role.STAFF
        return self.model.objects.create(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(role=BaseUser.Role.STAFF)


# ======= Client Managers =======
class BaseClientMgr(BaseUserManager):

    def create_client(
        self,
        first_name,
        last_name,
        email,
        phone_number,
        company_name,
        country,
        city,
        domain,
        role="AccountUser",
        password=None,
        account_id=None,
        subaccount_id=None,
        is_active=True,
    ):
        if not email:
            raise ValueError("The email field must be set")
        if role not in BaseClient.Role.values:
            raise ValueError(f"Invalid role: {role}")
        email = self.normalize_email(email)
        client = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            country=country,
            city=city,
            domain=domain,
            account_id=account_id,
            subaccount_id=subaccount_id,
            is_active=is_active,
            role=role,
        )
        if password and password is not None:
            client.set_password(password)
        client.save(using=self._db)
        return client


class AccountOwnerMgr(models.Manager):

    def create_account_owner(
        self,
        first_name,
        last_name,
        email,
        phone_number,
        company_name,
        country,
        city,
        domain,
        password=None,
        account_id=None,
        subaccount_id=None,
        is_active=True,
    ):
        if not password:
            raise ValueError("Password must be provided")

        if not phone_number or not re.match(r"^\+?\d{10,15}$", phone_number):
            raise ValueError("Invalid phone number format. Must be 10-15 digits long.")

        role = BaseClient.Role.ACCOUNT_OWNER
        hashed_password = make_password(password)

        account_owner = self.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            country=country,
            city=city,
            domain=domain,
            role=role,
            password=hashed_password,
            account_id=account_id,
            subaccount_id=subaccount_id,
            is_active=is_active,
        )
        return account_owner

    def get_queryset(self):
        return super().get_queryset().filter(role=BaseClient.Role.ACCOUNT_OWNER)


class AccountUserMgr(models.Manager):

    def create_account_user(
        self,
        first_name,
        last_name,
        email,
        phone_number,
        company_name,
        country,
        city,
        domain,
        password=None,
        account_id=None,
        subaccount_id=None,
        is_active=True,
    ):
        if not password:
            raise ValueError("Password must be provided")

        if not phone_number or not re.match(r"^\+?\d{10,15}$", phone_number):
            raise ValueError("Invalid phone number format. Must be 10-15 digits long.")

        role = BaseClient.Role.ACCOUNT_USER
        hashed_password = make_password(password)

        account_user = self.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            country=country,
            city=city,
            domain=domain,
            role=role,
            password=hashed_password,
            account_id=account_id,
            subaccount_id=subaccount_id,
            is_active=is_active,
        )
        return account_user

    def get_queryset(self):
        return super().get_queryset().filter(role=BaseClient.Role.ACCOUNT_USER)


# ======= User Models =======
class BaseUser(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        ADMIN = "Admin", _("Admin")
        STAFF = "Staff", _("Staff")

        @classmethod
        def values(cls):
            return [role.value for role in cls]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=False,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="baseuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="baseuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = BaseUserMgr()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email}"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_staff_user(self):
        return self.role == self.Role.STAFF


class Admin(BaseUser):

    objects = AdminMgr()

    def save(self, *args, **kwargs):
        if not self.role or self.role != self.Role.ADMIN:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Returns the full name of the admin."""
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        proxy = True
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")


class Staff(BaseUser):

    objects = StaffMgr()

    def save(self, *args, **kwargs):
        if not self.role or self.role != self.Role.STAFF:
            self.role = self.Role.STAFF
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Returns the full name of the account user."""
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        proxy = True
        verbose_name = _("Staff")
        verbose_name_plural = _("Staff")


# ========== Client Models ==========
class BaseClient(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        ACCOUNT_OWNER = "AccountOwner", _("Account Owner")
        ACCOUNT_USER = "AccountUser", _("Account User")

    @classmethod
    def values(cls):
        return [role.value for role in cls]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Phone Number"),
    )
    company_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_("Company Name"),
    )
    country = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("Country"),
    )
    city = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("City"),
    )
    domain = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Domain"),
    )
    account_id = models.UUIDField(
        blank=True,
        verbose_name=_("Account ID"),
    )
    subaccount_id = models.UUIDField(
        blank=True,
        verbose_name=_("Subaccount ID"),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
    )
    is_active = models.BooleanField(
        default=False,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ACCOUNT_USER,
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="baseclient_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="baseclient_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = BaseClientMgr()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email}"

    @property
    def is_account_owner(self):
        return self.role == self.Role.ACCOUNT_OWNER

    @property
    def is_account_user(self):
        return self.role == self.Role.ACCOUNT_USER


class AccountOwner(BaseClient):

    objects = AccountOwnerMgr()

    def save(self, *args, **kwargs):
        if not self.role or self.role != self.Role.ACCOUNT_OWNER:
            self.role = self.Role.ACCOUNT_OWNER
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Returns the full name of the account owner."""
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        proxy = True
        verbose_name = _("Account Owner")
        verbose_name_plural = _("Account Owners")


class AccountUser(BaseClient):

    objects = AccountUserMgr()

    def save(self, *args, **kwargs):
        if not self.role or self.role != self.Role.ACCOUNT_USER:
            self.role = self.Role.ACCOUNT_USER
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Returns the full name of the account user."""
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        proxy = True
        verbose_name = _("Account User")
        verbose_name_plural = _("Account Users")
