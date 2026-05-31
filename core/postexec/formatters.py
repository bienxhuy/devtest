from core.postexec.performance_result import PerformanceFailureResult, PerformanceLineResult
from uuid import uuid4


class LineProtocolFormatter:
    """Format post-execution results to InfluxDB line protocol."""

    def __init__(self, run_id: str, timestamp: int) -> None:
        self.run_id = self._escape_tag_value(run_id)
        self.timestamp = timestamp

    @staticmethod
    def _escape_tag_value(value: object) -> str:
        if value is None:
            value = ""
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace(" ", "\\ ")
            .replace(",", "\\,")
            .replace("=", "\\=")
        )

    @staticmethod
    def _escape_field_string(value: object) -> str:
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
        )

    def format_performance_metrics(
        self, 
        metrics: list[PerformanceLineResult], 
        summary_id: str,
        measurement: str) -> list[str]:
        lines = []
        for metric in metrics:
            request_method = metric.request_type if metric.request_type else "AGGREGATED"
            tags = (
                f"summary_id={summary_id},"
                f"name={self._escape_tag_value(metric.name)},"
                f"request_method={self._escape_tag_value(request_method)}"
            )
            fields = (
                f"request_count={metric.request_count},"
                f"failure_count={metric.failure_count},"
                f"median_response_time={metric.median_response_time},"
                f"average_response_time={metric.average_response_time},"
                f"min_response_time={metric.min_response_time},"
                f"max_response_time={metric.max_response_time},"
                f"average_content_size={metric.average_content_size},"
                f"requests_per_s={metric.requests_per_s},"
                f"failures_per_s={metric.failures_per_s},"
                f"p50={metric.p50},"
                f"p66={metric.p66},"
                f"p75={metric.p75},"
                f"p80={metric.p80},"
                f"p90={metric.p90},"
                f"p95={metric.p95},"
                f"p98={metric.p98},"
                f"p99={metric.p99},"
                f"p99_90={metric.p99_90},"
                f"p99_99={metric.p99_99},"
                f"p100={metric.p100}"
            )
            line = f"{measurement},{tags} {fields} {self.timestamp}"
            lines.append(line)
        return lines

    def format_performance_failures(
        self, 
        failures: list[PerformanceFailureResult], 
        summary_id: str,
        measurement: str) -> list[str]:
        lines = []
        for failure in failures:
            tags = (
                f"summary_id={summary_id},"
                f"method={self._escape_tag_value(failure.method)},"
                f"name={self._escape_tag_value(failure.name)}"
            )
            fields = (
                f"error=\"{self._escape_field_string(failure.error)}\","
                f"occurrences={failure.occurrences},"
                f"first_seen=\"{self._escape_field_string(failure.first_seen)}\","
                f"last_seen=\"{self._escape_field_string(failure.last_seen)}\""
            )
            line = f"{measurement},{tags} {fields} {self.timestamp}"
            lines.append(line)
        return lines
    
    def format_failed_tests_xml(
        self, 
        data: list[dict], 
        summary_id: str,
        failed_tests_measurement: str, 
        results_measurement: str, ) -> list[str]:
        lines = []
        for testcase in data:
            test_id = str(uuid4())
            case_tags = (
                f"summary_id={summary_id},"
                f"suite={self._escape_tag_value(testcase["suite"])},"
                f"test_id={test_id},"
                f"test_name={self._escape_tag_value(testcase["name"])}"
            )
            case_fields = (
                f"status=\"{self._escape_field_string(testcase["status"])}\","
                f"exec_time={testcase["exec_time"]}"
            )
            # For failed_tests table
            lines.append(
                f"{failed_tests_measurement},{case_tags} {case_fields} {self.timestamp}"
            )

            # Each failed test may have multiple results,
            # so we create a separate line for each result, 
            # linking back to the test case via test_id
            # This will be stored in results table
            for result in testcase["results"]:
                result_tags = (
                    f"test_id={test_id},"
                    f"tag={self._escape_tag_value(result["tag"])}"
                )
                result_fields = (
                    f"message=\"{self._escape_field_string(result["message"])}\","
                    f"logs=\"{self._escape_field_string(result["text"])}\""
                )
                lines.append(
                    f"{results_measurement},{result_tags} {result_fields} {self.timestamp}"
                )

        return lines
    
    def format_build_summary(self, summary: dict, measurement: str) -> str:
        tags = (
            f"run_id={self.run_id},"
            f"build_number={summary['build_number']},"
            f"build_url={self._escape_tag_value(summary['build_url'])},"
            f"branch={self._escape_tag_value(summary['branch'])},"
            f"author={self._escape_tag_value(summary['author'])},"
            f"host={self._escape_tag_value(summary['host'])},"
            f"run_type={summary['run_type']}"
        )
        fields = (
            f"total={summary['total']},"
            f"passed={summary['passed']},"
            f"failed={summary['failed']},"
            f"skipped={summary['skipped']},"
            f"unstable={summary['unstable']},"
            f"pass_rate={summary['pass_rate']},"
            f"execution_time={summary['execution_time']}"
        )
        return f"{measurement},{tags} {fields} {self.timestamp}"

    def format_performance_summary(self, summary: dict, measurement: str) -> str:
        tags = (
            f"run_id={self.run_id},"
            f"summary_id={summary["summary_id"]}"
        )
        fields = (
            f"total_requests={summary['total_requests']},"
            f"rps={summary['rps']},"
            f"mean_latency_ms={summary['mean_response']},"
            f"max_response={summary['max_response']},"
            f"min_response={summary['min_response']},"
            f"error_count={summary['error_count']},"
            f"error_rate={summary['error_rate']},"
            f"execution_time_s={summary['execution_time_s']},"
            f"users={summary['users']},"
            f"spawn_rate={summary['spawn_rate']}"
        )
        return f"{measurement},{tags} {fields} {self.timestamp}"

    def format_junit_summary(self, summary: dict, measurement: str) -> str:
        tags = (
            f"run_id={self.run_id},"
            f"summary_id={summary["summary_id"]},"
            f"type={summary["type"]}"
        )
        fields = (
            f"total={summary['total']},"
            f"passed={summary['passed']},"
            f"failed={summary['failed']},"
            f"skipped={summary['skipped']},"
            f"unstable={summary['unstable']},"
            f"pass_rate={summary['pass_rate']},"
            f"execution_time={summary['execution_time']},"
            f"mean_test_duration={summary['mean_test_duration']}"
        )
        return f"{measurement},{tags} {fields} {self.timestamp}"
