from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import BookSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from library import models
from .docs import messages

class GetCurrentUserToken(BasePermission):
    def has_permission(self, request, view):
        try:
            models.Tokens.objects.get(owner=request.user)
            return True
        except:
            return False

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser


class BooksViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated, GetCurrentUserToken,]

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


class UserRegisterView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        }
        ),
        responses= messages.register_user
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

class UserLoginView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses= messages.login_res
    )
    def post(self, request):
        if request.user.is_authenticated: 
            models.Tokens.objects.filter(owner=request.user).delete()
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful.'
            }
            tokens, _ = models.Tokens.objects.get_or_create(owner=user)
            tokens.token = token['access']
            tokens.token_refresh = token['refresh']
            tokens.save()

            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username,password or email.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    permission_classes = [IsAuthenticated,]
    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, 
    description='Token de autenticação (Bearer token)')
    ], responses=messages.user_res)
    def get(self, request):

        data = {
            'username':request.user.username,
            'email':request.user.email
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, 
    description='Token de autenticação (Bearer token)')
    ])
    def put(self,request):
        models.Tokens.objects.filter(owner=request.user).delete()
        user = User.objects.get(pk=request.user.id)
        username = request.data.get('username')
        email = request.data.get('email')

        email_existing = User.objects.get(email=email)

        if email_existing:
            return Response({'error': 'Invalid email.'}, status=status.HTTP_401_UNAUTHORIZED)

        user.username = username
        user.email = email
        user.save()

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, 
    description='Token de autenticação (Bearer token)')
    ])
    def delete(self, request):
        models.Tokens.objects.filter(owner=request.user).delete()
        User.objects.filter(pk=request.user.id).delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        

class BorrowedBook(APIView):
    permission_classes = [IsAuthenticated, GetCurrentUserToken,]

    def get(self, request, book_id):
        try:
            book = models.Book.objects.get(id = book_id)
        except models.Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.lent_book:
            return Response({"message": "Book is already on loan"}, status=status.HTTP_400_BAD_REQUEST)

        book.lent_book = True
        book.borrowed = request.user
        book.save()

        return Response({"message": "Successfully borrowed book"}, status=status.HTTP_200_OK)


class ReturnBook(APIView):
    permission_classes = [IsAuthenticated, GetCurrentUserToken,]

    def get(self, request, book_id):
        try:
            book = models.Book.objects.get(id = book_id)
        except models.Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if not book.lent_book:
            return Response({"message": "Book is not on loan"}, status=status.HTTP_400_BAD_REQUEST)

        book.lent_book = False
        book.borrowed = None
        book.save()

        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)


class UserBooksView(APIView):
    permission_classes = [IsAuthenticated, GetCurrentUserToken,]

    @swagger_auto_schema(
        responses= messages.user_books
    )
    def get(self, request):
        books_borrowed = models.Book.objects.filter(borrowed = request.user, lent_book = True)

        # Serializa os livros emprestados para retornar como resposta
        serializer = BookSerializer(books_borrowed, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)