from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from library import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            RegexValidator(
                regex=r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$',
                message="Enter a valid email"
            )
        ]
    )


    username = serializers.CharField(
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="The username can only contain letters, numbers and @/./+/-/_."  
            )
        ]
    )

    password = serializers.CharField(
        validators=[MinLengthValidator(7)],
        write_only=True
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def validate(self, attrs):
        # Validar se o email ou username já estão em uso
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "E-mail already registered"}
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "Username already registered"}  
            )

        return attrs

class PutSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            RegexValidator(
                regex=r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$',
                message="Enter a valid email"
            )
        ]
    )


    username = serializers.CharField(
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="The username can only contain letters, numbers and @/./+/-/_."  
            )
        ]
    )

    def validate(self, attrs):
        # Validar se o email ou username já estão em uso
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "E-mail already registered"}
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "Username already registered"}  
            )

        return attrs
    
