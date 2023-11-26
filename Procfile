web: python run.py


# Use uma imagem base Python
FROM python:3.10

# Configuração do diretório de trabalho
WORKDIR /Innovare

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código-fonte para o diretório de trabalho
COPY . .

# Comando de inicialização do aplicativo
CMD ["python", "run.py"]
