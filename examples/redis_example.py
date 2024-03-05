import redis

# Замените 'your_password' на фактический пароль, если он был установлен
redis_password = '123321'

# Подключение к Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, password=redis_password, decode_responses=True)

# Пример использования: установка значения
redis_client.set('example_key', 'example_value')

# Пример использования: получение значения
value = redis_client.get('example_key')
print(value)
