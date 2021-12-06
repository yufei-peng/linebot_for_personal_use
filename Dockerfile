FROM python:3.9.9
WORKDIR /app
COPY requirements.txt /app
RUN pip install --default-timeout=100 -r requirements.txt
EXPOSE 5000
