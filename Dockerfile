FROM python:3-alpine

RUN apk update \
  && apk upgrade \
  && apk add postgresql-dev \
  && pip install -U pip \
  && pip install gunicorn

RUN pip install flask \
  && pip install docker \
  && pip install flask_login \
  && pip install flask-restplus \
  && pip install docker-compose \
  && pip install sqlalchemy 




COPY . /app
WORKDIR /app

RUN pip install -e .

RUN mkdir -p /tmp/cache
ENV FLASK_APP=book_wish_list.book_wish_list
EXPOSE ${PORT}
WORKDIR /app/book_wish_list

CMD gunicorn -c /app/gunicorn.conf book_wish_list.app:app --log-level=debug --reload --bind 0.0.0.0:${PORT};
