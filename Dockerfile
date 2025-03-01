FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]
