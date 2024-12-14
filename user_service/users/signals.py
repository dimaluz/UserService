import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import AccountOwner, AccountUser, Admin, BaseClient, BaseUser, Staff


logger = logging.getLogger(__name__)


@receiver(post_save, sender=BaseUser)
def create_user_related_instance(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.role == BaseUser.Role.ADMIN:
                Admin.objects.create_admin(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email,
                )
                logger.info(f"Admin created for user {instance.email}")
            elif instance.role == BaseUser.Role.STAFF:
                Staff.objects.create_staff(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email,
                )
                logger.info(f"Staff created for user {instance.email}")
        except Exception as e:
            # Errors logs
            logger.error(f"Error creating related instance for user {instance.email}: {e}")


@receiver(post_save, sender=BaseClient)
def create_account_related_instance(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.role == BaseClient.Role.ACCOUNT_OWNER:
                AccountOwner.objects.create_account_owner(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email,
                    phone_number=instance.phone_number,
                    company_name=instance.company_name,
                    country=instance.country,
                    city=instance.city,
                    domain=instance.domain,
                    role=instance.role,
                    password=instance.password,
                )
                logger.info(f"AccountOwner created for user {instance.email}")
            elif instance.role == BaseClient.Role.ACCOUNT_USER:
                AccountUser.objects.create_account_user(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email,
                    phone_number=instance.phone_number,
                    company_name=instance.company_name,
                    country=instance.country,
                    city=instance.city,
                    domain=instance.domain,
                    role=instance.role,
                    password=instance.password,
                )
                logger.info(f"AccountUser created for user {instance.email}")
        except Exception as e:
            # Errors logs
            logger.error(f"Error creating related instance for user {instance.email}: {e}")
