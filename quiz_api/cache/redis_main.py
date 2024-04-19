from config import RD_HOST, RD_PORT
from redis import Redis
from cache.redis_class import RedisCache

redis_client = Redis(host=RD_HOST, port=RD_PORT, db=0, decode_responses=True)

cache = RedisCache(redis_client)