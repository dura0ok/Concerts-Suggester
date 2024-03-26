from elasticsearch import Elasticsearch

# Set up the Elasticsearch connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}], basic_auth=('elastic', '123321'))

# Define the search query
search_query = {
    "query": {
        "fuzzy": {
            "name": {
                "value": "Навасибирск",
                "fuzziness": "AUTO"
            }
        }
    }
}

# Specify the index and perform the search
index_name = "russian_cities"
response = es.search(index=index_name, body=search_query)

# Print the results
print("Search Results:")
print(response)
