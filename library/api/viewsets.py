from rest_framework import viewsets
from library.api import serializers
from library import models

class BooksViewset(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    
    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return models.Book.objects.filter(category__slug=category)
        else:
            return models.Book.objects.all()

