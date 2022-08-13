FROM python:3.10

ENV TZ=America/Sao_Paulo

WORKDIR /home

RUN apt-get update && \
    apt-get -qq -y install netcat-openbsd

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src/ .

COPY ./tests/ .

COPY ./start.sh .

RUN chmod +x start.sh

CMD ./start.sh
