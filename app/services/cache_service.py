from hashlib import sha256

from cachetools import TTLCache

from app.models.location import Location

notification_cache = TTLCache(maxsize=500, ttl=300)

ip_cache = TTLCache(maxsize=1000, ttl=3600)


def make_cache_key(*args) -> str:
    """
    Generates a normalized and secure cache key using SHA256 hash.
    """
    return sha256("-".join(map(str, args)).encode()).hexdigest()


def is_already_notified(visitor_ip: str, channel: str) -> bool:
    """
    Returns True if we have already sent a notification to this IP on the specified channel.
    """
    key = f"{channel}:{visitor_ip}"
    return key in notification_cache


def mark_notified(visitor_ip: str, channel: str):
    """
    Marks the IP as already notified in the channel.
    """
    key = f"{channel}:{visitor_ip}"
    notification_cache[key] = True


def get_from_cache(cache: TTLCache, key: str):
    """
    Retrieves a value from the cache if it exists, otherwise returns None.
    """
    return cache.get(key)


def set_in_cache(cache: TTLCache, key: str, value):
    cache[key] = value
    """
    Sets a value in the cache.
    """


def get_cached_location(visitor_ip: str) -> Location | None:
    key = make_cache_key(visitor_ip)
    return get_from_cache(ip_cache, key)
    """
    Retrieves the cached location for the given IP, or None if not cached.
    """


def set_cached_location(visitor_ip: str, location: Location):
    key = make_cache_key(visitor_ip)
    set_in_cache(ip_cache, key, location)
    """
    Caches the location for the given IP.
    """
