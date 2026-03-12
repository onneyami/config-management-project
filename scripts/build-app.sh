#!/bin/bash
docker build -t dynamic-app:latest 02-dynamic-update/test-app/
kind load docker-image dynamic-app:latest