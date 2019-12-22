FROM python:3.7.6-slim
MAINTAINER rudeigerc@gmail.com
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
CMD python -m uranus_middleware.app
