FROM python:3.8.2-slim

WORKDIR /app

COPY db/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY db/migration_manager.py .
COPY db/models.py .

CMD python3 migration_manager.py db migrate && python3 migration_manager.py db upgrade
