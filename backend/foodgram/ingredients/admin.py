from django.contrib import admin

from .models import Ingredient


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
