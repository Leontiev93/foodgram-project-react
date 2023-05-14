from django.contrib import admin

from .models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'role'
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = ('role',)
    empty_value_display = '-пусто-'
    exclude = (
        'date_joined',
        'last_login',
    )
