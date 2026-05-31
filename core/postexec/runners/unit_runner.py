from core.postexec import PostExec
from core.utils.logs import get_logger
logger = get_logger()

def main(junit_path: str) -> tuple[dict, list[dict]]:
    logger.info("[POST EXECUTION] - Starting unit post-execution processing.")
    postexec = PostExec(path=junit_path, context={"type": "unit"})
    logger.info("[POST EXECUTION] - Generating unit test summary.")
    summary = postexec.summary_xml()
    logger.info("[POST EXECUTION] - Extracting failed unit tests details.")
    failed_tests = postexec.get_failed_tests_report()
    logger.info("[POST EXECUTION] - Unit post-execution processing completed.")
    return summary, failed_tests
