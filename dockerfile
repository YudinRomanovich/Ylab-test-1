FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
