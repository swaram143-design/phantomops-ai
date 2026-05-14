from core.task_queue import *

from core.autonomous_loop import *

# =====================================================
# ADD TASKS
# =====================================================

add_task(
    "lead_generation"
)

add_task(
    "product_launch"
)

# =====================================================
# START AUTONOMOUS LOOP
# =====================================================

autonomous_loop()