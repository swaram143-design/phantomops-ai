from dataclasses import dataclass

@dataclass
class WorkerResult:
    ok: bool
    data: object = None
    error: str = None
    retryable: bool = False

class Worker:
    name = "worker"
    capabilities = set()

    def score(self, task):
        return 0

    async def run(self, task):
        raise NotImplementedError

class WorkerRegistry:
    def __init__(self):
        self.workers = {}

    def register(self, worker):
        self.workers[worker.name] = worker

    def find(self, capability):
        return [w for w in self.workers.values() if capability in w.capabilities]

    def ranked(self, capability, task=None):
        task = task or {}
        return sorted(self.find(capability), key=lambda w: (w.score(task), w.name), reverse=True)

    def choose(self, capability, task=None):
        candidates = self.ranked(capability, task)
        return candidates[0] if candidates else None
