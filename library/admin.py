from django.contrib import admin
from .models import Category,Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 
    list_display_links = 'name',
    search_fields = 'id', 'name', 
    list_per_page = 10
    ordering = '-id',
 


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'returned_book','borrowed'
    list_editable = 'returned_book',
    list_display_links = 'title',
    search_fields = 'id', 'title', 'id_borrowed',
    list_per_page = 10
    ordering = '-id',