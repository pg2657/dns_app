FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install Flask
RUN pip install pytz
RUN pip install requests

EXPOSE 8080

CMD ["python", "us.py"]

