from . import *

class BooksViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        return models.Book.objects.all()
    
    def get_permissions(self):
        if self.action != 'list': 
            return[IsAdminUser()]
        return [IsAuthenticated()]
          
    def list(self, request):
        queryset = self.get_queryset()

        category_id = request.query_params.get('category')
        author = request.query_params.get('author')
        title = request.query_params.get('title')
        
        if category_id:
            if not category_id.isdecimal():
                return Response({
                        "message": f"No books found for category ID: {category_id}"  
                    }, status=status.HTTP_404_NOT_FOUND)
            queryset = queryset.filter(category__id=category_id)

        if author:
            queryset = queryset.filter(author__icontains=author)

        if title:
            queryset = queryset.filter(title__icontains=title)
        
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

class BorrowedBook(APIView):
    permission_classes = [IsAuthenticated,]

    def patch(self, request, book_id):
        try:
            book = models.Book.objects.get(id = book_id)
        except models.Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.returned_book:
            return Response({"message": "Book is already on loan"}, status=status.HTTP_400_BAD_REQUEST)

        book.returned_book = False
        book.borrowed = request.user
        book.save()

        return Response({"message": "Successfully borrowed book"}, status=status.HTTP_200_OK)


class ReturnBook(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, book_id):
        try:
            book = models.Book.objects.get(borrowed = request.user, id = book_id)
        except models.Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if not book.returned_book:
            return Response({"message": "The book is on loan"}, status=status.HTTP_400_BAD_REQUEST)

        book.returned_book = True
        book.borrowed = None
        book.save()

        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)