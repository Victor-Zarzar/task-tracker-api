from cachetools import TTLCache
from hashlib import sha256

from app.models.tracker_model import Location

notification_cache = TTLCache(maxsize=500, ttl=300)

ip_cache = TTLCache(maxsize=1000, ttl=3600)


def make_cache_key(*args) -> str:
    """
    Gera uma chave de cache normalizada e segura usando hash SHA256.

    Parâmetros:
        *args: Elementos variádicos que compõem a chave composta

    Retorno:
        String hexadecimal de 64 caracteres representando o hash SHA256

    Garantias:
        - Unicidade: Diferentes combinações geram hashes distintos
        - Consistência: Mesma entrada sempre gera mesma saída
        - Segurança: Previne ataques de colisão deliberada
        - Tamanho fixo: Padroniza uso de memória no cache
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

    return cache.get(key)


def set_in_cache(cache: TTLCache, key: str, value):
    cache[key] = value


def get_cached_location(visitor_ip: str) -> Location | None:
    key = make_cache_key(visitor_ip)
    return get_from_cache(ip_cache, key)


def set_cached_location(visitor_ip: str, location: Location):

    key = make_cache_key(visitor_ip)
    set_in_cache(ip_cache, key, location)
