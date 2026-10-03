from .adapters import WorkerRegistry
from .phantomops_adapter import PhantomOpsAdapter
from .external_adapters import OpenClawAdapter,OpenHandsAdapter

def build_registry():
 r=WorkerRegistry();r.register(PhantomOpsAdapter())
 for w in (OpenClawAdapter(),OpenHandsAdapter()):r.register(w)
 return r
