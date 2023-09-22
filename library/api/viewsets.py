from rest_framework import viewsets
from library.api import serializers
from library import models

class BooksViewset(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return models.Book.objects.filter(category_id=category_id)
        else:
            return models.Book.objects.all()

