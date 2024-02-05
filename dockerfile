FROM python:3.10-slim

# RUN mkdir /code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

RUN cd app/

CMD ["gunicorn", "app.main:app", "--workers 1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
