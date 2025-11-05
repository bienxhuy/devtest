from junitparser import JUnitXml, Element, Failure, Error, Skipped, TestCase
from uuid import uuid4
from datetime import datetime
import requests, subprocess, os
from logs.logger import get_logger


# Maximum time of retries failed tests.
MAX_RETRIES = 2
# Get a logger instance for logging within the postexec
logger = get_logger()


class Unstable(Element):
    """Test result when case is unstable (fail then pass)"""
    
    _tag = "unstable"
    

class PostExec():
    
    context = {}
    xml_path = ""
    temp_xml_path = ""

    def __init__(self, path: str, temp: str = "temp.xml", context: dict = {}):
        self.context = context
        self.xml_path = path
        self.temp_xml_path = temp
        
    def get_xml_junit_object(self) -> JUnitXml:
        """Get xml JUnitXml object from instance's xml_path"""
        return JUnitXml.fromfile(self.xml_path)

    def retry_fails(self, xml_path: str = None) -> None:
        """Retry failed tests.

        Args:
            xml_path (str, optional): Path to the JUnit XML file. Defaults to None.
        """
        # Initilize xml object from own path or injected path
        if xml_path is not None:
            logger.info(f"[POST EXECUTION] - Loading JUnit XML from {xml_path}.")
            xml = JUnitXml.fromfile(xml_path)
        else:
            logger.info(f"[POST EXECUTION] - Loading JUnit XML from {self.xml_path}.")
            xml = JUnitXml.fromfile(self.xml_path)
        if not xml: 
            logger.info(f"[POST EXECUTION] - No JUnit XML found, skipping retry of failed tests.")
            return
        logger.info(f"[POST EXECUTION] - JUnit XML loaded successfully.")
        
        # Get failed tests from original run
        logger.info(f"[POST EXECUTION] - Extracting failed tests from JUnit XML.")
        failed_tests = self.get_failed_tests(xml)
        if not failed_tests: 
            logger.info(f"[POST EXECUTION] - No failed tests found, skipping retry.")
            return
        logger.info(f"[POST EXECUTION] - Found {len(failed_tests)} failed tests to retry.")

        # Re-runs failed tests
        logger.info(f"[POST EXECUTION] - Starting retry of failed tests for {MAX_RETRIES} times.")
        for attempt in range(1, MAX_RETRIES + 1):
            # Run previous failed results
            logger.info(f"[POST EXECUTION] - === Attempt {attempt} ===")
            self._run_tests([test["test_path"] for test in failed_tests])
            logger.info(f"[POST EXECUTION] - Retry run completed.")

            # Load new failed results
            logger.info(f"[POST EXECUTION] - Loading results of retried tests.")
            temp_xml = JUnitXml.fromfile(self.temp_xml_path)
            new_failed = self.get_failed_tests(temp_xml)
            logger.info(f"[POST EXECUTION] - Remaining {len(new_failed)} failed tests after retry.")

            # Compare with previous failed results to recognize unstable tests
            logger.info(f"[POST EXECUTION] - Comparing failed tests to identify unstable tests.")
            # First create the list of test paths from new failed results
            new_test_paths = [test["test_path"] for test in new_failed]
            # Loop through old failed tests
            for test in failed_tests:
                if test["test_path"] not in new_test_paths:
                    # If test does not appear in new failed tests
                    # It means it passed this time,
                    # mark as unstable
                    test["case"].append(Unstable())
                    logger.info(f"[POST EXECUTION] - Test {test['test_path']} marked as unstable.")
            logger.info(f"[POST EXECUTION] - Unstable test marking completed.")

            # Update failed_tests for next iteration
            logger.info(f"[POST EXECUTION] - Rewriting the JUnit XML file.")
            xml.write(self.xml_path)
            logger.info(f"[POST EXECUTION] - JUnit XML file updated.")
            logger.info(f"[POST EXECUTION] - Preparing for next retry iteration.")
            failed_tests = [t for t in failed_tests if t["case"].child(Unstable) is None]
            if (len(failed_tests) == 0):
                logger.info(f"[POST EXECUTION] - All tests passed or marked unstable, ending retries.")
                break 
            logger.info(f"[POST EXECUTION] - {len(failed_tests)} tests remain failed for next retry.")

    def get_failed_tests(self, xml: JUnitXml) -> list[dict[str, TestCase]]:
        """Get a list of failed tests from the JUnit XML.

        Args:
            xml (JUnitXML): The JUnit XML object 
                            that needs to be parsed for failed tests.

        Returns:
            list: A list of failed element test cases, each contains
                path to the test case and the corresponding TestCase object.
        """
        failed = []
        for suite in xml:
            for case in suite:
                if case.is_failure or case.is_error:
                    failed.append({
                        "test_path": f"{case.classname.replace('.', os.sep)}.py::{case.name}",
                        "case": case
                        })
        return failed

    def _run_tests(self, failed_tests_paths: list[str]) -> None:
        """Rerun failed tests.

        Args:
            failed_tests_paths (list[str]): Paths to the failed test cases.
        """
        if not failed_tests_paths:
            logger.info(f"[POST EXECUTION] - No failed tests to rerun.")
            return
        logger.info(f"[POST EXECUTION] - Rerunning {len(failed_tests_paths)} failed tests.")
        cmd = ["pytest", "-v", f"--junitxml={self.temp_xml_path}"] + failed_tests_paths
        subprocess.run(cmd)

    def summary(self, xml_path: str = None, context: dict = None) -> dict:
        """Generate a summary of test results.

        Args:
            xml_path (str, optional): Path to the JUnit XML file. 
                                    Defaults to None.

        Returns:
            dict: Summary of test results.
        """
        if xml_path is not None:
            logger.info(f"[POST EXECUTION] - Loading JUnit XML file from {xml_path}.")
            xml = JUnitXml.fromfile(xml_path)
        else:
            logger.info(f"[POST EXECUTION] - Loading JUnit XML file from {self.xml_path}.")
            xml = JUnitXml.fromfile(self.xml_path)
        logger.info(f"[POST EXECUTION] - JUnit XML loaded successfully.")
        if not xml: return {}
        
        logger.info(f"[POST EXECUTION] - Generating test summary.")
        run_id = str(uuid4())
        summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "unstable": 0}
        test_execution_time = 0
        total_test_time = 0

        # Loop through test suites and cases
        # Because of pytest, there's only 1 suite
        for suite in xml:
            # Extract information of that suite
            # timestamp = int(datetime.fromisoformat(suite.timestamp) \
            #                     .replace(tzinfo=timezone(timedelta(hours=7))) \
            #                     .timestamp() * 1000000)
            timestamp = int(datetime.fromisoformat(suite.timestamp).timestamp() * 1000000)
            test_execution_time = suite.time or 0

            # Because of pytest, there's only 1 suite
            # So, this loop will loop through all test cases in the process
            for case in suite:
                # Pre mark as passed
                status = "passed"
                
                # Check for real status
                failed = case.child(Failure) or case.child(Error)
                skipped = case.child(Skipped)
                unstable = case.child(Unstable)
                
                if unstable is not None:
                    status = "unstable"
                elif failed is not None:
                    status = "failed"
                elif skipped is not None:
                    status = "skipped"

                # Update summary
                summary["total"] += 1
                summary[status] += 1
                total_test_time += case.time or 0

        logger.info(f"[POST EXECUTION] - Test summary: {summary}")
        return {
            "run_id": run_id,
            "timestamp": timestamp,
            "total": summary["total"],
            "passed": summary["passed"],
            "failed": summary["failed"],
            "skipped": summary["skipped"],
            "unstable": summary["unstable"],
            "execution_time": test_execution_time,
            "mean_test_duration": 
                total_test_time / summary["total"] if summary["total"] > 0 else 0,
        }
    
    def send_records(self, records: list[str], host: str, token: str, database: str) -> None:
        """Send records to InfluxDB.

        Args:
            records (str): record should be in line protocol format
            host (str): InfluxDB host URL
            token (str): InfluxDB authorization token
            database (str): InfluxDB database name
        """
        if not records:
            logger.info(f"[POST EXECUTION] - No records to send to InfluxDB.")
            return

        logger.info(f"[POST EXECUTION] - Sending records to InfluxDB at {host}.")
        # Base URL to write & parameters
        url = f"{host}/api/v3/write_lp?"
        url += f"db={database}&precision=microsecond&accept_partial=true&no_sync=true"
        # HTTP header & data
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "text/plain; charset=utf-8"
        }
        data = "\n".join(records)
        
        # Send request & handle response
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 204:
            logger.info(f"[POST EXECUTION] - Records sent to InfluxDB successfully.")
        else:
            logger.error(f"Failed to send records to InfluxDB: {response.status_code} - {response.text}")
        return response
        