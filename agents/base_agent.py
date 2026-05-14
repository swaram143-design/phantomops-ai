from abc import ABC, abstractmethod
from datetime import datetime

from events.event_bus import event_bus
from events.event_types import (
    AGENT_STARTED,
    AGENT_FINISHED,
    TASK_FAILED
)


class BaseAgent(ABC):

    def __init__(self, name):

        self.name = name
        self.status = "idle"
        self.created_at = datetime.now()
        self.last_run = None

    async def run(self, task):

        self.status = "running"
        self.last_run = datetime.now()

        await event_bus.publish(
            AGENT_STARTED,
            {
                "agent": self.name,
                "task": task
            }
        )

        try:

            result = await self.execute(task)

            self.status = "idle"

            await event_bus.publish(
                AGENT_FINISHED,
                {
                    "agent": self.name,
                    "result": result
                }
            )

            return result

        except Exception as e:

            self.status = "error"

            await event_bus.publish(
                TASK_FAILED,
                {
                    "agent": self.name,
                    "error": str(e)
                }
            )

            return {
                "success": False,
                "error": str(e)
            }

    @abstractmethod
    async def execute(self, task):
        pass