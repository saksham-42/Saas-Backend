from slowapi import Limiter
from slowapi.util import get_remote_address
import os

def get_limit(limit:str):
    "Return limit in production, but bypass in testing"
    if os.getenv("TESTING") == "true":
        return "10000/minute"
    return limit

limiter = Limiter(key_func=get_remote_address)