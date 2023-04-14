FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME


COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# EXPOSE $PORT
CMD exec python3 run.py