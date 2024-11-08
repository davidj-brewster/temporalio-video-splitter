"""
Worker process that executes workflow activities.
"""
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import VideoProcessingWorkflow
from activities import analyze_video, extract_frames, process_frames

async def main():
    # Connect to server
    client = await Client.connect("localhost:7233")
    
    # Create worker
    worker = Worker(
        client,
        task_queue="video-processing-queue",
        workflows=[VideoProcessingWorkflow],
        activities=[
            analyze_video,
            extract_frames,
            process_frames
        ]
    )
    
    print("Starting worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())


