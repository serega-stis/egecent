FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
WORKDIR /backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]