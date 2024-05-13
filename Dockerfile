FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install coverage

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]