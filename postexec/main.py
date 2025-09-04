from postexec.summary import summary
from write import send_records
from dotenv import load_dotenv
import os


# Load configuration
load_dotenv()
JUNIT_PATH = os.getenv("JUNIT_PATH", "junit.xml")


if __name__ == "__main__":
    records = summary(JUNIT_PATH, {})
    print(records)
    send_records(records)