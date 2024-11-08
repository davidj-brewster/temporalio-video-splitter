# activities.py
"""
Activity definitions for video processing tasks.
"""
import os
from dataclasses import dataclass
from typing import List
from time import sleep
from temporalio import activity
import cv2

@dataclass
class VideoMetadata:
    """Video metadata container."""
    width: int
    height: int
    fps: float
    frame_count: int
    duration: float

@activity.defn
async def analyze_video(video_path: str) -> VideoMetadata:
    """
    Analyze video and extract metadata.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Video metadata
    """
    # Ensure the file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")
        
    try:
        # Extract basic properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        
        return VideoMetadata(
            width=width,
            height=height,
            fps=fps,
            frame_count=frame_count,
            duration=duration
        )
    finally:
        cap.release()

@activity.defn
async def extract_frames(
    video_path: str,
    metadata: VideoMetadata
) -> List[str]:
    """
    Extract frames from video.
    
    Args:
        video_path: Path to video file
        metadata: Video metadata
        
    Returns:
        List of frame file paths
    """
    # Create output directory if it doesn't exist
    output_dir = "extracted_frames"
    os.makedirs(output_dir, exist_ok=True)
    
    frame_paths = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")
    
    try:
        frame_number = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Add frame number as text overlay
            text = f"Frame: {frame_number}"
            # Use putText instead of draw.Text
            #cv2.putText(
            #    frame,
            #    text,
            #    (10, 30),  # Position (x, y)
            #    cv2.FONT_HERSHEY_SIMPLEX,  # Font
            #    1,  # Font scale
            #    (255, 255, 255),  # Color (BGR)
            #    2,  # Thickness
            #    cv2.LINE_AA  # Line type
            #)
                
            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{frame_number:06d}.png")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            frame_number += 1
            
            # Report progress
            if frame_number % 10 == 0:  # Report every 10 frames
                activity.heartbeat(frame_number / metadata.frame_count)
            
    finally:
        cap.release()
        
    return frame_paths

@activity.defn
async def process_frames(frame_paths: List[str]) -> List[str]:
    """
    Process extracted frames.
    
    Args:
        frame_paths: List of frame paths to process
        
    Returns:
        List of processed frame paths
    """
    # Create output directory if it doesn't exist
    output_dir = "processed_frames"
    os.makedirs(output_dir, exist_ok=True)
    
    processed_paths = []
    
    for i, frame_path in enumerate(frame_paths):
        # Read frame
        frame = cv2.imread(frame_path)
        if frame is None:
            print(f"Warning: Could not read frame: {frame_path}")
            continue
            
        # Process frame (example: apply Gaussian blur and edge detection)
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        edges = cv2.Canny(blurred, 100, 200)
        
        # Convert back to BGR for colored edge visualization
        colored_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Add processing info as text
        text = f"Processed Frame: {i}"
        cv2.putText(
            colored_edges,
            text,
            (10, 30),  # Position
            cv2.FONT_HERSHEY_SIMPLEX,  # Font
            1,  # Font scale
            (0, 255, 0),  # Color (BGR)
            2,  # Thickness
            cv2.LINE_AA  # Line type
        )
        
        # Save processed frame
        output_path = os.path.join(output_dir, f"processed_{i:06d}.png")
        cv2.imwrite(output_path, colored_edges)
        processed_paths.append(output_path)
        
        # Report progress
        if i % 10 == 0:  # Report every 10 frames
            activity.heartbeat(i / len(frame_paths))
            sleep(1)
    
    return processed_paths
