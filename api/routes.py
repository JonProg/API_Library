from api.viewsets import BooksViewset
from django.urls import path

urlpatterns = [
    path('book/', BooksViewset.as_view(), name="book")
]