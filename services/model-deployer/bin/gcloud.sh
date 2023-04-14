#!/bin/bash
docker build --platform=linux/amd64 -t model-runtime .
docker tag model-runtime gcr.io/blog-model-hosting/model-runtime
docker push gcr.io/blog-model-hosting/model-runtime