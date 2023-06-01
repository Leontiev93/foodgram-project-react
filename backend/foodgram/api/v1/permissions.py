from rest_framework import permissions


# Для модели User
class AdminOrSuperuserOnly(permissions.BasePermission):
    """Разрешение для администратора или суперпользователя."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


# Для моделей Review, Comment
class AdminModeratorAuthor(permissions.BasePermission):
    """Разрешение для администратора, модератора или автора
    иначе чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
                )


# Для моделей Genre, Categories, Title
class AdminOrReadOnly(permissions.IsAdminUser):
    """Разрешение для админов иначе чтение"""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)
