#!/bin/bash

docker-compose stop
docker-compose rm -f
docker-compose up -d --build