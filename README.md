<p align="center">
    <img src="https://i.postimg.cc/3NQ4jQST/api-3d.png" align="center" width=170px ></img>
</p>    

<h2 align="center">API Biblioteca | DRF</h2>

<div align="center">

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)
![Insomnia](https://img.shields.io/badge/Insomnia-black?style=for-the-badge&logo=insomnia&logoColor=5849BE)

</div>

[![apiy.gif](https://i.postimg.cc/0QF6K4j1/apiy.gif)](https://postimg.cc/Vr9s3DXK)

## Runing project using docker:
Modifique o .env antes de rodar a API os dados estaram no docker-compose.yml

~~~~bash
git clone git@github.com:JonProg/API_Library.git
cd API_Library
docker compose up -d --build
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
~~~~

~~~~python
#A api será executada na porta 8000 -> http://127.0.0.1:8000
~~~~


## Endpoints
#### Books Routes
- `GET /api/books/`: Lista todos os livros com opções de filtro por category, author e title. <br><br>

- `POST /api/books/`: Cria um novo livro (administradores).<br><br>

- `PUT /api/books/<id>/`: Atualiza um livro existente (administradores).<br><br>

- `DELETE /api/books/<id>/`: Remove um livro existente (administradores).<br><br>

- `PATCH /api/books/borrowed/<book_id>/`: Permite que um usuário faça o empréstimo de um livro.<br><br>

- `PATCH /api/books/refund/<book_id>/`: Permite que um usuário devolva um livro.

___

#### User Routes
- `GET /api/user/`: Retorna os dados do usuário logado, incluindo livros emprestados.<br><br>
- `PATCH /api/user/`: Atualiza informações do usuário logado (nome de usuário, e-mail).
- `DELETE /api/user/`: Deleta a conta do usuário logado.
- `POST /api/user/register/`: Registra um novo usuário.
- `POST /api/user/login/`: Realiza login com username e password e retorna tokens JWT nos cookies.

___

### JWT configuration through cookies

~~~~python
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
~~~~





