FROM python:3.10-alpine
WORKDIR /shop
COPY requirements.txt /shop/
RUN pip install -r requirements.txt

COPY . /shop/