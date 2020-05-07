FROM python:3.8.2-slim

COPY db/migration_manager.py /app/
WORKDIR /app 

COPY db/do_migrations.sh /app
COPY db/models.py /app
COPY db/requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD chmod +x do_migrations.sh
# CMD ["python3", "migration_manager.py", "db", "migrate"]
# CMD ["python3 migration_manager.py db migrate", ";", "python3 migration_manager.py db upgrade"]
