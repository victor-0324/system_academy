web: gunicorn -b 0.0.0.0:$PORT run:app 

# Adicione essa linha antes da instalação das dependências
RUN apt-get update && apt-get install -y gettext

# Instale as dependências
RUN --mount=type=cache,id=s/1787dbb0-01da-4429-ad1c-28429e524268-/root/cache/pip,target=/root/.cache/pip python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt