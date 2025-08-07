import subprocess
import os


# Singleton class to hold test context information
# This class is used to store information about the test environment
class TestContext:
    commit = os.getenv("GIT_COMMIT") or subprocess.getoutput("git rev-parse HEAD")
    branch = os.getenv("GIT_BRANCH") or subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
    env = os.getenv("ENVIRONMENT", "local")
    test_suite = None
    test_case = None

context = TestContext()
