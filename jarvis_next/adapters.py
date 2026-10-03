from dataclasses import dataclass
@dataclass
class WorkerResult: ok:bool; data:object=None; error:str=None
class Worker:
 name="worker";capabilities=set()
 async def run(self,task):raise NotImplementedError
class WorkerRegistry:
 def __init__(self):self.workers={}
 def register(self,w):self.workers[w.name]=w
 def find(self,cap):return [w for w in self.workers.values() if cap in w.capabilities]
