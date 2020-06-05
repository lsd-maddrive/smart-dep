FROM python:3.8.2-slim

COPY api_server/app.py /app/
COPY api_server/sockets.py api_server/api_v1.py api_server/api_func.py /app/api_server/
COPY db/models.py db/database.py /app/db/
WORKDIR /app

COPY api_server/requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["gunicorn", "-k=gevent", "--workers=1", "-b=0.0.0.0:8080", "app:app"]
CMD ["gunicorn", "-k=geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "--workers=1", "-b=0.0.0.0:8080", "app:app"]