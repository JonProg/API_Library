from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

class JWTUserMatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_auth = JWTAuthentication()

        try:
            # Verifique o token JWT na solicitação
            user, token = jwt_auth.authenticate(request)
            if user is not None:
                # Verifique se o token corresponde ao usuário logado
                if token['user_id'] != str(user.id):
                    raise AuthenticationFailed('Token inválido para o usuário logado.')
        except AuthenticationFailed:
            return Response('Token inválido.', status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response