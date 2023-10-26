from django.urls import path
from library.api.viewsets import UserLoginView, UserRegisterView
from rest_framework import routers
from django.urls import include
from library.api import viewsets


route = routers.DefaultRouter()
route.register(r'books',viewsets.BooksViewset, basename='Books')

urlpatterns = [
    path('', include(route.urls)),

    #User
    path('register/', UserRegisterView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]