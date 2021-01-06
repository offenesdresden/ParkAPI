FROM python:3.7-alpine
LABEL maintainer="Max Schorradt <schorradt@publicplan.de>"

ENV port=5000
ENV host=0.0.0.0
ENV database_uri=postgresql://parkapi:parkapi@postgres/parkapi
ENV debug=false
ENV live_scrape=false

RUN apk add --no-cache postgresql-dev build-base git

COPY . /app
WORKDIR /app

RUN pip install -e .

EXPOSE 5000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
