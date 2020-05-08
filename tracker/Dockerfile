FROM python:3.8.2-slim

COPY tracker/tracker.py /app/
WORKDIR /app 

COPY db/models.py /app
COPY tracker/requirements.txt /app 

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "tracker.py"] 