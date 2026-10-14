import asyncio

from jarvis_next.govi_core import GoviCore


# Legacy scheduler retained for compatibility; execution authority now flows
# through GOVI -> JARVIS-NEXT instead of the legacy core.Jarvis orchestrator.
govi = GoviCore()


class AutonomousRuntime:

    def __init__(self):

        self.running = True

        self.marketplace_interval = 300

        self.inbox_interval = 180

    async def marketplace_loop(
        self
    ):

        while self.running:

            try:

                print(
                    "\n[Runtime] "
                    "Scanning live marketplace..."
                )

                result = await govi.submit(
                    {"type": "live_marketplace"}
                )

                print(
                    f"[Marketplace] "
                    f"{result}"
                )

            except Exception as error:

                print(
                    f"[Marketplace Error] "
                    f"{error}"
                )

            await asyncio.sleep(
                self.marketplace_interval
            )

    async def inbox_loop(
        self
    ):

        while self.running:

            try:

                print(
                    "\n[Runtime] "
                    "Scanning inbox..."
                )

                result = await govi.submit(
                    {"type": "inbox_monitor"}
                )

                print(
                    f"[Inbox] "
                    f"{result}"
                )

            except Exception as error:

                print(
                    f"[Inbox Error] "
                    f"{error}"
                )

            await asyncio.sleep(
                self.inbox_interval
            )

    async def run(
        self
    ):

        print(
            "[Runtime] "
            "Autonomous runtime started"
        )

        await asyncio.gather(

            self.marketplace_loop(),

            self.inbox_loop()
        )


autonomous_runtime = (
    AutonomousRuntime()
)
