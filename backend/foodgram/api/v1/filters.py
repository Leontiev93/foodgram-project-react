import django_filters
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from recipes.models import Recipes

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(django_filters.FilterSet):

    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(user__favorited=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(user__shoppingcart=self.request.user)
        return queryset
