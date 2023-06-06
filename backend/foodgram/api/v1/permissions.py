from rest_framework import permissions


# Для регистрации
class CreateNewUser(permissions.BasePermission):
    """Разрешение на создание записи администратора или суперпользователя."""

    def has_permission(self, request, view):
        return ((request.method == "POST" and request.user.is_anonymous)
                or request.user.is_authenticated)


# Для моделей Recipes
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
