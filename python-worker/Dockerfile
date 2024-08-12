FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3-dev

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-u" , "main.py"]