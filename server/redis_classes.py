import redis


class RedisManager():

    def __init__(self, host, port, db):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def do_set(self, key, value):
        self.redis_client.set(name=f'{key}', value=value)

    def do_get_all(self):
        data = {}

        keys = self.redis_client.keys('*')
        if keys:
            for key in keys:
                data.update({
                    f"{key}": self.redis_client.get(key),
                })
        return data

    def close(self):
        self.redis_client.close()
