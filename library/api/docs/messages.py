from drf_yasg import openapi

msg_login = {
	"refresh":openapi.Schema(type=openapi.TYPE_STRING, title="Token Refresh",
    description="Token de atualização para o usuário"),
	"access":openapi.Schema(type=openapi.TYPE_STRING, title="Token Access",
    description="Token de acesso para o usuário"),
	"message":openapi.Schema(type=openapi.TYPE_STRING, title="Login successful",
    description="Mensagem indicando o sucesso do login")
}

msg_userbooks = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
    "id":openapi.Schema(type=openapi.TYPE_INTEGER, title="ID", read_only=True),
    "title":openapi.Schema(type=openapi.TYPE_STRING, title="Title"),
    "author":openapi.Schema(type=openapi.TYPE_STRING, title="Author"),
    "release_year":openapi.Schema(type=openapi.TYPE_NUMBER, title="Release Year"),
    "pages":openapi.Schema(type=openapi.TYPE_NUMBER, title="Pages"),
    "publishing_company":openapi.Schema(type=openapi.TYPE_STRING, title="Company"),
    "create_at":openapi.Schema(type=openapi.FORMAT_DATETIME, title="Create At"),
    "updated_at":openapi.Schema(type=openapi.FORMAT_DATETIME, title="Updated At"),
    "lent_book":openapi.Schema(type=openapi.TYPE_BOOLEAN, title="Lent Book"),
    "category":openapi.Schema(type=openapi.TYPE_INTEGER, title="Category"),
    "borrowed":openapi.Schema(type=openapi.TYPE_INTEGER, title="Borrowed"),
})

msg_user = {
    "username":openapi.Schema(type=openapi.TYPE_STRING, title="username"),
    "email":openapi.Schema(type=openapi.TYPE_STRING, title="email@gmail.com")
}

user_books = {
    200: openapi.Response(
        description='Success',
        schema=openapi.Schema(
            title="User Books",
            type=openapi.TYPE_ARRAY,
            items=msg_userbooks
        )
    )
}


login_res = {
    200: openapi.Response(
        description='Success message',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=msg_login
        )
    )
}

user_res = {
    200: openapi.Response(
        description='Success message',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=msg_user
        )
    )
}