FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
RUN apk add bash curl git nano

RUN pip install --upgrade pip

WORKDIR /app
RUN git clone --branch main https://github.com/riazmey/counterparty.git

WORKDIR /app/counterparty
RUN pip3 install --no-cache-dir -r requirements.txt

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["bash"]
