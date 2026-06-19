class BuildSummary:
    def __init__(self, build_number, build_url, branch, author, host, run_type):
        self.build_number = build_number
        self.build_url = build_url
        self.branch = branch
        self.author = author
        self.host = host
        self.run_type = run_type
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.unstable = 0
        self.pass_rate = 0.0
        self.execution_time = 0

    def update(self, total=0, passed=0, failed=0, skipped=0, unstable=0, execution_time=0):
        self.total += total
        self.passed += passed
        self.failed += failed
        self.skipped += skipped
        self.unstable += unstable
        if self.total > 0:
            self.pass_rate = (self.passed / self.total) * 100
        else:
            self.pass_rate = 0.0
        self.execution_time += execution_time
    
    def to_dict(self):
        return {
            "build_number": self.build_number,
            "build_url": self.build_url,
            "branch": self.branch,
            "author": self.author,
            "host": self.host,
            "run_type": self.run_type,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "unstable": self.unstable,
            "pass_rate": self.pass_rate,
            "execution_time": self.execution_time
        }