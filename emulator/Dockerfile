FROM python:3.8.2-slim

COPY app.py config.yml /emulator/
WORKDIR /emulator 

COPY requirements.txt /emulator 
# just in case 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "/emulator/app.py"]
