# Generated by Django 4.2.15 on 2024-12-14 10:53

import uuid

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseClient",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("first_name", models.CharField(blank=True, max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(max_length=15, unique=True, verbose_name="Phone Number")),
                ("company_name", models.CharField(max_length=255, verbose_name="Company Name")),
                ("country", models.CharField(max_length=100, verbose_name="Country")),
                ("city", models.CharField(max_length=100, verbose_name="City")),
                ("domain", models.CharField(max_length=255, unique=True, verbose_name="Domain")),
                ("account_id", models.UUIDField(blank=True, verbose_name="Account ID")),
                ("subaccount_id", models.UUIDField(blank=True, verbose_name="Subaccount ID")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "role",
                    models.CharField(
                        choices=[("AccountOwner", "Account Owner"), ("AccountUser", "Account User")],
                        default="AccountUser",
                        max_length=20,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to.",
                        related_name="baseclient_groups",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="baseclient_permissions",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BaseUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("first_name", models.CharField(blank=True, max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "role",
                    models.CharField(choices=[("Admin", "Admin"), ("Staff", "Staff")], default="Staff", max_length=20),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to.",
                        related_name="baseuser_groups",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="baseuser_permissions",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AccountOwner",
            fields=[],
            options={
                "verbose_name": "Account Owner",
                "verbose_name_plural": "Account Owners",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.baseclient",),
        ),
        migrations.CreateModel(
            name="AccountUser",
            fields=[],
            options={
                "verbose_name": "Account User",
                "verbose_name_plural": "Account Users",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.baseclient",),
        ),
        migrations.CreateModel(
            name="Admin",
            fields=[],
            options={
                "verbose_name": "Admin",
                "verbose_name_plural": "Admins",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.baseuser",),
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[],
            options={
                "verbose_name": "Staff",
                "verbose_name_plural": "Staff",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.baseuser",),
        ),
    ]