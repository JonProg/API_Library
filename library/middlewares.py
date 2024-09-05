from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verifica se há um token JWT armazenado em um cookie
        token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh') #adicionar logica para pegar o refresh caso não tenha o acess token
        if token:
            # Adiciona o token ao cabeçalho Authorization
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        elif refresh_token:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'