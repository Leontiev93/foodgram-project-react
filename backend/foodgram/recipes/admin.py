from django.contrib import admin

from .models import Recipes, IngredientsToRecipes


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        # 'tags',
        # 'ingredients',
        'is_favorited',
        'is_in_shopping_cart',
        'name',
        'cooking_time',
        'name',
    )
    search_fields = ('name',)
    list_filter = ('is_favorited',)
    list_editable = ('is_favorited', 'is_in_shopping_cart')
    empty_value_display = '-пусто-'


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
