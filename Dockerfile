FROM ubuntu:18.04 AS base

RUN apt-get update && apt-get upgrade -y

RUN apt-get update && apt-get install -y \
    apt-utils \
    cups-filters \
    cups-client \
    python3 \
    python3-pip

RUN apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt

WORKDIR /
COPY ./entrypoint/. /entrypoint
RUN chmod +x /entrypoint/entrypoint.sh

RUN mkdir -p /app
COPY ./config.py /app
COPY ./mvcapp.py /app
COPY ./api.py /app
COPY ./wsgi.py /app

RUN mkdir -p /install
WORKDIR /install
COPY ./requirements.txt /install
RUN pip3 install --no-cache-dir -r /install/requirements.txt

WORKDIR /usr/lib/cups/filter/
COPY ./drivers/raster/x86_64/. .
RUN chmod +x *

WORKDIR /usr/share/ppd/cupsfilters/
COPY ./drivers/ppd/x86_64/. .
RUN chmod +x *.ppd

WORKDIR /app
ENTRYPOINT ["/entrypoint/entrypoint.sh"]
