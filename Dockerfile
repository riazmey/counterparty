#FROM python:3.13
FROM python:latest-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -eux
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y \
  libpq-dev \
  gcc \
  curl \
  git \
  nano \
  ;

WORKDIR /app
RUN git clone --branch main https://github.com/riazmey/counterparty.git

WORKDIR /app/counterparty
RUN pip3 install --no-cache-dir -r requirements.txt

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["bash"]
