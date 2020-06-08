FROM python:3.8.2-slim

WORKDIR /emulator

COPY requirements.txt /emulator

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /emulator/

CMD ["python3", "app.py"]
