from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import BookSerializer, UserSerializer, PutSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from library import models
from .docs import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from api.views.book_viewset import BooksViewset, BorrowedBook, ReturnBook
from api.views.user_viewset import UserView, UserRegisterView, UserLoginView