import redis


redis_client = redis.StrictRedis(host='localhost', port=6379, password='123321', decode_responses=True)
redis_client.set('example_key', 'example_value')
value = redis_client.get('example_key')
print(value)
