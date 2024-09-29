# Dockerfile
FROM python:3.8.10

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta da aplicação Django (padrão 8000)
EXPOSE 8000

