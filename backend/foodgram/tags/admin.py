from django.contrib import admin

from .models import Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('color',)
    list_editable = ('color',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}
