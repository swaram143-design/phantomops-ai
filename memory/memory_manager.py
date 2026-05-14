import json
import os

from datetime import datetime


class MemoryManager:

    def __init__(self):

        self.memory_path = (
            "memory/system_memory.json"
        )

        self.memory = {
            "sessions": [],
            "tasks": [],
            "agents": [],
            "events": [],
            "results": [],
            "system_state": {}
        }

        self.load_memory()

    def load_memory(self):

        if os.path.exists(
            self.memory_path
        ):

            try:

                with open(
                    self.memory_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.memory = json.load(
                        file
                    )

            except Exception as e:

                print(
                    f"[Memory] "
                    f"Load error: {e}"
                )

    def save_memory(self):

        with open(
            self.memory_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.memory,
                file,
                indent=4
            )

    def add_task(self, task):

        self.memory["tasks"].append(
            {
                "timestamp":
                    str(datetime.now()),
                "task": task
            }
        )

        self.save_memory()

    def add_event(self, event):

        self.memory["events"].append(
            {
                "timestamp":
                    str(datetime.now()),
                "event": event
            }
        )

        self.save_memory()

    def add_result(self, result):

        self.memory["results"].append(
            {
                "timestamp":
                    str(datetime.now()),
                "result": result
            }
        )

        self.save_memory()

    def update_system_state(
        self,
        key,
        value
    ):

        self.memory[
            "system_state"
        ][key] = value

        self.save_memory()


memory_manager = MemoryManager()