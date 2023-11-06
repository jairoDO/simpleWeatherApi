FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV COUNT 10
COPY . /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
WORKDIR /code