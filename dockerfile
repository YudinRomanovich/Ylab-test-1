FROM python:3.10

RUN mkdir /ylab_app

WORKDIR /ylab_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
