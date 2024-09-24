from django.urls import path
from rest_framework import routers
from django.urls import include
from library.api import viewsets


route = routers.DefaultRouter()
route.register(r'api/books',viewsets.BooksViewset, basename='Books')

urlpatterns = [
    #Book
    path('', include(route.urls)),
    path('api/books/borrowed/<int:book_id>/', viewsets.BooksViewset.as_view({'put': 'borrowed'})),
    path('api/books/refund/<int:book_id>/', viewsets.BooksViewset.as_view({'put': 'refund'})),

    #User
    path('api/user/', viewsets.UserView.as_view(), name='user'),
    path('api/user/register/', viewsets.UserRegisterView.as_view(), name='user-registration'),
    path('api/user/login/', viewsets.UserLoginView.as_view(), name='user-login'), #só pode ver o usuario atual,deletar,atualizar
]