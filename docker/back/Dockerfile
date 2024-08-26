FROM python:latest

WORKDIR /code

COPY back/requirements.txt /code/requirements.txt

RUN pip install --upgrade -r requirements.txt

COPY back/ /code/

COPY docker/back/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
