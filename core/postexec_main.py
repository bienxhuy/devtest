from uuid import uuid4
from dotenv import load_dotenv
import os
from core.utils.logs import get_logger
from core.postexec import Runners, LineProtocolFormatter, PostExec, BuildSummary


# Get a logger instance for logging within the postexec
logger = get_logger()
# Load configuration
load_dotenv()

RUN_TYPE = os.getenv("RUN_TYPE", "nightly")

UNIT_JUNIT_PATH = os.getenv("UNIT_JUNIT_PATH", "reports/jest-junit.xml")
API_JUNIT_PATH = os.getenv("API_JUNIT_PATH", "reports/api-junit.xml")
E2E_JUNIT_PATH = os.getenv("E2E_JUNIT_PATH", "reports/e2e-junit.xml")
PERF_CSV_STATS_PATH = os.getenv("PERF_CSV_STATS_PATH", "reports/performance/results_stats.csv")
PERF_CSV_FAILURES_PATH = os.getenv("PERF_CSV_FAILURES_PATH", "reports/performance/results_failures.csv")

TIMESTAMP = int(os.getenv("TIMESTAMP"))
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local_run")
BUILD_URL = os.getenv("BUILD_URL", "http://localhost:8080/job/devtest")
BRANCH = os.getenv("BRANCH")
AUTHOR = os.getenv("AUTHOR", "none")
HOST = os.getenv("HOST", "none")

PERFORMANCE_RUN_TIME = os.getenv("PERFORMANCE_RUN_TIME")
PERFORMANCE_USERS = int(os.getenv("PERFORMANCE_USERS"))
PERFORMANCE_SPAWN_RATE = int(os.getenv("PERFORMANCE_SPAWN_RATE", "0"))

BUILD_SUMMARY_MEASUREMENT = "build_summaries"
TESTS_SUMMARY_MEASUREMENT = "xml_test_summaries"
FAILED_TESTS_MEASUREMENT = "failed_tests"
FAILED_TESTS_RESULTS_MEASUREMENT = "results"
PERFORMANCE_SUMMARY_MEASUREMENT = "performance_summaries"
PERFORMANCE_METRICS_MEASUREMENT = "performance_metrics"
PERFORMANCE_FAILURE_MEASUREMENT = "performance_failures"
FAILED_TESTS_MEASUREMENT = "failed_tests"

INFLUX_HOST = os.getenv("INFLUX_HOST")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE")


