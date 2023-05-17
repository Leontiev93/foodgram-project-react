from django.contrib import admin

from .models import Recipes, IngredientsToRecipes, Ingredient


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    fields = [
        'tags',
        'is_favorited',
        'is_in_shopping_cart',
        'name',
        'cooking_time',
        'author',
#        'ingredients'
    ]
    list_display = (
        'pk',
        '_tags',
#        '_ingredients',
        'is_favorited',
        'is_in_shopping_cart',
        'name',
        'cooking_time',
    )
    search_fields = ('name',)
    list_filter = ('is_favorited',)
    list_editable = ('is_favorited', 'is_in_shopping_cart')
    empty_value_display = '-пусто-'

    def _tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    def _ingredients(self, obj):
        return '\n'.join([ingredient.name for ingredient in obj.ingredients.all()])



@admin.register(IngredientsToRecipes)
class IngredientsToRecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipes',
        'ingredient',
        'amount',
    )
    search_fields = ('recipes',)
    list_filter = ('recipes',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
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
