from rest_framework import viewsets
from library.api import serializers
from library import models

class BooksViewset(viewsets.ModelViewSet):
    serializer_class = serializers.BooksSerializer
    queryset = models.Books.objects.all()