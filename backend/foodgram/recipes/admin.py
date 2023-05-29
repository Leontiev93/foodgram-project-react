from django.contrib import admin

from .models import Recipes, IngredientsToRecipes, Ingredient, Favorited, ShoppingCart


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    fields = [
        'tags',
        'name',
        'cooking_time',
        'author',
#       'ingredients'
    ]
    list_display = (
        'pk',
        '_tags',
        '_ingredients',
        'name',
        'cooking_time',
        # 'favorited'
    )
    search_fields = ('name',)
    list_filter = ('author',)
    list_editable = ('cooking_time', )
    empty_value_display = '-пусто-'

    def _tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    def _ingredients(self, obj):
        return ', '.join([ingredient.name for ingredient in obj.ingredients.all()])

    # def favorited(self, obj):
    #     x = obj.favorited.all()
    #     print)
    #     print('aaaaaaaa')
    #     return ', '.join([favorited.user for favorited in obj.favorited.all()])



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
    list_editable = ('ingredient', 'amount')
    empty_value_display = '-пусто-'


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
        'is_favorited',
    )
    search_fields = (
        'pk',
        'user',
        'recipes',
        'is_favorited',
    )
    list_filter = (
        'user',
        'recipes',
        'is_favorited',
    )
    list_editable = ('is_favorited',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipes',
        'is_in_shopping_cart',
    )
    search_fields = (
        'pk',
        'user',
        'recipes',
        'is_in_shopping_cart',
    )
    list_filter = (
        'user',
        'recipes',
        'is_in_shopping_cart',
    )
    list_editable = ('is_in_shopping_cart',)
    empty_value_display = '-пусто-'
