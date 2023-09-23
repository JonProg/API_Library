from rest_framework import viewsets
from library.api import serializers
from library import models

class BooksViewset(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    
    def get_queryset(self):
        category_slug = self.request.query_params.get('category')
        if category_slug:
            return models.Book.objects.filter(category_slug=category_slug)
        else:
            return models.Book.objects.all()

