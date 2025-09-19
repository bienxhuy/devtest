from postexec import PostExec, Unstable
from dotenv import load_dotenv
import os
from logs.logger import get_logger
from junitparser import TestCase


# Get a logger instance for logging within the postexec
logger = get_logger()
# Load configuration
load_dotenv()
JUNIT_PATH = os.getenv("JUNIT_PATH", "./postexec/junit.xml")
INFLUX_HOST = os.getenv("INFLUX_HOST")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local_run")
BUILD_URL = os.getenv("BUILD_URL", "http://localhost:8080/job/devtest")
BRANCH = os.getenv("BRANCH", "local_branch")
AUTHOR = os.getenv("AUTHOR", "local_author")
HOST = os.getenv("HOST", "local_host")
BUILD_SUMMARIES_TABLE = "build_summaries"
FAILED_TESTS_TABLE = "failed_tests"


def format_failed_tests_list_to_line_protocol(
    data: list[TestCase], run_id: str, timestamp: int
    ) -> list[str]:
    """Format failed tests list to line protocol list."""
    lines = []
    for testcase in data:
        tags = (
            f"run_id={run_id},"
            f"suite={testcase.classname},"
            f"test_name={testcase.name}"
        )
        fields = (
            f'status="{ "UNSTABLE" if testcase.child(Unstable) else "FAILURE" }",'
            f"exec_time={testcase.time}"
        )
        line = f"{FAILED_TESTS_TABLE},{tags} {fields} {timestamp}"
        lines.append(line)
    return lines


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
    line = f"{BUILD_SUMMARIES_TABLE},{tags} {fields} {data['timestamp']}"
    return line


if __name__ == "__main__":
    logger.info("[POST EXECUTION] - Starting post-execution processing.")
    postexec = PostExec(path=JUNIT_PATH, temp="./postexec/temp.xml")
    
    # # Retry failed test cases
    # logger.info(f"[POST EXECUTION] - Starting retry of failed tests from {JUNIT_PATH}.")
    # postexec.retry_fails()
    
    logger.info("[POST EXECUTION] - Retry completed. Generating summary.")
    summ = postexec.summary()
    logger.info(f"[POST EXECUTION] - Summary generated: {summ}")
    
    logger.info("[POST EXECUTION] - Retrieving failed_tests list and formatting to line protocol")
    failed_tests_dict = postexec.get_failed_tests(postexec.get_xml_junit_object())
    failed_tests = [test['case'] for test in failed_tests_dict]
    results = format_failed_tests_list_to_line_protocol(
        data=failed_tests, 
        run_id=summ['run_id'], 
        timestamp=summ['timestamp']
    )
    logger.info("[POST EXECUTION] - Done retrieving and formating failed tests")
    
    logger.info("[POST EXECUTION] - Adding summary as line protocol to results")
    summary_line = format_summary_to_line_protocol(summ)
    results.append(summary_line)
    logger.info("[POST EXECUTION] - Added summary as line protocol to results")
    
    logger.info("[POST EXECUTION] - Sending results to InfluxDB.")
    postexec.send_records(
        records=results,
        host=INFLUX_HOST,
        token=INFLUX_TOKEN,
        database=INFLUX_DATABASE
    )
