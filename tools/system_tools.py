import platform
import psutil
import socket
from datetime import datetime


class SystemTools:

    async def get_system_info(self):

        return {
            "os": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_usage":
                psutil.cpu_percent(),
            "memory_usage":
                psutil.virtual_memory().percent,
            "hostname":
                socket.gethostname(),
            "timestamp":
                str(datetime.now())
        }


system_tools = SystemTools()