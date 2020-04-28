FROM python:3.8.2-slim

COPY logger/logger.py /app/
WORKDIR /app 

COPY shared/models/table_models.py /app
COPY logger/requirements.txt /app 

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "logger.py", "-c", "config.yml"]