FROM python:3

RUN pip install -U pip \
  && pip install flask \
  && pip install gunicorn \
  && pip install docker \
  && pip install flask-restplus \
  && pip install flask-sqlalchemy \
  && pip install docker-compose \
  && pip install sqlalchemy \
  && pip install sqlalchemy_utils \
  && pip install passlib \
  && pip install psycopg2 \
  && pip install pytest \
  && pip install pytest-cov \
  && pip install pytest-flask

COPY . /app
WORKDIR /app

ENTRYPOINT ["pytest", "-p", "no:cacheprovider", "--cov"]
