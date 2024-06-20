FROM python:3.12-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt
ADD . /app
WORKDIR /app
ENTRYPOINT ["python", "main.py"]
