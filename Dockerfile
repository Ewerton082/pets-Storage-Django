FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron procps nano dos2unix

COPY . /app/

COPY cronjob /etc/cron.d/cronjob

RUN dos2unix /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN service cron start

EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]
