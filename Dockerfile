FROM python:3.8-slim-buster
WORKDIR /app/old-crawler

COPY requirements.txt /app/old-crawler/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get purge -y \
    && apt-get autoremove --purge -y

COPY . /app/old-crawler

RUN chmod 755 /app/old-crawler/docker-entrypoint.sh

ENTRYPOINT ["/app/old-crawler/docker-entrypoint.sh"]