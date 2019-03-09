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
  && pip install psycopg2




COPY . /app
WORKDIR /app

RUN pip install -e .

RUN mkdir -p /tmp/cache
ENV FLASK_APP=book_wish_list.book_wish_list
EXPOSE ${PORT}
WORKDIR /app/book_wish_list

CMD gunicorn -c /app/gunicorn.conf book_wish_list.run:app --log-level=debug --reload --bind 0.0.0.0:${PORT};
