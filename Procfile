# Use uma imagem base
FROM railwayapp/python:3.8

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . .

# Instale as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponha a porta do aplicativo
EXPOSE 5000

# Comando para iniciar o aplicativo
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]