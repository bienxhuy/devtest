from junitparser import JUnitXml, Element, Failure, Error, Skipped 
from uuid import uuid4
from datetime import datetime, timezone


class Unstable(Element):
    _tag = "unstable"
    

def summary(path, context):
    """Generate a summary of test results.

    Loop through the junit xml file produced by pytest,
    summarize the report.

    Args:
        path (_type_): File path of the junit xml file
        context (_type_): Context information for the test execution
    """
    xml = JUnitXml.fromfile(path)
    run_id = str(uuid4())
    summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "unstable": 0}
    test_execution_time = 0
    host_name = "<HOST_NAME>"
    total_test_time = 0

    # Loop through test suites and cases
    # Because of pytest, there's only 1 suite
    for suite in xml:
        # Extract information of that suite
        timestamp = datetime.fromisoformat(suite.timestamp) \
                            .replace(tzinfo=timezone.utc) \
                            .timestamp()
        host_name = suite.hostname
        test_execution_time = suite.time or 0

        for case in suite:
            status = "passed"
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
        "host_name": host_name
    }
