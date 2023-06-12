import django_filters
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from recipes.models import Recipes, ShoppingCart, Favorited
from tags.models import Tags

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    author = django_filters.CharFilter(field_name='author')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all())

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, value):
        temp_queryset = Favorited.objects.filter(
            user=self.request.user).values('recipes_id')
        if value and self.request.user.is_authenticated:
            return queryset.filter(id__in=temp_queryset)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        temp_queryset = ShoppingCart.objects.filter(
            user=self.request.user).values('recipes_id')
        if value and self.request.user.is_authenticated:
            return queryset.filter(id__in=temp_queryset)
        return queryset
