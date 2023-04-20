FROM python:3.10-alpine

RUN apk add terraform --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME


COPY . .
# copy default creds
COPY ./.creds/gac.json ~/.config/gcloud/application_default_credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=./.creds/gac.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# EXPOSE $PORT
CMD terraform init && exec python3.10 run.py