FROM python:3.11-slim
LABEL org.opencontainers.image.source=https://github.com/immunoodle/data-portal-ingest-api
RUN apt update -qq && apt upgrade -y
WORKDIR /api
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
# CMD flask --app api run --host=0.0.0.0 

CMD gunicorn --bind 0.0.0.0:5000 --log-level DEBUG api:app
