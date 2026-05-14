import asyncio

from runtime.runtime_manager import (
    runtime_manager
)

from core.execution_pipeline import (
    execution_pipeline
)


async def main():

    asyncio.create_task(
        runtime_manager.start()
    )

    await asyncio.sleep(2)

    await execution_pipeline.submit_goal(
        {
            "type":
                "marketplace_mining"
        }
    )

    await execution_pipeline.submit_goal(
        {
            "type":
                "draft_outreach",

            "company":
                "AI Startup",

            "need":
                "workflow automation"
        }
    )

    while True:

        await asyncio.sleep(1)


if __name__ == "__main__":

    asyncio.run(main())