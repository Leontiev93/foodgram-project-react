from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.v1.validators import (
    validate_username,
    validate_username_not_me
)
from tags.models import Tags
from recipes.models import Ingredient, IngredientsToRecipes, Favorited, Recipes
from users.models import User, Follow


class TagsSerializer(serializers.Serializer):
    """Сериализатор для модели Tag."""
    # name = serializers.SlugRelatedField(
    #     many=True,
    #     queryset=Tags.objects.all(),
    #     slug_field='slug'
    # )
    # slug = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug'
    # )
    id = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True, required=False)
    slug = serializers.CharField(allow_blank=True, required=False)
    color = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class SignUpSerializer(serializers.Serializer):
    """Сериализатор получения кода подтверждения."""
    username = serializers.CharField(
        validators=(validate_username,
                    validate_username_not_me,
                    UnicodeUsernameValidator(),
                    )
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role')

    def validate(self, data):
        username_exists = User.objects.filter(
            username=data['username']
        ).exists()
        email_exists = User.objects.filter(
            email=data['email']
        ).exists()
        if username_exists and not email_exists:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже есть'
            )
        if email_exists and not username_exists:
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже есть'
            )
        return data


class CreateTokenSerializer(serializers.Serializer):
    """Сериализатор создания JWT-токена для пользователей."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role')
