from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from library.api import serializers
from library import models

class BooksViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.BookSerializer
    
    def get_queryset(self):
        queryset = models.Book.objects.all()

        publishing_company = self.request.query_params.get('company')
        category = self.request.query_params.get('category')
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')

        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset

