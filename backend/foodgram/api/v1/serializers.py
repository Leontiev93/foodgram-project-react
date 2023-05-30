import base64

from imaplib import _Authenticator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.files.base import ContentFile

from api.v1.validators import (
    validate_username,
    validate_username_not_me,
    validate_email_password,
    validateEmail

)
from tags.models import Tags
from recipes.models import Ingredient, IngredientsToRecipes, Favorited, Recipes, ShoppingCart
from users.models import User, Follow


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagsSerializer(serializers.Serializer):
    """Сериализатор для модели Tag."""
    id = serializers.IntegerField()
    # name = serializers.SlugRelatedField(required=True, )
    name = serializers.CharField(allow_blank=True, required=False)
    color = serializers.CharField(allow_blank=True, required=False)
    slug = serializers.CharField()

    class Meta:
        model = Tags
        fields = "__all__"


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

    # id = serializers.PrimaryKeyRelatedField(
    #     queryset=Ingredient.objects.all(),
    #     source='id'
    # )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.SerializerMethodField()

    class Meta:
        model = IngredientsToRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, ingredients, *args, **kwargs):
#        print(self.context.get("request").amount)
        print(self.context.get("request"))
        print(self)
        print(111111111111)
        print(ingredients)
        print(ingredients.id)
        print(args)
        print(kwargs)
        amount1 = IngredientsToRecipes.objects.select_related('ingredient', 'recipes',).filter(
            ingredient=ingredients.id
        )
        for i in amount1:
            print('цикл')
            print(i.amount)
            print(IngredientsToRecipes.objects.filter(
            ingredient=ingredients))
        print(amount1)
        return True


class RecipesListSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(
        read_only=True,
        many=True
    )
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientsToRecipesSerializer(
        many=True,
#        source='amount'
    )
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, recipes, *args, **kwargs):
        user = self.context.get("request").user
        if Favorited.objects.filter(
             user=user.id, recipes=recipes.id
             ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipes, *args, **kwargs):
        user = self.context.get("request").user
        if ShoppingCart.objects.filter(
             user=user.id, recipes=recipes.id
             ).exists():
            return True
        return False


class RecipesSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all()
    )
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    class Meta:
        model = Recipes
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    @staticmethod
    def save_ingredients(recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient.get('amount')
            ingredients_list.append(
                IngredientsToRecipes(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=current_amount
                )
            )
        IngredientsToRecipes.objects.bulk_create(ingredients_list)

    def validate(self, data):
        cooking_time = data.get('cooking_time')
        if cooking_time <= 0:
            raise serializers.ValidationError(
                {
                    'Ошибка': 'Время не может быть меньше минуты'
                }
            )
        ingredients_list = []
        print(1111111)
        print(data)
        ingredients_amount = data.get('ingredients_amount')
        for ingredient in ingredients_amount:
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    {
                        'Ошибка': 'Количество не может быть меньше 1'
                    }
                )
            ingredients_list.append(ingredient['ingredient']['id'])
        if len(ingredients_list) > len(set(ingredients_list)):
            raise serializers.ValidationError(
                {
                    'Ошибка': 'Ингридиент должен быть уникальный'
                }
            )
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data, author=author)
        recipe.tags.add(*tags)
        self.save_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        ingredients = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        instance.ingredients.clear()
        recipe = instance
        self.save_ingredients(recipe, ingredients)
        instance.save()
        return instance




# class IngredientsToRecipesSerializer(serializers.ModelSerializer):
#     recipes = RecipesSerializer()

#     class Meta:
#         model = IngredientsToRecipes
#         fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
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
