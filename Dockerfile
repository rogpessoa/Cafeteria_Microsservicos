FROM python:latest

# Instala dependências
RUN pip install Flask requests

# Cria diretório padrão (ainda será ajustado pelo docker-compose)
RUN mkdir /app
WORKDIR /app

# Copia tudo (o código será usado conforme o contexto de build)
COPY . .

# O docker-compose irá mudar o WORKDIR dinamicamente
CMD ["python", "app.py"]