from core.autonomous_loop import *

from core.task_queue import *

from core.logger import *

# =====================================================
# STARTUP LOG
# =====================================================

write_log(
    "PHANTOMOPS BACKGROUND WORKER STARTED"
)

# =====================================================
# INITIAL TASKS
# =====================================================

add_task(
    "lead_generation"
)

add_task(
    "product_launch"
)

# =====================================================
# START AUTONOMOUS SYSTEM
# =====================================================

autonomous_loop()