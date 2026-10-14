from .adapters import Worker, WorkerRegistry


class SecretFailingWorker(Worker):
    name = "secret-worker"

    def health(self):
        raise RuntimeError("Authorization: Bearer SUPER-SECRET-TOKEN https://secret.example.test")


def main():
    registry = WorkerRegistry()
    registry.register(SecretFailingWorker())

    result = registry.health()["secret-worker"]

    assert result["ok"] is False
    assert result["error"] == "RuntimeError: worker health check failed"
    assert "SUPER-SECRET-TOKEN" not in str(result)
    assert "secret.example.test" not in str(result)

    print("worker health exception redaction contract: ok")


if __name__ == "__main__":
    main()
