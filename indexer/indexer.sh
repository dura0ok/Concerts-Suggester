#!/bin/bash

ELASTIC_USER=${ELASTIC_USER:-elastic}
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-123321}

# curl -XPOST -u elastic:123321 -H "Content-Type: application/json" http://elasticsearch:9200/_security/role/kibana_user -d '{
#   "cluster": ["monitor"],
#   "indices": [],
#   "applications": [],
#   "run_as": [],
#   "metadata": {}
# }'

# curl -XPOST -u elastic:123321 -H "Content-Type: application/json" http://elasticsearch:9200/_security/user/kibana_user -d '{
#   "password": "123321",
#   "roles": ["kibana_system"]
# }'

curl -XPOST -u elastic:123321 'http://elasticsearch:9200/_security/user/kibana_system/_password' -H "Content-Type: application/json" -d'
{
  "password": "123321"
}
'

curl -XPUT -H "Content-Type: application/json" \
    -u kibana_system:123321 \
    http://elasticsearch:9200/kibana

# Elasticsearch index creation
curl -s -X PUT "elasticsearch:9200/russian_cities" -H "Content-Type: application/json" -u "$ELASTIC_USER:$ELASTIC_PASSWORD" -d @index_mapping.json

# Run Python script to separate JSON data
python separator.py russian-cities.json /tmp/russian-cities-separated.json > /dev/null

# Bulk indexing into Elasticsearch
curl -s -X POST "elasticsearch:9200/russian_cities/_bulk" -H "Content-Type: application/json" -u "$ELASTIC_USER:$ELASTIC_PASSWORD" --data-binary "@/tmp/russian-cities-separated.json"

curl -f -s -X GET 'elasticsearch:9200/_cat/health?v' --user elastic:123321
