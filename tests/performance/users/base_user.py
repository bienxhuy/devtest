from locust import HttpUser

from helpers.perf_config import HOST


class BasePerfUser(HttpUser):
    host = HOST
