FROM python:3.8.2-slim

WORKDIR /app

COPY tracker/requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY db/models.py /app
COPY tracker/tracker.py /app/

CMD ["python3", "tracker.py"]