from rest_framework import permissions


class CreateNewUser(permissions.BasePermission):
    """Разрешение на создание записи пользователя."""

    def has_permission(self, request, view):
        return ((request.method == "POST" and request.user.is_anonymous)
                or request.user.is_authenticated)


class AdminOrAuthor(permissions.BasePermission):
    """Разрешение для администратора или автора
    иначе чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or obj.author == request.user
                )
