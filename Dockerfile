FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add requirements packages
RUN apk update
RUN apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
RUN apk add bash curl git nano

# Add ru_RU locale
RUN apk add tzdata
RUN cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime
ENV TZ=Europe/Moscow
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8

# Set timezone
RUN echo "Europe/Moscow" > /etc/timezone

# Upgrade python-pip
RUN pip install --upgrade pip

WORKDIR /app
RUN git clone --branch main https://github.com/riazmey/counterparty.git

WORKDIR /app/counterparty
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash"]
