from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from api.v1.validators import (
    validate_username,
    validate_username_not_me,
    validate_email_password

)
from tags.models import Tags
from recipes.models import Ingredient, IngredientsToRecipes, Favorited, Recipes
from users.models import User, Follow


class TagsSerializer(serializers.Serializer):
    """Сериализатор для модели Tag."""
    id = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True, required=False)
    slug = serializers.CharField(allow_blank=True, required=False)
    color = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class SignUpSerializer(serializers.Serializer):
    """Сериализатор создания учетной зщаписи."""
    username = serializers.CharField(
        validators=(validate_username,
                    validate_username_not_me,
                    UnicodeUsernameValidator(),
                    )
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def validate(self, data):
        print(self)
        print(data)
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
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели User."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserCreateSerializer, self).create(validated_data)

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

class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""
#    following = serializers.StringRelatedField(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, following):
        try:
            user = self.context.get("request").user
            if Follow.objects.filter(user=user, author=following):
                return True
            return False
        except:
            return None