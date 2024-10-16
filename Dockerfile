# Utilize uma imagem base oficial de Python
FROM python:3.12

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Exponha a porta em que sua aplicação irá rodar
EXPOSE 8000

# Comando para executar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

# CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]

