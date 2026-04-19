FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*; exit 0

COPY requirements.txt .

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

COPY manage.py .
COPY todo ./todo

RUN python3 manage.py collectstatic --no-input
