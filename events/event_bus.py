from collections import defaultdict
import asyncio


class EventBus:

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, callback):

        self.subscribers[event_type].append(callback)

    async def publish(self, event_type, data=None):

        if event_type not in self.subscribers:
            return

        tasks = []

        for callback in self.subscribers[event_type]:

            tasks.append(
                asyncio.create_task(
                    callback(data)
                )
            )

        await asyncio.gather(*tasks)


event_bus = EventBus()