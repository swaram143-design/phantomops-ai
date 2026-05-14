import os
import datetime

# =====================================================
# LOG FILE
# =====================================================

LOG_FILE = "database/activity_log.txt"

# =====================================================
# INITIALIZE LOG
# =====================================================

def initialize_log():

    if not os.path.exists("database"):

        os.makedirs("database")

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "PHANTOMOPS ACTIVITY LOG\n\n"
            )

# =====================================================
# WRITE LOG
# =====================================================

def write_log(message):

    initialize_log()

    timestamp = datetime.datetime.now().strftime(
        "%H:%M:%S"
    )

    entry = f"[{timestamp}] {message}\n"

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(entry)

    print(entry)