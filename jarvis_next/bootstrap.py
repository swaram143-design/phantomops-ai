from .adapters import WorkerRegistry
from .phantomops_adapter import PhantomOpsAdapter
from .external_adapters import OpenClawAdapter,OpenHandsAdapter,BrowserWorker
from .nexus_adapter import NexusLegacyAdapter

def build_registry():
    r=WorkerRegistry()
    for w in (
        PhantomOpsAdapter(),
        NexusLegacyAdapter(),
        BrowserWorker(),
        OpenClawAdapter(),
        OpenHandsAdapter(),
    ):
        r.register(w)
    return r
