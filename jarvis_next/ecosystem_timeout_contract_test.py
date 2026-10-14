"""Contract for external command timeout safety."""

from .adapters import WorkerResult
from .ecosystem_adapters import _ambiguous_command_timeout


def test_command_timeout_is_uncertain_and_non_retryable():
    result = _ambiguous_command_timeout(12)
    assert isinstance(result, WorkerResult)
    assert not result.ok
    assert result.side_effect_uncertain is True
    assert result.retryable is False


if __name__ == "__main__":
    test_command_timeout_is_uncertain_and_non_retryable()
    print("ECOSYSTEM COMMAND TIMEOUT CONTRACT OK")
