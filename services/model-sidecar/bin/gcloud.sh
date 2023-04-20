#!/bin/bash
docker build --platform=linux/amd64 -t model-sidecar .
docker tag model-sidecar gcr.io/blog-model-hosting/model-sidecar
docker push gcr.io/blog-model-hosting/model-sidecar