from imaplib import _Authenticator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.db.models import Exists
from django.db.models import OuterRef

from api.v1.validators import (
    validate_username,
    validate_username_not_me,
    validate_email_password,
    validateEmail

)
from tags.models import Tags
from recipes.models import Ingredient, IngredientsToRecipes, Favorited, Recipes
from users.models import User, Follow


class TagsSerializer(serializers.Serializer):
    """Сериализатор для модели Tag."""
    id = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True, required=False)
    color = serializers.CharField(allow_blank=True, required=False)
    slug = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Tags
        fields = ('id', 'name', 'slug', 'color')


class CreateTokenSerializer(serializers.Serializer):
    """Сериализатор создания токена для пользователей."""
    email = serializers.EmailField(max_length=150)
    user = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели User."""
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
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'password')

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
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, following, *args, **kwargs):
        try:
            user = self.context.get("request").user
            if Follow.objects.filter(user=user, author=following):
                return True
            return False
        except:
            return False


class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password)')


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            if validateEmail(email):
                user_request = get_object_or_404(
                    User,
                    email=email,
                )
                email = user_request.username

            user = authenticate(username=email, password=password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationError(msg)
        else:
            msg = 'Must include "email or username" and "password"'
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientsToRecipesSerializer(serializers.ModelSerializer):
    recipes = IngredientSerializer()

    class Meta:
        model = IngredientsToRecipes
        fields = "__all__"


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#    author = UserSerializer(read_only=True, )
#    ingredients = serializers.StringRelatedField(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, required=False)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = "__all__"

    def get_is_favorited(self, recipes, *args, **kwargs):
        print(self.context.get("request").query_params)
#        print(self.request)
        user = self.context.get("request").user
        if Favorited.objects.filter(user=user.id, recipes=recipes.id).exists():
            return True
        return False


class FollowSerializer(serializers.ModelSerializer):
    # user = SlugRelatedField(
    #     slug_field='username',
    #     read_only=True,
    #     default=serializers.CurrentUserDefault()
    # )
    # author = SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all()
    # )
    author = UserSerializer()

    class Meta:
#        fields = '__all__'
#        fields = ['recipes',]
        model = Follow
        read_only_fields = ('user',)
        exclude = ['id', "created", 'user']

    def validate(self, data):
        user = self.context.get("request").user
        following = data.get("following")
        if Follow.objects.filter(user=user, following=following):
            raise serializers.ValidationError(
                f'Вы уже подписаны на автора {following}!'
            )
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписыватся на самого себя!"
            )
        return data
