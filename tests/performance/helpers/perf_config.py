import os

from dotenv import load_dotenv


load_dotenv()

HOST = os.getenv("BE_URL") or os.getenv("BASE_URL", "http://localhost:3000")
PERF_USER_EMAIL = os.getenv("PERF_SEEDED_USER_EMAIL", "bxh@gmail.com")
PERF_USER_PASSWORD = os.getenv("PERF_SEEDED_USER_PASSWORD", "Huy123456")
