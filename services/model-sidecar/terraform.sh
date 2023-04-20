#!/bin/bash
# login to gcloud service account
gcloud auth activate-service-account gdg-ultra@trans-sunset-363917.iam.gserviceaccount.com --key-file=./.creds/gdg-ultra-sa.json
export GOOGLE_APPLICATION_CREDENTIALS=./.creds/gdg-ultra-sa.json
terraform "$@"