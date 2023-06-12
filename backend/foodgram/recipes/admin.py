from django.contrib import admin

from .models import (
    Recipes,
    IngredientsToRecipes,
    Ingredient,
    Favorited,
    ShoppingCart
)


class IngredientsToRecipesInline(admin.TabularInline):
    model = IngredientsToRecipes


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    fields = [
        'tags',
        'name',
        'cooking_time',
        'author',
        'image',
        'text',
    ]
    inlines = [
        IngredientsToRecipesInline,
    ]
    list_display = (
        'pk',
        '_tags',
        '_ingredients',
        'name',
        'cooking_time',
    )
    search_fields = ('name',)
    list_filter = ('author',)
    list_editable = ('cooking_time', )
    empty_value_display = '-пусто-'

    def _tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    def _ingredients(self, obj):
        return ', \n'.join(
            [f'({ingredient.ingredient}, {ingredient.amount}\n)'
               for ingredient in obj.ingredients.all()])


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
        'measurement_unit',
    )
    list_editable = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Favorited)
class FavoritedAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipes',
    )
    search_fields = (
        'pk',
        'user',
        'recipes',
    )
    list_filter = (
        'user',
        'recipes',
    )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipes',
    )
    search_fields = (
        'pk',
        'user',
        'recipes',
    )
    list_filter = (
        'user',
        'recipes',
    )
    empty_value_display = '-пусто-'
