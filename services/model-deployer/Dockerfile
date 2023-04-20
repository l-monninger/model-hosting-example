FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME


COPY . .
# copy default creds
COPY ./.creds/gac.json ~/.config/gcloud/application_default_credentials.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# EXPOSE $PORT
CMD exec python3 run.py