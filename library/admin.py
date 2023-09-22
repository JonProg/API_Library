from django.contrib import admin
from .models import Category,Tag, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    list_per_page = 10
    ordering = '-id',

admin.site.register(Tag)
admin.site.register(Book)
