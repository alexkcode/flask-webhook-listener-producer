FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install pika && \
    pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

# EXPOSE 5000

CMD [ "app.py" ]