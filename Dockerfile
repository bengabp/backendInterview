FROM python:3.11-slim


RUN mkdir -p /usr/app

WORKDIR /usr/app

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ADD . .

ENV PYTHONPATH .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