if __name__ == "__main__":
    logger.info("[POST EXECUTION] - Starting post-execution processing.")
    formatter = LineProtocolFormatter(run_id=str(uuid4()), timestamp=TIMESTAMP)
    records = []
    build_summary = BuildSummary(
        build_number=BUILD_NUMBER,
        build_url=BUILD_URL,
        branch=BRANCH,
        author=AUTHOR,
        host=HOST,
        run_type=RUN_TYPE,
    )
    
    # UNIT TEST PHASE
    logger.info("[POST EXECUTION] - Processing unit test results.")
    unit_summary, unit_failed_tests = Runners.run_unit(UNIT_JUNIT_PATH)
    unit_summary_record = formatter.format_junit_summary(
        summary=unit_summary, measurement=TESTS_SUMMARY_MEASUREMENT)
    unit_failed_tests_records = formatter.format_failed_tests_xml(
        data=unit_failed_tests,
        summary_id=unit_summary["summary_id"],
        failed_tests_measurement=FAILED_TESTS_MEASUREMENT,
        results_measurement=FAILED_TESTS_RESULTS_MEASUREMENT)
    # Update data for build summary and aggregate records
    records.append(unit_summary_record)
    records.extend(unit_failed_tests_records)
    build_summary.update(
        total=unit_summary["total"],
        passed=unit_summary["passed"],
        failed=unit_summary["failed"],
        skipped=unit_summary["skipped"],
        unstable=unit_summary["unstable"],
        execution_time=unit_summary["execution_time"]
    )

    # API TEST PHASE
    logger.info("[POST EXECUTION] - Processing API test results.")
    api_summary, api_failed_tests = Runners.run_api(API_JUNIT_PATH)
    api_summary_record = formatter.format_junit_summary(
        summary=api_summary, measurement=TESTS_SUMMARY_MEASUREMENT)
    api_failed_tests_records = formatter.format_failed_tests_xml(
        data=api_failed_tests,
        summary_id=api_summary["summary_id"],
        failed_tests_measurement=FAILED_TESTS_MEASUREMENT,
        results_measurement=FAILED_TESTS_RESULTS_MEASUREMENT)
    # Update data for build summary and aggregate records
    records.append(api_summary_record)
    records.extend(api_failed_tests_records)
    build_summary.update(
        total=api_summary["total"],
        passed=api_summary["passed"],
        failed=api_summary["failed"],
        skipped=api_summary["skipped"],
        unstable=api_summary["unstable"],
        execution_time=api_summary["execution_time"]
    )
    
    # IF RUN_TYPE IS NOT PUSH, IT MEANS THIS IS A NIGHTLY OR MANUAL RUN.
    # PROCESS E2E AND PERFORMANCE TESTS
    if (RUN_TYPE != "push"):
        logger.info("[POST EXECUTION] - RUN_TYPE is not 'push'; processing E2E and performance tests.")
        
        # E2E TEST PHASE (if needed, can be added similarly to unit and API)
        logger.info("[POST EXECUTION] - Processing E2E test results.")
        e2e_summary, e2e_failed_tests = Runners.run_e2e(E2E_JUNIT_PATH)
        e2e_summary_record = formatter.format_junit_summary(
            summary=e2e_summary, measurement=TESTS_SUMMARY_MEASUREMENT)
        e2e_failed_tests_records = formatter.format_failed_tests_xml(
            data=e2e_failed_tests,
            summary_id=e2e_summary["summary_id"],
            failed_tests_measurement=FAILED_TESTS_MEASUREMENT,
            results_measurement=FAILED_TESTS_RESULTS_MEASUREMENT)
        # Update data for build summary and aggregate records
        records.append(e2e_summary_record)
        records.extend(e2e_failed_tests_records)
        build_summary.update(
            total=e2e_summary["total"],
            passed=e2e_summary["passed"],
            failed=e2e_summary["failed"],
            skipped=e2e_summary["skipped"],
            unstable=e2e_summary["unstable"],
            execution_time=e2e_summary["execution_time"]
        )

        # PERFORMANCE TEST PHASE
        logger.info("[POST EXECUTION] - Processing performance test results.")
        perf_context = {
            "execution_time_s": formatter.locust_run_time_parser(PERFORMANCE_RUN_TIME),
            "users": int(PERFORMANCE_USERS),
            "spawn_rate": int(PERFORMANCE_SPAWN_RATE) }
        perf_summary, perf_details_metrics, perf_failures = Runners.run_performance(
            csv_stats_path=PERF_CSV_STATS_PATH, 
            csv_failures_path=PERF_CSV_FAILURES_PATH, 
            context=perf_context)
        perf_summary_record = formatter.format_performance_summary(
            summary=perf_summary, measurement=PERFORMANCE_SUMMARY_MEASUREMENT)
        perf_metrics_records = formatter.format_performance_metrics(
            metrics=perf_details_metrics, summary_id=perf_summary["summary_id"], measurement=PERFORMANCE_METRICS_MEASUREMENT)
        perf_failures_records = formatter.format_performance_failures(
            failures=perf_failures, summary_id=perf_summary["summary_id"], measurement=PERFORMANCE_FAILURE_MEASUREMENT)
        # Update data for build summary and aggregate records
        records.append(perf_summary_record)
        records.extend(perf_metrics_records)
        records.extend(perf_failures_records)
        build_summary.update(execution_time=perf_summary["execution_time_s"])

    # BUILD SUMMARY - AGGREGATE ALL DATA
    build_summary = build_summary.to_dict()
    logger.info(f"[POST EXECUTION] - Build summary: {build_summary}")
    build_summ_record = formatter.format_build_summary(summary=build_summary, measurement=BUILD_SUMMARY_MEASUREMENT)
    records.append(build_summ_record)

    # AGGREGATE ALL RECORDS AND SEND TO INFLUXDB
    logger.info(f"[POST EXECUTION] - Sending {len(records)} records to InfluxDB.")
    response = PostExec.send_records(records=records, host=INFLUX_HOST, token=INFLUX_TOKEN, database=INFLUX_DATABASE)
    logger.info(f"[POST EXECUTION] - InfluxDB response: {response.status_code}")
    logger.info("[POST EXECUTION] - Post-execution processing completed.")
