import redis
from django.conf import settings


def redis_client():
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                               password=settings.REDIS_PASS, decode_responses=True)
    return redis_client
