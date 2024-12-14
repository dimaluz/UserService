from django.contrib import admin

from .models import AccountOwner, AccountUser, Admin, BaseUser, Staff


# @admin.register(BaseUser)
# class BaseUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'role')
#     search_fields = ('email', 'first_name', 'last_name')
#     list_filter = ('date_joined', 'role')
#     readonly_fields = ('date_joined',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "date_joined", "role")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("date_joined", "role")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "date_joined", "role")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("date_joined", "role")


@admin.register(AccountOwner)
class AccountOwnerAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "date_joined", "role")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("date_joined", "role")


@admin.register(AccountUser)
class AccountUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "date_joined", "role")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("date_joined", "role")
