from django.utils.deprecation import MiddlewareMixin

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verifica se há um token JWT armazenado em um cookie
        token = request.COOKIES.get('access')
        refresh = request.COOKIES.get('refresh') #adicionar logica para pegar o refresh caso não tenha o acess token
        if token:
            # Adiciona o token ao cabeçalho Authorization
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
