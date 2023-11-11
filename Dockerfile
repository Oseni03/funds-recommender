FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir /code

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python pkg/manage.py runserver