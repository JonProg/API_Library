from django.contrib import admin
from .models import Category,Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    search_fields = 'id', 'name',
    list_per_page = 10
    ordering = '-id',
 

admin.site.register(Book)
