FROM python:3.8.2-slim

COPY logger.py /logger/
WORKDIR /logger 

COPY requirements.txt /logger 

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-c", "config.yml"]