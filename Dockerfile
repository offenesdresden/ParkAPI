FROM python:3.6-slim

COPY . .

RUN apt-get -q update && \
    apt-get -q install -y \
    git \
    && rm -r /var/lib/apt/lists/*

RUN ["pip", "install", "-e", "."]

ENTRYPOINT ["python", "bin/parkapi-server"]
