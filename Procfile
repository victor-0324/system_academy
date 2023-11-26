web: gunicorn -b 0.0.0.0:5000 run:app

FROM python:3.10.0

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]