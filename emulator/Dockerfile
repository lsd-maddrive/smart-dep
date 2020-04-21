FROM python:3.8.2-slim

COPY app.py /emulator/
WORKDIR /emulator 

COPY requirements.txt /emulator 

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
