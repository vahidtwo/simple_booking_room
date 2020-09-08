from django.contrib import admin

from accounts.models import User
from core.admin import AbstractBaseAdmin


class UserAdmin(AbstractBaseAdmin):
    search_fields = ('id', 'username', 'phone_number')
    list_filter = ('gender', 'is_staff')


admin.site.register(User, UserAdmin)
