from memory.memory_manager import *

# =====================================================
# STORE MEMORY
# =====================================================

remember(
    "user_name",
    "Doctor Ramesh"
)

remember(
    "project",
    "PhantomOps AI Infrastructure"
)

remember(
    "goal",
    "Build autonomous AI operating system"
)

# =====================================================
# RECALL MEMORY
# =====================================================

print("\nRECALL TEST\n")

print(
    recall("user_name")
)

print(
    recall("project")
)

print(
    recall("goal")
)

# =====================================================
# SHOW ALL MEMORY
# =====================================================

show_memory()