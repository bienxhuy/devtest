from junitparser import JUnitXml, Element, Failure, Error, Skipped, TestCase
from uuid import uuid4
import csv, os, requests, subprocess
from requests import Response
from core.postexec.performance_result import PerformanceLineResult, PerformanceFailureResult, PerformanceResult
from core.utils.logs import get_logger


# Maximum time of retries failed tests.
MAX_RETRIES = 2
# Get a logger instance for logging within the postexec
logger = get_logger()


class Unstable(Element):
    """Test result when case is unstable (fail then pass)"""
    
    _tag = "unstable"
    

class PostExec():
    
    _context = {}
    _file_path = ""
    _secondary_path = ""
    # Situational attributes for retrying failed tests
    _temp_retry_path = "temp_retry_results.xml"
    _xml_object = None
    _csv_object = None

    def __init__(self, path: str, context: dict, secondary_path: str = None) -> None:
        self._context = context
        self._file_path = path
        self._secondary_path = secondary_path

    def _generate_xml_object(self) -> JUnitXml:
        """Generate a JUnitXml object from the XML file path."""      
        logger.info(f"[POST EXECUTION] - Loading JUnit XML from {self._file_path}.")
        try:
            self._xml_object = JUnitXml.fromfile(self._file_path)
            logger.info(f"[POST EXECUTION] - JUnit XML loaded successfully.")
            return self._xml_object
        except Exception as exc:
            logger.error(f"[POST EXECUTION] - Failed to load JUnit XML: {exc}")
            return None

    def retry_fails(self) -> None:
        """Retry failed tests.
        """
        logger.info(f"[POST EXECUTION] - Begin retrying failed tests.") 
        # Initilize xml object from own path or injected path
        self._generate_xml_object()
        
        # Get failed tests from original run
        logger.info(f"[POST EXECUTION] - Extracting failed tests from JUnit XML.")
        failed_tests = self._get_failed_tests(self._xml_object)
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
            temp_xml = JUnitXml.fromfile(self._temp_retry_path)
            new_failed = self._get_failed_tests(temp_xml)
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
                    # --> unstable
                    test["case"].append(Unstable())
                    logger.info(f"[POST EXECUTION] - Test {test['test_path']} marked as unstable.")
            logger.info(f"[POST EXECUTION] - Unstable test marking completed.")

            # Update failed_tests list for next iteration
            logger.info(f"[POST EXECUTION] - Rewriting the JUnit XML file.")
            self._xml_object.write(self._file_path)
            logger.info(f"[POST EXECUTION] - JUnit XML file updated.")
            failed_tests = [t for t in failed_tests if t["case"].child(Unstable) is None]
            if (len(failed_tests) == 0):
                logger.info(f"[POST EXECUTION] - All tests passed or marked unstable, ending retries.")
                break 
            logger.info(f"[POST EXECUTION] - {len(failed_tests)} tests remain failed.")

    def _get_failed_tests(self, xml: JUnitXml) -> list[dict[str, TestCase]]:
        """Get a list of failed tests from the JUnit XML.

        Args:
            xml (JUnitXML): The JUnit XML object 
                            that needs to be parsed for failed tests.

        Returns:
            list: A list of failed element test cases, each contains
                path to the test case and the corresponding TestCase object.
        """
        failed_tests = []
        for suite in xml:
            for case in suite:
                if case.is_failure or case.is_error:
                    failed_tests.append({
                        "test_path": f"{case.classname.replace('.', os.sep)}.py::{case.name}",
                        "case": case
                        })
        return failed_tests

    def _run_tests(self, failed_tests_paths: list[str]) -> None:
        """Rerun failed tests.

        Args:
            failed_tests_paths (list[str]): Paths to the failed test cases.
        """
        if not failed_tests_paths:
            logger.info(f"[POST EXECUTION] - No failed tests to rerun.")
            return
        logger.info(f"[POST EXECUTION] - Rerunning {len(failed_tests_paths)} failed tests.")
        cmd = ["pytest", f"--junitxml={self._temp_retry_path}"] + failed_tests_paths
        subprocess.run(cmd)
        
    def _parse_locust_csv(self) -> None:
        """Parse Locust stats and failures CSVs and assign self._csv_object as PerformanceResult."""
        
        if self._csv_object is not None:
            logger.info(f"[POST EXECUTION] - CSV already parsed, reusing PerformanceResult object.")
            return
        
        def to_int(value: str) -> int:
            try:
                return int(float(value))
            except (TypeError, ValueError):
                return 0

        def to_float(value: str) -> float:
            try:
                return float(value)
            except (TypeError, ValueError):
                return 0.0

        # Parse results stats
        metrics: list[PerformanceLineResult] = []
        if not self._file_path:
            logger.error("[POST EXECUTION] - Stats CSV path not provided.")
        else:
            logger.info(f"[POST EXECUTION] - Loading Locust stats CSV from {self._file_path}.")
            try:
                with open(self._file_path, "r", encoding="utf-8", newline="") as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        name = row.get("Name", "").strip()
                        if not name:
                            continue
                        metrics.append(PerformanceLineResult(
                            request_type=row.get("Type"),
                            name=name,
                            request_count=to_int(row.get("Request Count")),
                            failure_count=to_int(row.get("Failure Count")),
                            median_response_time=to_float(row.get("Median Response Time")),
                            average_response_time=to_float(row.get("Average Response Time")),
                            min_response_time=to_float(row.get("Min Response Time")),
                            max_response_time=to_float(row.get("Max Response Time")),
                            average_content_size=to_float(row.get("Average Content Size")),
                            requests_per_s=to_float(row.get("Requests/s")),
                            failures_per_s=to_float(row.get("Failures/s")),
                            p50=to_float(row.get("50%")),
                            p66=to_float(row.get("66%")),
                            p75=to_float(row.get("75%")),
                            p80=to_float(row.get("80%")),
                            p90=to_float(row.get("90%")),
                            p95=to_float(row.get("95%")),
                            p98=to_float(row.get("98%")),
                            p99=to_float(row.get("99%")),
                            p99_90=to_float(row.get("99.9%")),
                            p99_99=to_float(row.get("99.99%")),
                            p100=to_float(row.get("100%")),
                        ))
                logger.info(f"[POST EXECUTION] - Loaded {len(metrics)} rows from stats CSV.")
            except FileNotFoundError:
                logger.error(f"[POST EXECUTION] - Stats CSV not found at {self._file_path}.")
            except OSError as exc:
                logger.error(f"[POST EXECUTION] - Failed reading stats CSV: {exc}.")

        # Parse results failures
        failures: list[PerformanceFailureResult] = []
        if not self._secondary_path:
            logger.warning("[POST EXECUTION] - Failures CSV path not provided, skipping.")
        else:
            logger.info(f"[POST EXECUTION] - Loading Locust failures CSV from {self._secondary_path}.")
            try:
                with open(self._secondary_path, "r", encoding="utf-8", newline="") as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        failures.append(PerformanceFailureResult(
                            method=row.get("Method") or None,
                            name=row.get("Name") or None,
                            error=row.get("Error") or None,
                            occurrences=to_int(row.get("Occurrences")),
                            first_seen=row.get("First Seen") or None,
                            last_seen=row.get("Last Seen") or None,
                        ))
                logger.info(f"[POST EXECUTION] - Loaded {len(failures)} failure rows.")
            except FileNotFoundError:
                logger.error(f"[POST EXECUTION] - Failures CSV not found at {self._secondary_path}.")
            except OSError as exc:
                logger.error(f"[POST EXECUTION] - Failed reading failures CSV: {exc}.")

        self._csv_object = PerformanceResult(metrics=metrics, failures=failures)
        logger.info("[POST EXECUTION] - PerformanceResult assigned to self._csv_object.")

    def summary_xml(self) -> dict:
        """Generate a summary of test results from the stored JUnit XML object along with context.

        Returns:
            dict: Summary of test results.
        """
        self._generate_xml_object()
        logger.info(f"[POST EXECUTION] - Generating summary from JUnit XML.")
        
        # Fallback result in case of missing or invalid XML data
        summary_id = str(uuid4())
        empty = { "summary_id": summary_id, "type": self._context["type"], 
            "total": 0, "passed": 0, "failed": 0, "skipped": 0, "unstable": 0,
            "execution_time": 0.0, "pass_rate": 0.0, "mean_test_duration": 0.0 }
        
        if not self._xml_object:
            logger.info(f"[POST EXECUTION] - No valid JUnit XML found when generating summary, returning empty summary.")
            return empty
        
        summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "unstable": 0}
        test_execution_time = 0
        total_test_time = 0

        # Loop through test suites and cases
        # Because of pytest, there's only 1 suite
        for suite in self._xml_object:
            # Extract information of that suite
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

        result = {
            "summary_id": summary_id,
            "type": self._context["type"],
            "total": summary["total"],
            "passed": summary["passed"],
            "failed": summary["failed"],
            "skipped": summary["skipped"],
            "unstable": summary["unstable"],
            "execution_time": test_execution_time,
            "pass_rate": 
                summary["passed"] * 100 / summary["total"] if summary["total"] > 0 else 0,
            "mean_test_duration": 
                total_test_time / summary["total"] if summary["total"] > 0 else 0,
        }
        logger.info(f"[POST EXECUTION] - Summary generated: {result}")
        return result

    def summary_csv(self) -> dict:
        """Generate a summary from the Aggregated row of the parsed stats CSV.
        Returns:
            dict: Summary of the performance metrics.
        """
        self._parse_locust_csv()
        summary_id = str(uuid4())
        
        # Fallback result in case of missing or invalid CSV data
        empty = { "summary_id": summary_id, "total_requests": 0, "rps": 0.0, "mean_response": 0.0, "max_response": 0.0,
            "min_response": 0.0, "error_count": 0, "error_rate": 0.0, 
            "execution_time_s": self._context.get("execution_time_s", 0.0),
            "users": self._context.get("users", 0), "spawn_rate": self._context.get("spawn_rate", 0) }

        if not self._csv_object or not self._csv_object.metrics:
            logger.error("[POST EXECUTION] - No metrics available. Call _parse_locust_csv() first.")
            return empty

        # Extract the "Aggregated" row
        aggregated = next(
            (row for row in self._csv_object.metrics if row.name == "Aggregated"),
            None
        )
        if aggregated is None:
            logger.error("[POST EXECUTION] - Aggregated row not found in metrics.")
            return empty

        result = {
            "summary_id": summary_id,
            "total_requests": aggregated.request_count,
            "rps": aggregated.requests_per_s,
            "mean_response": aggregated.average_response_time,
            "max_response": aggregated.max_response_time,
            "min_response": aggregated.min_response_time,
            "error_count": aggregated.failure_count,
            "error_rate": 
                (aggregated.failure_count / aggregated.request_count * 100) if aggregated.request_count > 0 else 0.0,
            "execution_time_s": self._context.get("execution_time_s", 0.0),
            "users": self._context.get("users", 0),
            "spawn_rate": self._context.get("spawn_rate", 0),
        }
        logger.info(f"[POST EXECUTION] - Summary generated: {result}")
        return result
    
    def get_performance_metrics_csv(self) -> list[PerformanceLineResult]:
        """Get a list of performance metrics from the parsed stats CSV.

        Returns:
            list: A list of performance metric objects.
        """
        self._parse_locust_csv()
        if not self._csv_object or not self._csv_object.metrics:
            logger.error("[POST EXECUTION] - No metrics found.")
            return []
        return self._csv_object.metrics
    
    def get_failures_csv(self) -> list[PerformanceFailureResult]:
        """Get a list of failures from the parsed failures CSV.

        Returns:
            list: A list of failure objects.
        """
        self._parse_locust_csv()
        if not self._csv_object or not self._csv_object.failures:
            logger.error("[POST EXECUTION] - No failures found.")
            return []
        return self._csv_object.failures
    
    def get_failed_tests_report(self) -> list[dict]:
        """Get a list of failed tests with details from the JUnit XML,
        including results of each failed test (failure, error, or unstable)
        along with logs
        Returns:
            list[dict]: A list of dictionaries, each containing details of a failed test case and its results.
        """
        self._generate_xml_object()
        failed_tests = self._get_failed_tests(self._xml_object)
        
        result = []
        for test in failed_tests:
            test_case = test["case"]
            result.append({
                "suite": test_case.classname,
                "name": test_case.name,
                "status": "UNSTABLE" if test_case.child(Unstable) else "FAILURE",
                "exec_time": test_case.time,
                "results": [{ 
                        "tag": child._tag, 
                        "message": child.message, 
                        "text": child.text
                    } for child in test_case]                
            })
        return result

    @staticmethod
    def send_records(records: list[str], host: str, token: str, database: str) -> Response:
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
        