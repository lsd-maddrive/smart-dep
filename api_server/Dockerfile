FROM python:3.8.2-slim

WORKDIR /app

COPY api_server/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY api_server/app.py .
COPY api_server/sockets.py .
COPY api_server/api_v1.py .
COPY api_server/api_func.py .
COPY api_server/auth.py .
COPY api_server/messages.py .
COPY api_server/database.py .
COPY db/models.py ./db/

# CMD ["gunicorn", "-k=gevent", "--workers=1", "-b=0.0.0.0:8080", "app:app"]
CMD ["gunicorn", "-k=geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "--workers=1", "-b=0.0.0.0:8080", "app:app"]
