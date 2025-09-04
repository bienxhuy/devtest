from postexec import PostExec
from dotenv import load_dotenv
import os


# Load configuration
load_dotenv()
JUNIT_PATH = os.getenv("JUNIT_PATH", "./postexec/junit.xml")
INFLUX_HOST = os.getenv("INFLUX_HOST")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE")
RUN_TABLE = "build_summaries"


def format_summary_to_line_protocol(data: dict) -> str:
    """Format a dictionary to InfluxDB line protocol.

    Args:
        data (dict): The dictionary to format.

    Returns:
        str: The formatted line protocol string.
    """
    tags = f"run_id={data['run_id']},host_name={data['host_name']}"
    fields = (
        f"total={data['total']},"
        f"passed={data['passed']},"
        f"failed={data['failed']},"
        f"skipped={data['skipped']},"
        f"unstable={data['unstable']},"
        f"execution_time={data['execution_time']},"
        f"mean_test_duration={data['mean_test_duration']}"
    )
    line = f"{RUN_TABLE},{tags} {fields} {data['timestamp']}"
    return line


if __name__ == "__main__":
    postexec = PostExec(path=JUNIT_PATH, temp="./postexec/temp")
    postexec.retry_fails()
    summ = postexec.summary()
    print(postexec.send_records(
        records=[format_summary_to_line_protocol(summ)],
        host=INFLUX_HOST,
        token=INFLUX_TOKEN,
        database=INFLUX_DATABASE
    ))
