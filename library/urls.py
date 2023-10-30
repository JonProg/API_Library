from django.urls import path
from rest_framework import routers
from django.urls import include
from library.api import viewsets


route = routers.DefaultRouter()
route.register(r'api/books',viewsets.BooksViewset, basename='Books')

urlpatterns = [
    #Book
    path('', include(route.urls)),
    path('api/book/borrowed/<id:book_id>', viewsets.BorrowedBook.as_view(), name='book-borrowed'),
    path('api/book/refund/<id:book_id>', viewsets.ReturnBook.as_view(), name='book-return'),

    #User
    path('api/user/register/', viewsets.UserRegisterView.as_view(), name='user-registration'),
    path('api/user/login/', viewsets.UserLoginView.as_view(), name='user-login'),
    path('api/user/books/', viewsets.UserBooksView.as_view(), name='user-books'),
]