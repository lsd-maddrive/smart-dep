FROM python:3.8.2-slim

COPY db/migration_manager.py /app/
WORKDIR /app

COPY db/models.py /app
COPY db/db.py /app 
COPY db/requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python3 /app/migration_manager.py db migrate; python3 /app/migration_manager.py db upgrade
