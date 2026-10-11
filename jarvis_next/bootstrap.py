import os

from .adapters import WorkerRegistry
from .phantomops_adapter import PhantomOpsAdapter
from .external_adapters import OpenClawAdapter,OpenHandsAdapter,BrowserWorker
from .nexus_adapter import NexusLegacyAdapter
from .ecosystem_adapters import RufloAdapter,PaperclipAdapter,AIReceptionistAdapter,N8NAdapter,TwentyAdapter

def build_registry():
    r=WorkerRegistry()
    workers=[
        PhantomOpsAdapter(),
        BrowserWorker(),
        OpenClawAdapter(),
        OpenHandsAdapter(),
        RufloAdapter(),
        PaperclipAdapter(),
        AIReceptionistAdapter(),
        N8NAdapter(),
        TwentyAdapter(),
    ]
    if os.getenv("NEXUS_ROOT"):
        workers.append(NexusLegacyAdapter())
    for w in workers:
        r.register(w)
    return r
