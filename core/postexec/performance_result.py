from dataclasses import dataclass


@dataclass
class PerformanceLineResult:
	"""Container for a single Locust performance summary line."""
	request_type: str | None = None
	name: str | None = None
	request_count: int = 0
	failure_count: int = 0
	median_response_time: float = 0.0
	average_response_time: float = 0.0
	min_response_time: float = 0.0
	max_response_time: float = 0.0
	average_content_size: float = 0.0
	requests_per_s: float = 0.0
	failures_per_s: float = 0.0
	p50: float = 0.0
	p66: float = 0.0
	p75: float = 0.0
	p80: float = 0.0
	p90: float = 0.0
	p95: float = 0.0
	p98: float = 0.0
	p99: float = 0.0
	p99_90: float = 0.0
	p99_99: float = 0.0
	p100: float = 0.0


@dataclass
class PerformanceFailureResult:
  """Container for a single Locust performance failure summary line."""
  method: str | None = None
  name: str | None = None
  error: str | None = None
  occurrences: int = 0
  first_seen: str | None = None
  last_seen: str | None = None


@dataclass
class PerformanceResult:
  """Container for the overall Locust performance summary."""
  metrics: list[PerformanceLineResult]
  failures: list[PerformanceFailureResult]
