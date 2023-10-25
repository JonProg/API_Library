from rest_framework import serializers
from django.contrib.auth.models import User
from library import models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
