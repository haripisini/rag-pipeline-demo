import asyncio
from temporalio.client import Client

async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        "DemoWorkflow.run",
        "test query",
        id="demo-id",
        task_queue="demo-task",
    )

    print(result)

asyncio.run(main())