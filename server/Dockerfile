FROM python:3

# FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt update && apt install openssl

RUN python -m pip install --upgrade pip

RUN pip install pika && \
    pip install -r requirements.txt

COPY . /app

# ENTRYPOINT [ "python3" ]

# EXPOSE 5000

CMD [ "python3", "app.py" ]

# CMD ["gunicorn", "--config", "gunicorn-conf.py", "--bind", "0.0.0.0:5000", "app:app"]