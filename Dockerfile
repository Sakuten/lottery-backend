FROM python:3.6-alpine3.8

ENV PIP_NO_CACHE_DIR=false \
    DB_GEN_POLICY=never \
    FLASK_CONFIGURATION=deployment \
    FLASK_APP=app.py \
    FLASK_ENV=production

COPY . /code
WORKDIR /code

RUN apk update && apk upgrade \
    && apk add --update --no-cache \
      --virtual .build-deps \
      libffi-dev build-base jpeg-dev libpng-dev postgresql-dev \
    && apk add --update --no-cache libffi jpeg \
    && pip install pipenv \
    && pipenv install --system \
    && pip uninstall -y pipenv \
    && apk del --purge .build-deps \
    && rm -rf /var/cache/apk/*


EXPOSE 80

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80", "--workers", "4"]
