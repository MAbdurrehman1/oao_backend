FROM python:3.11-slim

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /src/requirements.txt
COPY ./Makefile /src/Makefile
COPY ./entry_point.sh /src/entry_point.sh
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    make \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN curl -s https://packagecloud.io/install/repositories/golang-migrate/migrate/script.deb.sh | bash

RUN apt-get install migrate=4.17.1

COPY ./src /src
COPY ./static /static

CMD ["sh","entry_point.sh"]