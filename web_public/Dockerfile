FROM python:3.9-slim
WORKDIR /app
RUN pip install flask markdown gunicorn
COPY . .
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app
