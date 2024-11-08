# workflows.py
"""
Workflow definitions for video processing.
"""
from datetime import timedelta
from typing import List
from temporalio import workflow
from temporalio.common import RetryPolicy
from activities import (
    analyze_video,
    extract_frames,
    process_frames
)

@workflow.defn
class VideoProcessingWorkflow:
    """Workflow for processing video files."""

    @workflow.run
    async def run(self, video_path: str) -> List[str]:
        """
        Execute the video processing workflow.
        
        Args:
            video_path: Path to input video
            
        Returns:
            List of processed frame paths
        """
        # Define retry policy for activities
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(minutes=1),
            maximum_attempts=3,
            non_retryable_error_types=["VideoError"]
        )
        
        # Execute analyze_video activity
        metadata = await workflow.execute_activity(
            analyze_video,
            args=[video_path],  # Pass arguments as a list
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=retry_policy,
            task_queue="video-processing-queue"
        )
        
        # Execute extract_frames activity
        frames = await workflow.execute_activity(
            extract_frames,
            args=[video_path, metadata],  # Pass arguments as a list
            start_to_close_timeout=timedelta(hours=1),
            retry_policy=retry_policy,
            task_queue="video-processing-queue"
        )
        
        # Execute process_frames activity
        processed_frames = await workflow.execute_activity(
            process_frames,
            args=[frames],  # Pass arguments as a list
            start_to_close_timeout=timedelta(hours=1),
            retry_policy=retry_policy,
            task_queue="video-processing-queue"
        )
        
        return processed_frames
