FROM python:3.9.2

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o conteúdo local para o contêiner
COPY . /app

# Adiciona o caminho do mariadb_config ao PATH
ENV PATH /usr/bin:$PATH

# Define a variável MARIADB_CONFIG
ENV MARIADB_CONFIG /usr/bin/mariadb_config

# Instala as dependências do projeto
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta em que o aplicativo será executado
EXPOSE 5000

# Comando para iniciar o aplicativo quando o contêiner for iniciado
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]