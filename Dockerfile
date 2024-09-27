FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["python3", "app.py"]