FROM python:3.10

ENV TZ=America/Sao_Paulo

WORKDIR /home

RUN apt-get update && \
    apt-get -qq -y install netcat-openbsd

COPY docker/requirements.txt .

RUN pip install -r requirements.txt

COPY ./src/ .

COPY ./start.sh .

RUN chmod +x start.sh

EXPOSE 5000

CMD ./start.sh
