"""Integration-test placeholder (IQ #490 / #492).

The CI `pytest tests/integration/ -v` step predates any integration suite, so the
job errored on a missing directory. This stub keeps the integration job green
until real cross-component tests land — replace it with genuine integration
coverage as the azimuth surface grows (API <-> storage <-> CLI round-trips).
"""


def test_integration_placeholder():
    """Trivial pass so `pytest tests/integration/` collects at least one test."""
    assert True
