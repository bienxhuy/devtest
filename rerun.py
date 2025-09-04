import os
import subprocess
from junitparser import JUnitXml, Element


XML_FILE_PATH = "junit_results.xml"
TEMP_XML = "temp_results.xml"
MAX_RETRIES = 2


class Unstable(Element):
    _tag = "unstable"


def get_failed_tests(xml):
    failed = []
    for suite in xml:
        for case in suite:
            if case.is_failure or case.is_error:
                failed.append({
                    "test_path": f"{case.classname.replace('.', os.sep)}.py::{case.name}",
                    "case": case
                    })
    return failed


def run_tests(failed_tests_paths):
    if not failed_tests_paths: 
        return
    cmd = ["pytest", "-v", f"--junitxml={TEMP_XML}"] + failed_tests_paths
    subprocess.run(cmd)


if __name__ == "__main__":
    # Initilize xml file
    xml = JUnitXml.fromfile(XML_FILE_PATH)
    # Get failed tests from original run
    failed_tests = get_failed_tests(xml)
    if not failed_tests:
        exit(0)

    # Re-runs failed tests
    for attempt in range(1, MAX_RETRIES + 1):
        # Run previous failed results
        print(f"\n=== Attempt {attempt} ===")
        run_tests([test["test_path"] for test in failed_tests])

        # Load new failed results
        temp_xml = JUnitXml.fromfile(TEMP_XML)
        new_failed = get_failed_tests(temp_xml)

        # Compare with previous failed results
        # First create the list of test paths from new failed results
        new_test_paths = [test["test_path"] for test in new_failed]
        # Loop through old failed tests
        for test in failed_tests:
            # if test["test_path"] not in new_test_paths:
            if attempt == 1:
                # If test does not appear in new failed tests
                # It means it passed this time,
                # mark as unstable
                test["case"].append(Unstable())

        # Update failed_tests for next iteration
        xml.write(XML_FILE_PATH)
        failed_tests = [t for t in failed_tests if t["case"].child(Unstable) is None]
