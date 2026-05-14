import time

from core.workflow_engine import *

# =====================================================
# TASK QUEUE
# =====================================================

task_queue = []

# =====================================================
# ADD TASK
# =====================================================

def add_task(workflow_name):

    task_queue.append(workflow_name)

    print(
        f"\nTask added: {workflow_name}"
    )

# =====================================================
# SHOW QUEUE
# =====================================================

def show_queue():

    print("\n========== TASK QUEUE ==========\n")

    if len(task_queue) == 0:

        print("Queue is empty.\n")

        return

    for index, task in enumerate(task_queue, start=1):

        print(f"{index}. {task}")

# =====================================================
# PROCESS QUEUE
# =====================================================

def process_queue():

    print("\n================================")
    print("STARTING TASK QUEUE")
    print("================================\n")

    while len(task_queue) > 0:

        workflow = task_queue.pop(0)

        print(
            f"\nProcessing: {workflow}"
        )

        run_workflow(workflow)

        time.sleep(1)

    print("\n================================")
    print("ALL TASKS COMPLETED")
    print("================================\n")