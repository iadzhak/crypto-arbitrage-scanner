import asyncio


class Scanner:
    def __init__(self, exchanges):
        pass

    def get_data(self) -> list[dict]:
        pass

    async def run(self):
        pass

    def run_async(self):
        asyncio.run(self.run())
