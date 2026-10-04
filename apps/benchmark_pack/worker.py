class BenchmarkPackWorker:
    def __init__(self, engine: object | None = None) -> None:
        self.engine = engine

    async def run(self, task: dict) -> dict:
        return await self.engine.execute(task)


benchmark_pack_worker = BenchmarkPackWorker()
