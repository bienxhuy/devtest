from core.postexec import PostExec
from core.postexec.performance_result import PerformanceFailureResult, PerformanceLineResult
from core.utils.logs import get_logger
logger = get_logger()

def main(csv_stats_path: str, csv_failures_path: str, context: dict) -> tuple[dict, list[PerformanceLineResult], list[PerformanceFailureResult]]:
    logger.info("[POST EXECUTION] - Starting Performance post-execution processing.")
    context["type"] = "performance"
    postexec = PostExec(path=csv_stats_path, context=context, secondary_path=csv_failures_path)
    logger.info("[POST EXECUTION] - Generating Performance test summary.")
    summary = postexec.summary_csv()
    logger.info("[POST EXECUTION] - Extracting failed Performance tests details.")
    performance_stats_metrics = postexec.get_performance_metrics_csv()
    logger.info("[POST EXECUTION] - Extracting performance failures details.")
    performance_failures_metrics = postexec.get_failures_csv()
    logger.info("[POST EXECUTION] - Performance post-execution processing completed.")
    return summary, performance_stats_metrics, performance_failures_metrics
