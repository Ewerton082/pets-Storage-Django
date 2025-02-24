FROM python:3.12-slim

WORKDIR .

RUN apt update && apt install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    gcc \
    && apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["uwsgi", "--ini", "uwsgi.ini"]
