FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get update \
        -o Acquire::Retries=5 \
        -o Acquire::http::No-Cache=True \
        -o Acquire::https::No-Cache=True \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        openssh-client \
        iputils-ping \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY . /app

RUN mkdir -p \
    /app/storage/preview \
    /app/storage/AW100 \
    /app/storage/AW200

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "App:app"]