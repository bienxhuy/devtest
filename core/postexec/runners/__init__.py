from junitparser import TestCase
from core.postexec.performance_result import PerformanceFailureResult, PerformanceLineResult

from .unit_runner import (
  main as unit_main
)

from .api_runner import (
  main as api_main
)

from .e2e_runner import (
  main as e2e_main
)

from .perf_runner import (
  main as perf_main
)

class Runners:
    @staticmethod
    def run_unit(junit_path: str) -> tuple[dict, list[dict]]:
        """ Return a summary of unit test results and a list of failed tests with their results details
        Returns:
            tuple[dict, list[dict]]:
                - dict: A summary of unit test results (total, passed, failed, etc.)
                - list[dict]: A list of dictionaries, each containing details of a failed test case and its results.
        """
        return unit_main(junit_path=junit_path)
    
    @staticmethod
    def run_api(junit_path: str) -> tuple[dict, list[dict]]:
        """ Retry failed tests then return a summary of API test results and a list of failed tests with their results details
        Returns:
            tuple[dict, list[dict]]:
                - dict: A summary of API test results (total, passed, failed, etc.)
                - list[dict]: A list of dictionaries, each containing details of a failed test case and its results.
        """
        return api_main(junit_path=junit_path)
    
    @staticmethod
    def run_e2e(junit_path: str) -> tuple[dict, list[dict]]:
        """ Retry failed tests then return a summary of E2E test results and a list of failed tests with their results details
        Returns:
            tuple[dict, list[dict]]:
                - dict: A summary of E2E test results (total, passed, failed, etc.)
                - list[dict]: A list of dictionaries, each containing details of a failed test case and its results.
        """
        return e2e_main(junit_path=junit_path)

    @staticmethod
    def run_performance(csv_stats_path: str, csv_failures_path: str, context: dict) -> tuple[dict, list[PerformanceLineResult], list[PerformanceFailureResult]]:
        """ Return a summary of performance test results and lists of performance metrics and failures
        Returns:
            tuple[dict, list[PerformanceLineResult], list[PerformanceFailureResult]]:
                - dict: A summary of performance test results (total, error_count, etc.)
                - list[PerformanceLineResult]: A list of performance metric objects.
                - list[PerformanceFailureResult]: A list of failure objects.
        """
        return perf_main(csv_stats_path=csv_stats_path, csv_failures_path=csv_failures_path, context=context)

__all__ = [
    "Runners"
]