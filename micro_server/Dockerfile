FROM python:3.8.2-slim

WORKDIR /app

COPY micro_server/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY micro_server/app.py .
COPY micro_server/sample_code.py .
COPY micro_server/api_v1.py .
COPY micro_server/database.py .
COPY micro_server/wsgi.py .
COPY db/models.py .

CMD ["gunicorn", "--workers=1", "-b=0.0.0.0:8080", "wsgi:create_app()"]
