FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

ENV APP_ROOT /app
ENV CONFIG_ROOT /config

RUN apt update --fix-missing -y


ARG DEBIAN_FRONTEND=noninteractive
RUN apt install --fix-missing -y build-essential software-properties-common apt-utils \
    python3-dev python3-pip python3-setuptools python3-wheel python3-cffi python3-brotli git

RUN mkdir ${CONFIG_ROOT}
COPY ./requirements_sys.txt ${CONFIG_ROOT}/
COPY ./requirements_dev.txt ${CONFIG_ROOT}/
COPY ./requirements.txt ${CONFIG_ROOT}/

WORKDIR ${CONFIG_ROOT}
ARG DEBIAN_FRONTEND=noninteractive
RUN apt install --fix-missing -y $(grep -vE "^\s*#" requirements_sys.txt  | tr "\n" " ")

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN pip3 install -r ${CONFIG_ROOT}/requirements_dev.txt


COPY . ${APP_ROOT}/
WORKDIR ${APP_ROOT}

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
