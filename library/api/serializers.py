from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from library import models

class IsOwnerOrReadOnly(BasePermission):

  def has_object_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True

    return request.user.is_staff

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
        extra_kwargs = {
        'permissions': [IsAuthenticated, IsOwnerOrReadOnly]
    }
