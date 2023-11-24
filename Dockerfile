FROM python:3.11-alpine

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]
