from rest_framework import viewsets
from rest_framework.decorators import action
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
from library.models import Book
from .docs import messages
from django.conf import settings
from django.utils import timezone
import datetime

def set_jwt_cookie(response, token, refresh_token):
    """Define cookies for JWT tokens."""
    access_expiration = timezone.now() + datetime.timedelta(minutes=25) 
    refresh_expiration = timezone.now() + datetime.timedelta(days=7)

    response.set_cookie(
        key='access',
        value=token,
        expires=access_expiration,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite='Lax'
    )
    response.set_cookie(
        key='refresh',
        value=refresh_token,
        expires=refresh_expiration,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite='Lax'
    )
    return response


class BooksViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action != 'list': 
            return[IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def borrowed(self, request, book_id=None):
        try:
            book = Book.objects.get(id = book_id)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.refund_book:
            return Response({"message": "Book is already on loan"}, status=status.HTTP_400_BAD_REQUEST)

        book.refund_book = True
        book.borrowed = request.user
        book.save()

        return Response({"message": "Successfully borrowed book"}, status=status.HTTP_200_OK)
    
    
    def refund(self, request, book_id=None):
        try:
            book = Book.objects.get(id = book_id)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if not book.refund_book:
            return Response({"message": "Book is not on loan"}, status=status.HTTP_400_BAD_REQUEST)

        book.refund_book = False
        book.borrowed = None
        book.save()

        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)
    
          
    def list(self, request):
        queryset = Book.objects.all()

        publishing_company = request.query_params.get('company')
        category_id = request.query_params.get('category')
        author = request.query_params.get('author')
        title = request.query_params.get('title')
        
        if category_id:
            if not category_id.isdecimal():
                return Response({
                        "message": f"No books found for category ID: {category_id}"  
                    }, status=status.HTTP_404_NOT_FOUND)
            queryset = queryset.filter(category__id=category_id) # or author or || testar

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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Success': 'Success in registering the user'}, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

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
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            refresh = RefreshToken.for_user(user)
            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            response = set_jwt_cookie(response, str(refresh.access_token), str(refresh))
            return response
        else:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, 
    description='Token de autenticação (Bearer token)')
    ], responses=messages.user_res)


    def get(self, request):
        books_borrowed = Book.objects.filter(borrowed = request.user, refund_book = True)

        # Serializa os livros emprestados para retornar como resposta
        serializer = BookSerializer(books_borrowed, many=True)

        data = {
            'username':request.user.username,
            'email':request.user.email,
            'books_borrowed':serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, 
    description='Token de autenticação (Bearer token)')
    ])

    def put(self,request):
        serializer = PutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(pk=request.user.id)
            username = request.data.get('username')
            email = request.data.get('email')
            user.username = username
            user.email = email
            user.save()
            return Response({'Success': 'Success in update the user'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, 
    description='Token de autenticação (Bearer token)')
    ])

    def delete(self, request):
        User.objects.filter(pk=request.user.id).delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        