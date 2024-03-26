#!/bin/bash

ELASTIC_USER=${ELASTIC_USER:-elastic}
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-123321}

# Elasticsearch index creation
curl -X PUT "elasticsearch:9200/russian_cities" -H "Content-Type: application/json" -u "$ELASTIC_USER:$ELASTIC_PASSWORD" -d @index_mapping.json

# Run Python script to separate JSON data
python separator.py russian-cities.json /tmp/russian-cities-separated.json

# Bulk indexing into Elasticsearch
curl -X POST "elasticsearch:9200/russian_cities/_bulk" -H "Content-Type: application/json" -u "$ELASTIC_USER:$ELASTIC_PASSWORD" --data-binary "@/tmp/russian-cities-separated.json"
