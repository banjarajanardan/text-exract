FROM python:3.8-slim-buster

COPY . .

RUN pip3 install -r app/requirements.txt


EXPOSE $PORT

CMD [ "bash", "runserver.sh" ]