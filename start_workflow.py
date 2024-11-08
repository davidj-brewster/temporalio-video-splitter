# start_workflow.py
"""
Control script to start and manage Temporal workflows.
"""
import asyncio
from datetime import timedelta
from temporalio.client import Client
from workflows import VideoProcessingWorkflow

async def main():
    # Create client connected to server
    client = await Client.connect("localhost:7233")
    
    # Start a workflow
    handle = await client.start_workflow(
        VideoProcessingWorkflow.run,
        "input_video.mp4",
        id="video-processing-workflow",
        task_queue="video-processing-queue",
        execution_timeout=timedelta(hours=1)
    )
    
    # Wait for result
    result = await handle.result()
    print(f"Workflow completed with result: {result}")

if __name__ == "__main__":
    asyncio.run(main())

