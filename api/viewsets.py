from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.serializers import BookSerializer
from library import models


class BooksViewset(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookSerializer
    
    def get(self):
        queryset = models.Book.objects.all().order_by('-id')

        publishing_company = self.request.query_params.get('company')
        category = self.request.query_params.get('category')
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')
        
        if category:
            queryset = queryset.filter(category__slug=category)

        elif author:
            queryset = queryset.filter(author__icontains=author)

        elif title:
            queryset = queryset.filter(title__icontains=title)

        elif publishing_company:
            queryset = queryset.filter(publishing_company__icontains=publishing_company)
        
        return queryset
    
    def post(self, request):
        # Implemente a lógica para criar um novo registro
        # com base nos dados fornecidos na requisição POST
        # e retorne uma resposta com os dados criados
        return Response('aqui', status=status.HTTP_201_CREATED)

    def get_object(self, id):
        # Implemente a lógica para recuperar um objeto específico
        # com base no parâmetro passado na URL, como ID ou slug
        return None
    
    def get(self, request, *args, **kwargs):
        objeto = self.get_object()
        # Implemente a lógica para recuperar um objeto específico
        # e retorne uma resposta com os dados do objeto encontrado
        return Response('aqui', status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        objeto = self.get_object()
        # Implemente a lógica para atualizar um objeto específico
        # com base nos dados fornecidos na requisição PUT e retorne
        # uma resposta com os dados atualizados
        return Response('aqui', status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        objeto = self.get_object()
        # Implemente a lógica para excluir um objeto específico
        # e retorne uma resposta com o status da operação
        return Response(status=status.HTTP_204_NO_CONTENT)

    



