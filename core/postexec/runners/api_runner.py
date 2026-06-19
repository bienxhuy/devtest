from core.postexec import PostExec
from core.utils.logs import get_logger
logger = get_logger()

def main(junit_path: str) -> tuple[dict, list[dict]]:
    logger.info("[POST EXECUTION] - Starting API post-execution processing.")
    postexec = PostExec(path=junit_path, context={"type": "api"})
    logger.info("[POST EXECUTION] - Retrying failed API tests.")
    postexec.retry_fails()
    logger.info("[POST EXECUTION] - Generating API test summary.")
    summary = postexec.summary_xml()
    logger.info("[POST EXECUTION] - Extracting failed API tests details.")
    failed_tests = postexec.get_failed_tests_report()
    logger.info("[POST EXECUTION] - API post-execution processing completed.")
    return summary, failed_tests
