from junitparser import JUnitXml, Element, Failure, Error, Skipped, TestCase
from uuid import uuid4
from datetime import datetime, timezone, timedelta
import requests, subprocess, os


# Maximum time of retries failed tests.
MAX_RETRIES = 2


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

    def retry_fails(self, xml_path: str = None) -> None:
        """Retry failed tests.

        Args:
            xml_path (str, optional): Path to the JUnit XML file. Defaults to None.
        """
        # Initilize xml object from own path or injected path
        if xml_path is not None:
            xml = JUnitXml.fromfile(xml_path)
        else:
            xml = JUnitXml.fromfile(self.xml_path)
        if not xml: return
        
        # Get failed tests from original run
        failed_tests = self._get_failed_tests(xml)
        if not failed_tests: return

        # Re-runs failed tests
        for attempt in range(1, MAX_RETRIES + 1):
            # Run previous failed results
            print(f"\n=== Attempt {attempt} ===")
            self._run_tests([test["test_path"] for test in failed_tests])

            # Load new failed results
            temp_xml = JUnitXml.fromfile(self.temp_xml_path)
            new_failed = self._get_failed_tests(temp_xml)

            # Compare with previous failed results
            # First create the list of test paths from new failed results
            new_test_paths = [test["test_path"] for test in new_failed]
            # Loop through old failed tests
            for test in failed_tests:
                if test["test_path"] not in new_test_paths:
                    # If test does not appear in new failed tests
                    # It means it passed this time,
                    # mark as unstable
                    test["case"].append(Unstable())

            # Update failed_tests for next iteration
            xml.write(self.xml_path)
            failed_tests = [t for t in failed_tests if t["case"].child(Unstable) is None]   

    def _get_failed_tests(self, xml: JUnitXml) -> list[dict[str, TestCase]]:
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
            return
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
            xml = JUnitXml.fromfile(xml_path)
        else:
            xml = JUnitXml.fromfile(self.xml_path)
        if not xml: return {}
        
        run_id = str(uuid4())
        summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "unstable": 0}
        test_execution_time = 0
        host_name = "<HOST_NAME>"
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
    
    def send_records(self, records: str, host: str, token: str, database: str) -> None:
        """Send records to InfluxDB.

        Args:
            records (str): record should be in line protocol format
            host (str): InfluxDB host URL
            token (str): InfluxDB authorization token
            database (str): InfluxDB database name
        """
        if not records:
            return

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
        return response
        