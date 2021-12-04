FROM python:3.9.9
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
CMD python app.py