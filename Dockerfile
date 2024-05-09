FROM python:3.10-alpine


WORKDIR /app

COPY . /app
COPY .env.example /app/.env
RUN pip install -r requirements.txt
EXPOSE 9999

CMD ["python3", "server.py"]
