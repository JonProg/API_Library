<p align="center">
    <img src="https://i.postimg.cc/3NQ4jQST/api-3d.png" align="center" width=177px ></img>
</p>    
<br>
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

```bash
$git clone git@github.com:JonProg/API_Library.git

$cd API_Library

$docker compose up -d

$docker compose exec web python manage.py migrate
```
~~~~python
#A api será executada na porta 8000 -> http://127.0.0.1:8000
~~~~

### Route - (api/books/)


| Method | Description
|---|---|
| `GET` - (All Users) | Retorna informações de todos livros adicionados no Postgres e quando a rota é "api/books/{id}" ele retorna o livro com um id específico. |
| `POST` - (OAI) | Usada para adicionar um livro a base de dados.|
| `PUT` - (OAI) | Atualiza uma parte dos dados de um livro.|
| `PATCH` - (OAI) | Atualiza os dados por completo de um livro.|
| `DELETE` - (OAI) | Exclui o livro da base de dados.|

> OAI = Only Admins with ID













