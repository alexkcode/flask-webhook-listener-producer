FROM python:3.9

# FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt update && apt install openssl

RUN python -m pip install --upgrade pip

RUN pip install pika && \
    pip install -r requirements.txt

# COPY ./app /app

COPY . /app

# ENTRYPOINT [ "python3" ]

# EXPOSE 5000

# CMD ["uwsgi", "--ini", "uwsgi.ini"]

CMD [ "python3", "main.py" ]

# CMD ["gunicorn", "--config", "gunicorn-conf.py", "--bind", "0.0.0.0:5000", "app:app"]