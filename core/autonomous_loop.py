import time

from core.task_queue import *

# =====================================================
# AUTONOMOUS LOOP
# =====================================================

def autonomous_loop():

    print("\n================================")
    print("PHANTOMOPS AUTONOMOUS LOOP")
    print("================================\n")

    print("System is now monitoring tasks...\n")

    # =============================================
    # CONTINUOUS LOOP
    # =============================================

    while True:

        # =========================================
        # CHECK TASKS
        # =========================================

        if len(task_queue) > 0:

            print("\nTasks detected.")

            process_queue()

        else:

            print(
                "No pending tasks..."
            )

        # =========================================
        # WAIT
        # =========================================

        time.sleep(10)