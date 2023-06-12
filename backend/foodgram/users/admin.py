from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        '_following'
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    empty_value_display = '-пусто-'
    exclude = (
        'date_joined',
        'last_login',
        'password'
    )

    def _following(self, obj):
        return ', '.join(
            [following.username for following in obj.following.all()])


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = (
        'user',
    )
    empty_value_display = '-пусто-'
