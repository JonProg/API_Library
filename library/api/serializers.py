from rest_framework import serializers
from library import models

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Books
        fields = '__all__'