FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
COPY requirements /config/requirements
RUN pip install -r /config/requirements/dev.txt
RUN mkdir /src;
WORKDIR /src
