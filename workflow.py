from temporalio import workflow

@workflow.defn
class DemoWorkflow:
    @workflow.run
    async def run(self, query: str):
        return f"Processed: {query}"