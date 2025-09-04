# write_points.py
import requests
import os
from dotenv import load_dotenv


# Load influxdb configuration
load_dotenv()
INFLUX_HOST = os.getenv("INFLUX_HOST")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE")


# Function to send records to influxdb
# Receive records as list of strings
def send_records(records):
    if not records:
        return

    # Base URL to write & parameters
    url = f"{INFLUX_HOST}/api/v3/write_lp?"
    url += f"db={INFLUX_DATABASE}&precision=microsecond&accept_partial=true&no_sync=true"
    # HTTP header & data
    headers = {
        "Authorization": f"Token {INFLUX_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }
    data = "\n".join(records)
    print(data)
    # Send request & handle response
    # response = requests.post(url, headers=headers, data=data)
    # print(response)

