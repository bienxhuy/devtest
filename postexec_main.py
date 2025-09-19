from postexec import PostExec
from dotenv import load_dotenv
import os
from logs.logger import get_logger

# Get a logger instance for logging within the postexec
logger = get_logger()
# Load configuration
load_dotenv()
JUNIT_PATH = os.getenv("JUNIT_PATH", "./postexec/junit.xml")
INFLUX_HOST = os.getenv("INFLUX_HOST")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE")
RUN_TABLE = "build_summaries"
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local_run")
BUILD_URL = os.getenv("BUILD_URL", "http://localhost:8080/job/devtest")
BRANCH = os.getenv("BRANCH", "local_branch")
AUTHOR = os.getenv("AUTHOR", "local_author")
HOST = os.getenv("HOST", "local_host")


def format_summary_to_line_protocol(data: dict) -> str:
    """Format summary to InfluxDB line protocol."""
    tags = (
        f"build_number={BUILD_NUMBER},"
        f"build_url={BUILD_URL},"
        f"run_id={data['run_id']},"
        f"branch={BRANCH},"
        f"author={AUTHOR},"
        f"host={HOST}"
    )
    fields = (
        f"total={data['total']},"
        f"passed={data['passed']},"
        f"failed={data['failed']},"
        f"skipped={data['skipped']},"
        f"unstable={data['unstable']},"
        f"pass_rate={data['passed'] * 100 / data['total'] if data['total'] > 0 else 0},"
        f"execution_time={data['execution_time']},"
        f"mean_test_duration={data['mean_test_duration']}"
    )
    line = f"{RUN_TABLE},{tags} {fields} {data['timestamp']}"
    return line


if __name__ == "__main__":
    logger.info("Starting post-execution processing.")
    postexec = PostExec(path=JUNIT_PATH, temp="./postexec/temp.xml")
    logger.info(f"Starting retry of failed tests from {JUNIT_PATH}.")
    postexec.retry_fails()
    logger.info("Retry completed. Generating summary.")
    summ = postexec.summary()
    logger.info(f"Summary generated: {summ}")
    logger.info("Sending summary to InfluxDB.")
    result = postexec.send_records(
        records=[format_summary_to_line_protocol(summ)],
        host=INFLUX_HOST,
        token=INFLUX_TOKEN,
        database=INFLUX_DATABASE
    )
    logger.info(f"InfluxDB response: {result.status_code} - {result.text}")
