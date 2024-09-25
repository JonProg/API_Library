def set_jwt_cookie(response, token, refresh_token):
    """Define cookies for JWT tokens."""
    access_expiration = timezone.now() + timedelta(minutes=25) 
    refresh_expiration = timezone.now() + timedelta(days=7)

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
        books_borrowed = models.Book.objects.filter(borrowed = request.user)

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

    def patch(self,request):
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