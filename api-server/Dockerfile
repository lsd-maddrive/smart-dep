FROM python:3.8.2-slim

COPY api-server/app.py api-server/sockets.py api-server/api_v1.py /app/
COPY db/models.py db/database.py /app/
WORKDIR /app

COPY api-server/requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["gunicorn", "-k=gevent", "--workers=1", "-b=0.0.0.0:8080", "app:app"]
CMD ["gunicorn", "-k=geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "--workers=1", "-b=0.0.0.0:8080", "app:app"]
