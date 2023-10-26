from rest_framework import viewsets
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework import status
from library import models

class IsOwnerOrReadOnly(BasePermission):

  def has_object_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True

    return request.user.is_staff

class BooksViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return models.Book.objects.all()
        

    def list(self, request):
        queryset = self.get_queryset()

        publishing_company = request.query_params.get('company')
        category_id = request.query_params.get('category')
        author = request.query_params.get('author')
        title = request.query_params.get('title')
        
        if category_id:
            if not category_id.isdecimal():
                return Response({
                        "message": f"No books found for category ID: {category_id}"  
                    }, status=status.HTTP_404_NOT_FOUND)
            queryset = queryset.filter(category__id=category_id)

        elif author:
            queryset = queryset.filter(author__icontains=author)

        elif title:
            queryset = queryset.filter(title__icontains=title)

        elif publishing_company:
            queryset = queryset.filter(publishing_company__icontains=publishing_company)
        
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    
    

    



