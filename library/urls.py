from django.urls import path
from rest_framework import routers
from django.urls import include
from library.api.views import book_viewset, user_viewset


route = routers.DefaultRouter()
route.register(r'api/books',book_viewset.BooksViewset, basename='Books')

urlpatterns = [
    #Book
    path('', include(route.urls)),
    path('api/books/borrowed/<int:book_id>/', book_viewset.BorrowedBook.as_view()),
    path('api/books/refund/<int:book_id>/', book_viewset.ReturnBook.as_view()),

    #User
    path('api/user/', user_viewset.UserView.as_view(), name='user'),
    path('api/user/register/', user_viewset.UserRegisterView.as_view(), name='user-registration'),
    path('api/user/login/', user_viewset.UserLoginView.as_view(), name='user-login'), #só pode ver o usuario atual,deletar,atualizar
]